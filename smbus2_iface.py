#
# Interfaces class to for using native I2C (SMBus) on Linux to talk to devices.
# A wrapper around the smbus2 package, implementing I_I2C
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

class smbus2_i2c(I_I2C):
    '''
    smbus2 wrapper for the I_I2C interface class
    '''
    def __init__(self, bus_num: int):
        #Import the smbus2 package here so it doesn't cause conflicts on Windows
        #when this file is imported. Should only get touched if the class is
        #initialized
        global _smbus, _i2c_msg
        from smbus2 import SMBus as _smbus
        self.__bus = _smbus(bus_num)

    def i2c_read_words(self, bus_addr:int , reg_addr: int, num_words: int):
        rd = self.__bus.read_i2c_block_data(bus_addr >> 1, reg_addr, num_words * 2)
        #< for little endian, H for unsigned short
        return unpack('<' + 'H'*num_words, bytes(rd))

    def sbs_block_read(self, bus_addr: int, reg_addr: int, num_bytes: int):
        rd = self.__bus.read_i2c_block_data(bus_addr >> 1, reg_addr, num_bytes)
        return bytes(rd)

    def sbs_word_read(self, bus_addr: int, reg_addr: int):
        rd = self.__bus.read_i2c_block_data(bus_addr >> 1, reg_addr, 2)
        #< for little endian, H for unsigned short
        return unpack('<' + 'H', bytes(rd))[0]
