#
# Interfaces class to for using FTDI2232 on Windows to talk to devices.
# Uses the ftd2xx package, implementing I_I2C
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
from i2c_iface import I_I2C
from struct import unpack
from time import sleep

# Constants for building commands for the FTDI MPSSE. Taken from the libMPSSE
# source code
CMD_SET_DATABITS_LOW    = 0x80
CMD_DATAOUT_NEG_EDGE    = 0x13
CMD_DATAIN_POS_EDGE     = 0x22
CMD_SEND_IMMEDIATE      = 0x87
CMD_CLKDIV_DISABLE      = 0x8B
CMD_SET_CLOCK           = 0x86
DATASIZE_1BIT           = 0x00
DATASIZE_8BITS          = 0x07
DATA_SEND_NACK          = 0x80
DATA_SEND_ACK           = 0x00
VAL_SCLHI_SDAHI         = 0x03
VAL_SCLHI_SDALO         = 0x01
VAL_SCLLO_SDALO         = 0x00
VAL_SCLLO_SDAHI         = 0x02
DIR_SCLOUT_SDAOUT       = 0x13
DIR_SCLIN_SDAIN         = 0x10
DIR_SCLOUT_SDAIN        = 0x11


class ftd2xx_i2c(I_I2C):
    '''
    FTDI wrapper for the I_I2C interface class.  This class leverages ftd2xx on
    Windows and pylibftdi on Linux.  There are other alternative Python libraries
    however they all depend on various libusb drivers being used for the
    device, which breaks the ability to interface with the EvKit using the
    ADI provided GUI.

    The code here was lifted from the MPSSE library code provided by FTDI, and
    is unfortunately a little bit of magic in terms of commands.
    '''
    def __init__(self, bus_num: int):
        #Import the ftd2xx package here so it doesn't cause conflicts on other
        #systems when this file is imported. Should only get touched if the
        #class is initialized
        #
        #In the future, try using something like pylibftdi for Linux
        global _ftd
        import ftd2xx as _ftd
        self.__dev = _ftd.open(bus_num)
        self.__dev.setLatencyTimer(8)
        self.__dev.setBitMode(0, 0) #Reset MPSSE
        self.__dev.setBitMode(0, 2) #Enable MPSSE

        sleep(0.05)
        #Clock speed is 100kHz: 0x8B = Clock Divide
        self.__ft_write([CMD_CLKDIV_DISABLE, 1])
        div = int((6000000 / (40000 * 2)) - 1)  # Set I2C Clock
        self.__ft_write([CMD_SET_CLOCK, div % 256, div // 256])

        #Flush the read queue
        self.__ft_read(2)

        #Set IO Pin States
        self.__ft_write([CMD_SET_DATABITS_LOW, 0x13, 0x13])

    def __ft_write(self, data):
        '''
        Writes a byte stream to the FTDI for processing

        :param data: Iterable of bytes to send
        :return: Result from the write command
        '''
        s = bytes(data)
        return self.__dev.write(s)

    def __ft_read(self, nbytes):
        '''
        Reads the specified number of bytes from the FTDI device and converts to
        bytes depending on the return value
        :param nbytes: Number of bytes to read
        :return: List of byte data read
        '''
        s = self.__dev.read(nbytes)
        return [ord(c) for c in s] if type(s) is str else list(s)

    def __ft_i2c_start(self):
        '''
        Performs a I2C bus start action. This logic was taken directly from MPSSE.
        '''
        START_DUR_1 = 10
        START_DUR_2 = 20
        cmd_data = [CMD_SET_DATABITS_LOW, VAL_SCLHI_SDAHI, DIR_SCLOUT_SDAOUT] * START_DUR_1
        cmd_data.extend([CMD_SET_DATABITS_LOW, VAL_SCLHI_SDALO, DIR_SCLOUT_SDAOUT] * START_DUR_2)
        cmd_data.extend([CMD_SET_DATABITS_LOW, VAL_SCLLO_SDALO, DIR_SCLOUT_SDAOUT])
        self.__ft_write(cmd_data)

    def __ft_i2c_stop(self):
        '''
        Performs a I2C bus stop action. This logic was taken directly from MPSSE.
        '''
        STOP_DUR_1 = 10
        STOP_DUR_2 = 10
        STOP_DUR_3 = 10
        cmd_data = [CMD_SET_DATABITS_LOW, VAL_SCLLO_SDALO, DIR_SCLOUT_SDAOUT] * STOP_DUR_1
        cmd_data.extend([CMD_SET_DATABITS_LOW, VAL_SCLHI_SDALO, DIR_SCLOUT_SDAOUT] * STOP_DUR_2)
        cmd_data.extend([CMD_SET_DATABITS_LOW, VAL_SCLHI_SDAHI, DIR_SCLOUT_SDAOUT] * STOP_DUR_3)
        cmd_data.extend([CMD_SET_DATABITS_LOW, VAL_SCLHI_SDAHI, DIR_SCLIN_SDAIN])
        self.__ft_write(cmd_data)

    def __ft_i2c_write_get_ack(self, data):
        '''
        Writes the specified data byte (could be data or the device address) and
        gets the response (ACK/NACK) from the bus.  If an ACK, this returns
        normally, if a NACK, this throws a IOError.
        :param data: Data byte to write
        :raises: IOError on a NACK
        '''
        cmd_data = [CMD_SET_DATABITS_LOW, VAL_SCLLO_SDAHI, DIR_SCLOUT_SDAOUT]
        cmd_data.extend([CMD_DATAOUT_NEG_EDGE, DATASIZE_8BITS, data])
        cmd_data.extend([CMD_SET_DATABITS_LOW, VAL_SCLLO_SDALO, DIR_SCLOUT_SDAIN])
        cmd_data.extend([CMD_DATAIN_POS_EDGE, DATASIZE_1BIT])
        cmd_data.append(CMD_SEND_IMMEDIATE)
        self.__ft_write(cmd_data)
        result = self.__ft_read(1)
        #Throw an exception on a NACK
        if result[0] & 0x1:
            raise IOError

    def __ft_i2c_read_give_ack(self, nack = False):
        '''
        Reads a byte from the I2C bus and provides the corresponding end bit
        (ACK or NACK).
        :param: nack (Default False), NACK the bus instead of ACK
        '''
        cmd_data = [CMD_SET_DATABITS_LOW, VAL_SCLLO_SDALO, DIR_SCLOUT_SDAIN]
        cmd_data.extend([CMD_DATAIN_POS_EDGE, DATASIZE_8BITS])
        if nack:
            cmd_data.extend([CMD_SET_DATABITS_LOW, VAL_SCLLO_SDALO, DIR_SCLOUT_SDAIN])
            cmd_data.extend([CMD_DATAOUT_NEG_EDGE, DATASIZE_1BIT, DATA_SEND_NACK])
        else:
            cmd_data.extend([CMD_SET_DATABITS_LOW, VAL_SCLLO_SDALO, DIR_SCLOUT_SDAOUT])
            cmd_data.extend([CMD_DATAOUT_NEG_EDGE, DATASIZE_1BIT, DATA_SEND_ACK])
        cmd_data.extend([CMD_SET_DATABITS_LOW, VAL_SCLLO_SDALO, DIR_SCLOUT_SDAIN])
        cmd_data.append(CMD_SEND_IMMEDIATE)

        self.__ft_write(cmd_data)
        return self.__ft_read(1)[0]

    def __ft_i2c_dev_addr(self, bus_addr, read = False):
        '''
        Sends the device address to the bus correctly depending if it is a read
        or write action.
        :param bus_addr: 8-bit device address. Lowest bit is ignored
        :param read: Read operation (lsb will get set)
        '''
        addr = (bus_addr & 0xFE)
        if read:
            addr |= 0x1
        self.__ft_i2c_write_get_ack(addr)

    def __ft_i2c_write_reg_addr(self, bus_addr, reg_addr, stop = False ):
        '''
        Performs a write transaction for reg address. Starts the bus, sends the
        device address then the register address. A stop bit is optional
        :param bus_addr: Address of the device on the bus (8-bit)
        :param reg_addr: Register address (data byte to send)
        :param stop: Send a stop bit or not
        '''
        self.__ft_i2c_start()
        self.__ft_i2c_dev_addr(bus_addr)
        self.__ft_i2c_write_get_ack(reg_addr)
        if stop:
            self.__ft_i2c_stop()

    def __ft_i2c_read_bytes(self, bus_addr, num_bytes, stop = True):
        '''
        Performs a read transaction. Starts the bus, sends the device address
        then perform num_bytes worth of reads. A stop bit is optional.
        Note: This currently NACK's on the last data byte
        :param bus_addr: Address of the device on the bus (8-bit)
        :param num_bytes: Number of bytes to read
        :param stop: Send a stop bit or not
        '''
        out_data = []
        self.__ft_i2c_start()
        self.__ft_i2c_dev_addr(bus_addr, read=True)
        for i in range(num_bytes):
            out_data.append(self.__ft_i2c_read_give_ack(i==(num_bytes-1)))
        if stop:
            self.__ft_i2c_stop()
        return out_data

    def i2c_read_words(self, bus_addr:int , reg_addr: int, num_words: int):
        self.__ft_i2c_write_reg_addr(bus_addr, reg_addr, False)
        rd = self.__ft_i2c_read_bytes(bus_addr,num_words*2, True)
        #< for little endian, H for unsigned short
        return unpack('<' + 'H'*num_words, bytes(rd))

    def sbs_block_read(self, bus_addr: int, reg_addr: int, num_bytes: int):
        self.__ft_i2c_write_reg_addr(bus_addr, reg_addr, False)
        return self.__ft_i2c_read_bytes(bus_addr,num_bytes, True)

    def sbs_word_read(self, bus_addr: int, reg_addr: int):
        return self.i2c_read_words(bus_addr, reg_addr, 1)[0]

