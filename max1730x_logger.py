#
# Core logging functionality for the application. Continuously logs register
# data for the attached MAX1730x device.
#
# Copyright © 2025 by Analog Devices, Inc.  All rights reserved.
# This software is proprietary to Analog Devices, Inc. and its licensors.
# This software is provided on an “as is” basis without any representations,
# warranties, guarantees or liability of any kind.
# Use of the software is subject to the terms and conditions of the
# Clear BSD License ( https://spdx.org/licenses/BSD-3-Clause-Clear.html ).
#
# Author: Brent Kowal <brent.kowal@analog.com>
#
import platform
import argparse
import csv
import io
import time
import max1730x_regs
from datetime import datetime
from i2c_iface import I_I2C
from smbus2_iface import smbus2_i2c
from ftd2xx_iface import ftd2xx_i2c
####
# Note: While likely not necessary, to save on some unnecessary dictionaries or
# data frames, the register data is pulled in and written to the CSV
# sequentially based on the order of the register maps.  This same ordering is
# used to generate the CSV headers. An alternate approach would be store each
# read block into a dictionary or data frame and have the CSV written from there.
# The application is simple enough this approach should be just fine. Just be
# mindful to change both the header generation and data capture order if changes
# occur.


# Dictionary of possible interface names and the classes
INTERFACE_DICT = { 'smbus2' : smbus2_i2c,
                   'ftdi'   : ftd2xx_i2c}

#Status interval in seconds
STATUS_INTERVAL = 30

def get_header_fields(keep_rsvd: bool):
    '''
    Function to provide a list of the column headers for the CSV file. The order
    of the fields is based on the order of the register lists from the regs
    package. This same ordering needs to be followed during actual data capture.

    :param keep_rsvd: Flag to also store Reserved register data
    :return: List of header fields (strs)
    '''
    hdrfields = ['Timestamp']
    for page in max1730x_regs.REGISTER_PAGES:
        for idx,r in enumerate(page.reg_names):
            if keep_rsvd and (r == None):
                hdrfields.append('RSVD_{:03X}'.format(page.base_addr + idx))
            elif r != None:
                hdrfields.append(r + '_{:03X}'.format(page.base_addr + idx))

    for sbs in max1730x_regs.SBS_REGISTERS:
        hdrfields.append(sbs.reg_name + '_{:03X}'.format(sbs.base_addr))

    return hdrfields


def start_logging(output_file: io.TextIOBase,  bus_dev: I_I2C,
                  quit_on_error: bool = False, interval:float = 5.0,
                  keep_rsvd:bool = False):
    '''
    Performs the actual logging loop. Generates and writes the CSV headers,
    then periodically (based on the interval) collects the register data and
    writes it to a file.  The loop will terminate on a KeyboardInterrupt.
    If a I2C error (or other exception occurs), optionally the loop can exit, or
    continue trying to execute.

    :param output_file: Opened file descriptor to write the data to
    :param bus_dev: I2C Bus instance
    :param quit_on_error: Determines if the loop should quit on any non-keyboard
                          exception
    :param interval: Collection interval in seconds
    :param keep_rsvd: Flag to capture Reserved registers as well
    '''
    csv_wr = csv.writer(output_file)
    csv_wr.writerow(get_header_fields(keep_rsvd))
    record_ct = 0
    status_time = 0
    while True:
        try:
            #Current time stamp, and when the next interval should occur
            now_time = time.time()
            next_time = now_time + interval

            #The row data starts with timestamp. Just use Epoch time in seconds
            row_data = [str(int(now_time))]

            #Do the register pages first
            for page in max1730x_regs.REGISTER_PAGES:
                reg_data = bus_dev.i2c_read_words(page.dev_addr, page.base_addr & 0xFF, 16)
                if keep_rsvd:
                    row_data += ['{:04X}'.format(w) for w in reg_data]
                else:
                    row_data += ['{:04X}'.format(w) for idx,w in enumerate(reg_data) if page.reg_names[idx] != None]

            #SBS Registers
            for sbs in max1730x_regs.SBS_REGISTERS:
                if sbs.block_size > 0:
                    #For block reads, the data is a bit Hex string
                    reg_data = bus_dev.sbs_block_read(sbs.dev_addr, sbs.base_addr & 0xFF, sbs.block_size)
                    row_data.append(''.join(['{:02X}'.format(r) for r in reg_data]))
                else:
                    #For words, same as a normal 16-bit register
                    row_data.append('{:04X}'.format(bus_dev.sbs_word_read(sbs.dev_addr, sbs.base_addr & 0xFF)))

            #Write it to the CSV file
            csv_wr.writerow(row_data)
            record_ct += 1

            #Some simple status to let the user know its still running
            if now_time > status_time:
                print('{:d} Records Logged...'.format(record_ct))
                status_time = now_time + STATUS_INTERVAL

            #Simple periodic loop, accounting for time spent doing work
            delay = next_time - time.time()
            if delay > 0:
                time.sleep(delay)

        except KeyboardInterrupt:
            #Always exit on a keyboard interrupt
            print('User interrupt via Keyboard')
            break
        except Exception as ex:
            print('Exception: ' + str(ex))
            if(quit_on_error):
                break


def arg_check_interface(value: str):
    '''
    Performs an argument check for the interface option. Use the INTERFACE_DICT
    for valid values

    :param value: Input string from the user
    :return: Class reference for the I2C interface
    :raises: ArgumentTypeError on an invalid choice
    '''
    if value.lower() not in INTERFACE_DICT:
        raise argparse.ArgumentTypeError('%s is not a valid interface' % value)
    return INTERFACE_DICT[str(value).lower()]


if __name__ == '__main__':
    #Generate a default file name based on the current date and time
    def_out_file = datetime.now().strftime('max1730x_log_%Y-%m-%d_%H%M%S.csv')

    #Give the user some valuable defaults
    if platform.system() == 'Windows':
        def_iface = 'ftdi'
        def_bus = 1
    else:
        def_iface = 'smbus2'
        def_bus = 6

    #Accept some user arguments
    parser = argparse.ArgumentParser(
        description='Simple application for continuously logging the register '
                     'map for the MAX1730x series of parts',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--iface', dest='iface',
                        type=arg_check_interface, default=def_iface,
                        help='Select Interface: ' + ','.join(INTERFACE_DICT.keys()))
    parser.add_argument('-b', '--bus', dest='bus_num',
                        type=int, default=def_bus,
                        help='I2C bus number for the interface.')
    parser.add_argument('-o', '--output', dest='out_file',
                        type=str, default=def_out_file,
                        help='File name for the output CSV')
    parser.add_argument('-x', dest='exit_on_error', action='store_true',
                        help='Exit the application on a bus error.')
    parser.add_argument('-t', '--time', dest='interval',
                        type=float, default=5.0,
                        help='Collection interval, in seconds.')
    args = parser.parse_args()

    try:
        bus = args.iface(args.bus_num)
    except:
        print('Failed to open I2C device!')
        quit()

    # Do a simple poke of a register to make sure comms are alive before starting
    try:
        bus.i2c_read_words(max1730x_regs.M5_DEV_ADDR, 0, 1)
    except:
        print('Failed to communicate with device. Check configuration')
        quit()

    #Per recommendation of CSV documentation, open file with newline = ''
    with open(args.out_file, 'w', newline='', encoding='utf-8') as output_file:
        start_logging(output_file, bus, args.exit_on_error, args.interval)
