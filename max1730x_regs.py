#
# Definitions of the register space for the MAX1730x device.
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
from collections import namedtuple

#Address for the core m5 registers (Regs 0x000-0x0FF)
M5_DEV_ADDR     = 0x6C

#Address for the Non-volatile and SBS registers (Regs 0x100-0x1FF)
SBS_NV_DEV_ADDR = 0x16

#Represents a page of Registers in the device. Each page consists of 16 registers
#The reg_names is just a list of plain-text strings to describe the registers.
#If a reg name is None, that register is designated as Reserved by the device.
RegisterPage = namedtuple('RegisterPage', ['dev_addr', 'base_addr', 'reg_names'])

#Represents a SBS register which could be a single word, or a block read for
#longer data. If block_size <= 0, it is assumed to be a single word. Otherwise,
#block_size is the number of expected bytes in a block read
SBS_Register = namedtuple('SBS_Register', ['dev_addr', 'base_addr', 'block_size', 'reg_name'])

#Registers 0x000-0x00F
M5_DATABLOCK_000 = RegisterPage(M5_DEV_ADDR, 0x000,
   ['Status',     'VAlrtTh',    'TAlrtTh',    'SAlrtTh',
    'AtRate',     'RepCap',     'RepSOC',     'Age',
    'MaxMinVolt', 'MaxMinTemp', 'MaxMinCurr', 'Config',
    'QResidual',  'MixSOC',     'AvSOC',      'MiscCfg'])

#Registers 0x010-0x01F
M5_DATABLOCK_010 = RegisterPage(M5_DEV_ADDR, 0x010,
   ['FullCapRep', 'TTE',        'VCellRep', 'FullSocThr',
    'RSlow',      'RFast',      'AvgTA',    'Cycles',
    'DesignCap',  'AvgVCell',   'VCell',    'Temp',
    'Current',    'AvgCurrent', 'IChgTerm', 'AvCap'])

#Registers 0x020-0x02F
M5_DATABLOCK_020 = RegisterPage(M5_DEV_ADDR, 0x020,
   ['TTF',             'DevName',   'CurrRep',         'FullCapNom',
    None,              None,        None,              'AIN0',
    'ChargingCurrent', 'FilterCfg', 'ChargingVoltage', 'MixCap',
    None,              None,        None,              None])

#Registers 0x030-0x03F
M5_DATABLOCK_030 = RegisterPage(M5_DEV_ADDR, 0x030,
   [None,      None,      'QRTable20', None,
    'DieTemp', 'FullCap', 'IAvgEmpty', None,
    None,      'FStat2',  'VEmpty',    None,
    None,      'FStat',   'Timer',     'Vrelax'])

#Registers 0x040-0x04F
M5_DATABLOCK_040 = RegisterPage(M5_DEV_ADDR, 0x040,
   ['AvgDieTemp', None,          'QRTable30', None,
    None,         'dQAcc',       'dPAcc',     None,
    None,         'ProtTmrStat', 'VFRemCap',  None,
    None,         'QH',          None,        None])

#Registers 0x0A0-0x0AF
M5_DATABLOCK_0A0 = RegisterPage(M5_DEV_ADDR, 0x0A0,
   ['RelaxCfg',      'LearnCfg',     None,             None,
    'MaxPeakPower',  'SusPeakPower', 'PackResistance', 'SysResistance',
    'MinSysVoltage', 'MPPCurrent',   'SPPCurrent',     'Config2',
    'IAlrtTh',       'MinVolt',      'MinCurr',        None])

#Registers 0x0B0-0x0BF
M5_DATABLOCK_0B0 = RegisterPage(M5_DEV_ADDR, 0x0B0,
   ['Status2',     'Power',       'VRipple',  'AvgPower',
    'ReturnPatch', 'TTFCfg',      'CVMixCap', 'CVHalfTime',
    'CGTempCo',    'AgeForecast', None,       'FOTPStat',
    None,          None,          'TimerH',    None,])

#Registers 0x0D0-0x0DF
M5_DATABLOCK_0D0 = RegisterPage(M5_DEV_ADDR, 0x0D0,
   ['SOCHold',     None,         None,      None,
    'AvgCell1',    None,         None,      'Status',
    'CELL1',       'ProtStatus', None,      'ModelCfg',
    'AtQResidual', 'AtTTE',      'AtAvSOC', 'AtAvCap'])

#Registers 0x0F0-0x0FF
M5_DATABLOCK_0F0 = RegisterPage(M5_DEV_ADDR, 0x0F0,
   [None, None,       None, None,
    None, 'HConfig2', None, None,
    None, None,       None, 'VFOCV',
    None, None,       None, 'VFSOC'])

#Registers 0x180-0x18F
M5_NVBLOCK_180 = RegisterPage(SBS_NV_DEV_ADDR, 0x180,
   ['nCAPTable0', 'nCAPTable1', 'nCAPTable2', 'nCAPTable3',
    'nCAPTable4', 'nCAPTable5', 'nCAPTable6', 'nCAPTable7',
    'nCAPTable8', 'nCAPTable9', 'nCAPTable10','nCAPTable11',
    'nVAlrtTh',   'nTAlrtTh',   'nIAlrtTh',   'nSAlrtTh'])

#Registers 0x190-0x19F
M5_NVBLOCK_190 = RegisterPage(SBS_NV_DEV_ADDR, 0x190,
   ['nOCVTable0', 'nOCVTable1', 'nOCVTable2',  'nOCVTable3',
    'nOCVTable4', 'nOCVTable5', 'nOCVTable6',  'nOCVTable7',
    'nOCVTable8', 'nOCVTable9', 'nOCVTable10', 'nOCVTable11',
    'nIChgTerm',  'nFilterCfg', 'nVEmpty',     'nLearnCfg'])

#Registers 0x1A0-0x1AF
CFG_NVBLOCK_1A0 = RegisterPage(SBS_NV_DEV_ADDR, 0x1A0,
   ['nQRTable00', 'nQRTable10',   'nQRTable20',    'nQRTable30',
    'nCycles',     'nFullCapNom', 'nRComp0',      'nTempCo',
    'nBattStatus', 'nFullCapRep', 'nVoltTemp',    'nMaxMinCurr',
    'nMaxMinVolt', 'nMaxMinTemp', 'nFullCapFltr', 'nTimerH' ])

#Registers 0x1B0-0x1BF
CFG_NVBLOCK_1B0 = RegisterPage(SBS_NV_DEV_ADDR, 0x1B0,
   ['nCONFIG', 'nRippleCfg', 'nMiscCFG',  'nDesignCap',
    'nSBSCFG', 'nPACKCFG',   'nRelaxCFG', 'nConvgCFG',
    'nNVCFG0', 'nNVCFG1',    'nNVCFG2',   'nHibCFG',
    'nROMID0', 'nROMID1',    'nROMID2',   'nROMID3'])

#Registers 0x1C0-0x1CF
CFG_NVBLOCK_1C0 = RegisterPage(SBS_NV_DEV_ADDR, 0x1C0,
   [None,           None,              None,            None,
    'nRGain',       'nPackResistance', 'nFullSOCThr',   'nTTFCFG',
    'nCGAIN',       'nTCurve',         'nThermcfg',     'nTOFF',
    'nManfctrName', 'nManfctrName1',   'nManfctrName2', 'nRSense'])

#Registers 0x1D0-0x1DF
PROT_NVBLOCK_1D0 = RegisterPage(SBS_NV_DEV_ADDR, 0x1D0,
   ['nVPrtTh1',  'nTPrtTh1', 'nTPrtTh3',    'nIPrtTh1',
    'nVPrtTh2',  'nTPrtTh2', 'nProtMiscTh', 'nProtCfg',
    'nJEITAC',   'nJEITAV',  'nJEITACfg',   'nStepChg',
    'nDelayCfg', 'nODSCTh',  'nODSCCfg',    'nCheckSum'])

#Registers 0x1E0-0x1EF
USER_NVBLOCK_1E0 = RegisterPage(SBS_NV_DEV_ADDR, 0x1E0,
   ['nDPLimit',       'nScOcvLim',      'nAgeFcCfg',      'nDesignVoltage',
    'nPackCfg2',      'nRFastVShdn',    'nManfctrDate',   'nFirstUsed',
    'nSerialNumber0', 'nSerialNumber1', 'nSerialNumber2', 'nDeviceName0',
    'nDeviceName1',   'nDeviceName2',   'nDeviceName3',   'nDeviceName4'])

#All of the SBS Registers (0x100-0x17F, sparsely filled)
SBS_REGISTERS = [
    SBS_Register(SBS_NV_DEV_ADDR, 0x100, 0, 'sManfctAccess'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x101, 0, 'sRemCapAlarm'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x102, 0, 'sRemTimeAlarm'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x103, 0, 'sBatteryMode'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x104, 0, 'sAtRate'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x106, 0, 'sAtTTE'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x107, 0, 'sAtRateOK'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x108, 0, 'sTemperature'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x109, 0, 'sPackVoltage'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x10A, 0, 'sCurrent'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x10B, 0, 'sAvgCurrent'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x10C, 0, 'sMaxError'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x10D, 0, 'sRelSOC'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x10E, 0, 'sAbsSOC'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x10F, 0, 'sRemCap'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x110, 0, 'sFullCap'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x111, 0, 'sRunTTE'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x112, 0, 'sAvgTTE'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x113, 0, 'sAvgTTF'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x114, 0, 'sChargingCurrent'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x115, 0, 'sChargingVoltage'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x116, 0, 'sBatteryStatus'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x117, 0, 'sCycles'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x118, 0, 'sDesignCap'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x119, 0, 'sDesignVolt'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x11A, 0, 'sSpecInfo'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x11B, 0, 'sManfctDate'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x11C, 6, 'sSerialNumber'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x120, 5, 'sManfctName'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x121, 5, 'sDeviceName'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x122, 4, 'sDevChemistry'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x123, 9, 'sManfctData'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x134, 0, 'sTemp1'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x135, 0, 'sIntTemp'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x136, 0, 'sFirstUsed'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x137, 0, 'sAvgTemp1'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x138, 0, 'sAvgIntTemp'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x13F, 0, 'sCell1'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x14F, 0, 'sAvgCell1'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x167, 0, 'sAvCap'),
    SBS_Register(SBS_NV_DEV_ADDR, 0x168, 0, 'sMixCap'),
    #Not supported in MAX1730x
    #SBS_Register(SBS_NV_DEV_ADDR, 0x170, True,  'sManfctInfo'),
]

#Put all the register pages in a list for easy iteration
REGISTER_PAGES = [
    M5_DATABLOCK_000, M5_DATABLOCK_010, M5_DATABLOCK_020, M5_DATABLOCK_030,
    M5_DATABLOCK_040, M5_DATABLOCK_0A0, M5_DATABLOCK_0B0, M5_DATABLOCK_0D0,
    M5_DATABLOCK_0F0, M5_NVBLOCK_180,   M5_NVBLOCK_190,   CFG_NVBLOCK_1A0,
    CFG_NVBLOCK_1B0,  CFG_NVBLOCK_1C0,  PROT_NVBLOCK_1D0, USER_NVBLOCK_1E0 ]
