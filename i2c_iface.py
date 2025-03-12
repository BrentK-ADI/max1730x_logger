#
# Interfaces class to abstract out bus accesses between different host I2C
# interfaces
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

class I_I2C:
    '''
    Interface class defining basic read access to the I2C as needed by the
    MAX1730x devices
    '''
    def i2c_read_words(self, bus_addr: int, reg_addr: int, num_words: int):
        '''
        Reads a series of words (unsigned 16-bit) from the device starting
        at the provided reg_addr.  2x num_words is read, and the result is
        a list of uint16, built via little endian from the read bytes.

        :param bus_addr: 8-bit I2C bus address. lsb (R/W bit) is ignored
        :param reg_addr: Starting register address to read from
        :param num_words: Number of 16-bit words to read
        :return: Sequential list of read words
        '''
        raise NotImplementedError

    def sbs_block_read(self, bus_addr: int, reg_addr: int, num_bytes: int):
        '''
        Performs a block read from SBS registers

        :param bus_addr: 8-bit I2C bus address. lsb (R/W bit) is ignored
        :param reg_addr: Starting register address to read from
        :param num_bytes: Number of bytes to read
        :return: Sequential list of read bytes
        '''
        raise NotImplementedError

    def sbs_word_read(self, bus_addr: int, reg_addr: int):
        '''
        Reads a single word (unsigned 16-bit) from the device's SBS register

        :param bus_addr: 8-bit I2C bus address. lsb (R/W bit) is ignored
        :param reg_addr: Register address to read from
        :return: Read word
        '''
        raise NotImplementedError
