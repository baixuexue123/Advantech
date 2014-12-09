#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'baixue'


from ctypes import *


MAX_DRIVER_NAME_LEN = 128


#------------------设备函数组-------------------#

class tagGAINLIST(Structure):
    _fields_ = [("usGainCde", c_int),
                ("fMaxGainVal", c_int),
                ("fMinGainVal", c_int),
                ("szGainStr[16]", c_int)
        ]
GAINLIST = tagGAINLIST


class tagDEVFEATURES(Structure):
    _fields_ = [("szDriverVer", c_char*8),
                ("szDriverName", c_char*MAX_DRIVER_NAME_LEN),
                ("dvBoardID", c_uint),
                ("usMaxAIDiffChl", c_ushort),
                ("usMaxAISiglChl", c_ushort),
                ("usMaxAOChl", c_ushort),
                ("usMaxDOChl", c_ushort),
                ("usMaxDIChl", c_ushort),
                ("usDIOPort", c_ushort),
                ("usMaxTimerChl", c_ushort),
                ("usMaxAlarmChl", c_ushort),
                ("usNumADBit", c_ushort),
                ("usNumADByte", c_ushort),
                ("usNumDABit", c_ushort),
                ("usNumDAByte", c_ushort),
                ("usNumGain", c_ushort),
                ("glGainList[16]", GAINLIST*16),
                ("dvPermutation[4]", c_uint*4)
        ]
DEVFEATURES = tagDEVFEATURES
LPDEVFEATURES = POINTER(tagDEVFEATURES)


class tagPT_DeviceGetFeatures(Structure):
    _fields_ = [("buffer", LPDEVFEATURES),
                ("size", c_ushort)
                #系统保留参数,不必关心该参数的值,建议为该值传入结构体 DEVFEATURES 的大小
        ]
PT_DeviceGetFeatures = tagPT_DeviceGetFeatures
LPT_DeviceGetFeatures = POINTER(tagPT_DeviceGetFeatures)


class tagDAUGHTERSET(Structure):
    _fields_ = [("dwBoardID", c_uint),
                ("usNum", c_ushort),
                ("fGain", c_float),
                ("usCards", c_ushort)
        ]
DAUGHTERSET = tagDAUGHTERSET
LPDAUGHTERSET = POINTER(tagDAUGHTERSET)


class tagPT_DEVLIST(Structure):
    _fields_ = [("dwDeviceNum", c_uint),
                ("szDeviceName", c_char*50),
                ("nNumOfSubDevices", c_short)
        ]
DEVLIST = tagPT_DEVLIST


class tagTRIGLEVEL(Structure):
    _fields_ = [("fLow", c_float),
                ("fHigh", c_float)
        ]
TRIGLEVEL = tagTRIGLEVEL


#------------------模拟量输入函数组-------------------#

class tagPT_AIConfig(Structure):
    _fields_ = [("DasChan", c_ushort),
                ("DasGain", c_ushort)
        ]
PT_AIConfig = tagPT_AIConfig
LPT_AIConfig = POINTER(tagPT_AIConfig)


class tagDEVCONFIG_AI(Structure):
    _fields_ = [("dwBoardID", c_uint),
                ("ulChanConfig", c_uint),
                ("usGainCtrMode", c_ushort),
                ("usPolarity", c_ushort),
                ("usDasGain", c_ushort),
                ("usNumExpChan", c_ushort),
                ("usCjcChannel", c_ushort),
                ("Daughter[MAX_DAUGHTER_NUM]", DAUGHTERSET*3),
                ("ulChanConfigEx", c_uint*3)
        ]
DEVCONFIG_AI = tagDEVCONFIG_AI
LPDEVCONFIG_AI = POINTER(tagDEVCONFIG_AI)


class tagPT_AIGetConfig(Structure):
    _fields_ = [("buffer", LPDEVCONFIG_AI),
                ("size", c_ushort)
        ]
PT_AIGetConfig = tagPT_AIGetConfig
LPT_AIGetConfig = POINTER(tagPT_AIGetConfig)


class tagPT_AIBinaryIn(Structure):
    _fields_ = [("chan", c_ushort),
                ("TrigMode", c_ushort),# 0:内部触发, 1:外部触发
                ("reading", POINTER(c_ushort))
        ]
PT_AIBinaryIn = tagPT_AIBinaryIn
LPT_AIBinaryIn = POINTER(tagPT_AIBinaryIn)


class tagPT_AIScale(Structure):
    _fields_ = [("reading", c_ushort),
                ("MaxVolt", c_float),
                ("MaxCount", c_ushort),
                ("offset", c_ushort),
                ("voltage", POINTER(c_float))
        ]
PT_AIScale = tagPT_AIScale
LPT_AIScale = POINTER(tagPT_AIScale)


class tagPT_AIVoltageIn(Structure):
    _fields_ = [("chan", c_ushort),
                ("gain", c_ushort),
                ("TrigMode", c_ushort),
                ("voltage", POINTER(c_float))
        ]
PT_AIVoltageIn = tagPT_AIVoltageIn
LPT_AIVoltageIn = POINTER(tagPT_AIVoltageIn)


class tagPT_AIVoltageInExp(Structure):
    _fields_ = [("DasChan", c_ushort),
                ("DasGain", c_ushort),
                ("ExpChan", c_ushort),
                ("voltage", POINTER(c_float))
        ]
PT_AIVoltageInExp = tagPT_AIVoltageInExp
LPT_AIVoltageInExp = POINTER(tagPT_AIVoltageInExp)


class tagPT_MAIConfig(Structure):
    _fields_ = [("NumChan", c_ushort),
                ("StartChan", c_ushort),
                ("GainArray", POINTER(c_ushort))
        ]
PT_MAIConfig = tagPT_MAIConfig
LPT_MAIConfig = POINTER(tagPT_MAIConfig)


class tagPT_MAIBinaryIn(Structure):
    _fields_ = [("NumChan", c_ushort),
                ("StartChan", c_ushort),
                ("TrigMode", c_ushort),
                ("ReadingArray", POINTER(c_ushort))
        ]
PT_MAIBinaryIn = tagPT_MAIBinaryIn
LPT_MAIBinaryIn = POINTER(tagPT_MAIBinaryIn)


class tagPT_MAIVoltageInExp(Structure):
    _fields_ = [("NumChan", c_ushort),
                ("DasChanArray", POINTER(c_ushort)),
                ("DasGainArray", POINTER(c_ushort)),
                ("ExpChanArray", POINTER(c_ushort)),
                ("VoltageArray", POINTER(c_float))
        ]
PT_MAIVoltageInExp = tagPT_MAIVoltageInExp
LPT_MAIVoltageInExp = POINTER(tagPT_MAIVoltageInExp)


class tagPT_MAIVoltageIn(Structure):
    _fields_ = [("NumChan", c_ushort),
                ("StartChan", c_ushort),
                ("GainArray", POINTER(c_ushort)),
                ("TrigMode", c_ushort),
                ("VoltageArray", POINTER(c_float))
        ]
PT_MAIVoltageIn = tagPT_MAIVoltageIn
LPT_MAIVoltageIn = POINTER(tagPT_MAIVoltageIn)

#------------------模拟量输出函数组-------------------#

class tagPT_AOConfig(Structure):
    _fields_ = [("chan", c_ushort),
                ("RefSrc", c_ushort),
                ("MaxValue", c_float),
                ("MinValue", c_float)
        ]
PT_AOConfig = tagPT_AOConfig
LPT_AOConfig = POINTER(tagPT_AOConfig)


class tagPT_AOBinaryOut(Structure):
    _fields_ = [("chan", c_ushort),
                ("BinData", c_ushort)
        ]
PT_AOBinaryOut = tagPT_AOBinaryOut
LPT_AOBinaryOut = POINTER(tagPT_AOBinaryOut)


class tagPT_AOVoltageOut(Structure):
    _fields_ = [("chan", c_ushort),
                ("OutputValue", c_float)
        ]
PT_AOVoltageOut = tagPT_AOVoltageOut
LPT_AOVoltageOut = POINTER(tagPT_AOVoltageOut)


class tagPT_AOScale(Structure):
    _fields_ = [("chan", c_ushort),
                ("OutputValue", c_float),
                ("BinData", POINTER(c_ushort))
        ]
PT_AOScale = tagPT_AOScale
LPT_AOScale = POINTER(tagPT_AOScale)


class tagPT_AOCurrentOut(Structure):
    _fields_ = [("chan", c_ushort),
                ("OutputValue", c_float)
        ]
PT_AOCurrentOut = tagPT_AOCurrentOut
LPT_AOCurrentOut = POINTER(tagPT_AOCurrentOut)


class tagAOSET(Structure):
    _fields_ = [("usAOSource", c_ushort),
                ("fAOMaxVol", c_float),
                ("fAOMinVol", c_float),
                ("fAOMaxCur", c_float),
                ("fAOMinCur", c_float)
        ]
AOSET = tagAOSET
LPAOSET = POINTER(tagAOSET)


class tagAORANGESET(Structure):
    _fields_ = [("usGainCount", c_ushort),
                ("usAOSource", c_ushort),
                ("usAOType", c_ushort),
                ("usChan", c_ushort),
                ("fAOMax", c_float),
                ("fAOMin", c_float)
        ]
AORANGESET = tagAORANGESET
LPAORANGESET = POINTER(tagAORANGESET)


#------------------数字量输入/输出组-------------------#

class tagPT_DioReadBit(Structure):
    _fields_ = [("port", c_ushort),
                ("bit", c_ushort),
                ("state", POINTER(c_ushort))
        ]
PT_DioReadBit = tagPT_DioReadBit
LPT_DioReadBit = POINTER(tagPT_DioReadBit)


class tagPT_DioWriteBit(Structure):
    _fields_ = [("port", c_ushort),
                ("bit", c_ushort),
                ("state", c_ushort)
        ]
PT_DioWriteBit = tagPT_DioWriteBit
LPT_DioWriteBit = POINTER(tagPT_DioWriteBit)


class tagPT_DioReadPortByte (Structure):
    _fields_ = [("port", c_ushort),
                ("value", POINTER(c_ushort))
        ]
PT_DioReadPortByte = tagPT_DioReadPortByte
LPT_DioReadPortByte = POINTER(tagPT_DioReadPortByte)


class tagPT_DioWritePortByte(Structure):
    _fields_ = [("port", c_ushort),
                ("mask", c_ushort),
                ("state", c_ushort)
        ]
PT_DioWritePortByte = tagPT_DioWritePortByte
LPT_DioWritePortByte = POINTER(tagPT_DioWritePortByte)


class tagPT_DioReadPortWord(Structure):
    _fields_ = [("port", c_ushort),
                ("value", POINTER(c_ushort)),
                ("ValidChannelMask", POINTER(c_ushort))
        ]
PT_DioReadPortWord = tagPT_DioReadPortWord
LPT_DioReadPortWord = POINTER(tagPT_DioReadPortWord)


class tagPT_DioWritePortWord(Structure):
    _fields_ = [("port", c_ushort),
                ("mask", c_ushort),
                ("state", c_ushort)
        ]
PT_DioWritePortWord = tagPT_DioWritePortWord
LPT_DioWritePortWord = POINTER(tagPT_DioWritePortWord)


class tagPT_DioReadPortDWord(Structure):
    _fields_ = [("port", c_ushort),
                ("value", POINTER(c_ulong)),
                ("ValidChannelMask", POINTER(c_ulong))
        ]
PT_DioReadPortDWord = tagPT_DioReadPortDWord
LPT_DioReadPortDWord = POINTER(tagPT_DioReadPortDWord)


class tagPT_DioWritePortDWord(Structure):
    _fields_ = [("port", c_ushort),
                ("mask", c_ulong),
                ("state", c_ulong)
        ]
PT_DioWritePortDWord = tagPT_DioWritePortDWord
LPT_DioWritePortDWord = POINTER(tagPT_DioWritePortDWord)


class tagPT_DioGetCurrentDOBit(Structure):
    _fields_ = [("port", c_ushort),
                ("bit", c_ushort),
                ("state", POINTER(c_ushort))
        ]
PT_DioGetCurrentDOBit = tagPT_DioGetCurrentDOBit
LPT_DioGetCurrentDOBit = POINTER(tagPT_DioGetCurrentDOBit)


class tagPT_DioGetCurrentDOByte(Structure):
    _fields_ = [("port", c_ushort),
                ("value", POINTER(c_ushort))
        ]
PT_DioGetCurrentDOByte = tagPT_DioGetCurrentDOByte
LPT_DioGetCurrentDOByte = POINTER(tagPT_DioGetCurrentDOByte)


class tagPT_DioGetCurrentDOWord(Structure):
    _fields_ = [("port", c_ushort),
                ("value", POINTER(c_ushort)),
                ("ValidChannelMask", POINTER(c_ushort))
        ]
PT_DioGetCurrentDOWord = tagPT_DioGetCurrentDOWord
LPT_DioGetCurrentDOWord = POINTER(tagPT_DioGetCurrentDOWord)


class tagPT_DioGetCurrentDODword(Structure):
    _fields_ = [("port", c_ushort),
                ("value", POINTER(c_ulong)),
                ("ValidChannelMask", POINTER(c_ulong))
        ]
PT_DioGetCurrentDODword = tagPT_DioGetCurrentDODword
LPT_DioGetCurrentDODword = POINTER(tagPT_DioGetCurrentDODword)


class tagPT_DioSetPortMode(Structure):
    _fields_ = [("port", c_ushort),
                ("dir", c_ushort)
        ]
PT_DioSetPortMode = tagPT_DioSetPortMode
LPT_DioSetPortMode = POINTER(tagPT_DioSetPortMode)


class tagPT_DioGetConfig(Structure):
    _fields_ = [("PortArray", POINTER(c_short)),
                ("NumOfPorts", c_ushort)
        ]
PT_DioGetConfig = tagPT_DioGetConfig
LPT_DioGetConfig = POINTER(tagPT_DioGetConfig)


class tagPT_DIFilter(Structure):
    _fields_ = [("usEventType", c_ushort),
                ("usEventEnable", c_ushort),
                ("usCount", c_ushort),
                ("usEnable", c_ushort),
                ("usHiValue", POINTER(c_ushort)),
                ("usLowValue", POINTER(c_ushort))
        ]
PT_DIFilter = tagPT_DIFilter
LPT_DIFilter = POINTER(tagPT_DIFilter)


class tagPT_DIPattern(Structure):
    _fields_ = [("usEventType", c_ushort),
                ("usEventEnable", c_ushort),
                ("usCount", c_ushort),
                ("usEnable", c_ushort),
                ("usValue", c_ushort)
        ]
PT_DIPattern = tagPT_DIPattern
LPT_DIPattern = POINTER(tagPT_DIPattern)


class tagPT_DIStatus(Structure):
    _fields_ = [("usEventType", c_ushort),
                ("usEventEnable", c_ushort),
                ("usCount", c_ushort),
                ("usEnable", c_ushort),
                ("usRisingedge", c_ushort),
                ("usFallingedge", c_ushort)
        ]
PT_DIStatus = tagPT_DIStatus
LPT_DIStatus = POINTER(tagPT_DIStatus)


#------------------高速数据采集函数组-------------------#

class tagPT_DICounter(Structure):
    _fields_ = [("usEventType", c_ushort),
                ("usEventEnable", c_ushort),
                ("usCount", c_ushort),
                ("usEnable", c_ushort),
                ("usTrigEdge", c_ushort),
                ("usTrigPreset", POINTER(c_ushort)),
                ("usMatchEnable", c_ushort),
                ("usValue", POINTER(c_ushort)),
                ("usOverflow", c_ushort),
                ("usDirection", c_ushort)
        ]
PT_DICounter = tagPT_DICounter
LPT_DICounter = POINTER(tagPT_DICounter)


class tagPT_EnableEvent(Structure):
    _fields_ = [("EventType", c_ushort),
                ("Enabled", c_ushort),
                ("Count", c_ushort)
        ]
PT_EnableEvent = tagPT_EnableEvent
LPT_EnableEvent = POINTER(tagPT_EnableEvent)


class tagPT_EnableEventEx(Structure):
    _fields_ = [("Filter", PT_DIFilter),
                ("Pattern", PT_DIPattern),
                ("Counter", PT_DICounter),
                ("Status", PT_DIStatus)
        ]
PT_EnableEventEx = tagPT_EnableEventEx
LPT_EnableEventEx = POINTER(tagPT_EnableEventEx)


class tagPT_CheckEvent(Structure):
    _fields_ = [("EventType", POINTER(c_ushort)),
                ("Milliseconds", c_uint)
        ]
PT_CheckEvent = tagPT_CheckEvent
LPT_CheckEvent = POINTER(tagPT_CheckEvent)


class tagPT_AllocateDMABuffer(Structure):
    _fields_ = [("CyclicMode", c_ushort),
                ("RequestBufSize", c_ulong),
                ("ActualBufSize", POINTER(c_ulong)),
                ("buffer", POINTER(c_long))
        ]
PT_AllocateDMABuffer = tagPT_AllocateDMABuffer
LPT_AllocateDMABuffer = POINTER(tagPT_AllocateDMABuffer)


class tagPT_FAIIntStart(Structure):
    _fields_ = [("TrigSrc", c_ushort),
                ("SampleRate", c_uint),
                ("chan", c_ushort),
                ("gain", c_ushort),
                ("buffer", POINTER(c_ushort)),
                ("count", c_ulong),
                ("cyclic",c_ushort),
                ("IntrCount",c_ushort)
        ]
PT_FAIIntStart = tagPT_FAIIntStart
LPT_FAIIntStart = POINTER(tagPT_FAIIntStart)


class tagPT_FAIIntScanStart(Structure):
    _fields_ = [("TrigSrc", c_ushort),
                ("SampleRate", c_uint),
                ("NumChans", c_ushort),
                ("StartChan", c_ushort),
                ("GainList", POINTER(c_ushort)),
                ("buffer", POINTER(c_ushort)),
                ("count", c_ulong),
                ("cyclic",c_ushort),
                ("IntrCount",c_ushort)
        ]
PT_FAIIntScanStart = tagPT_FAIIntScanStart
LPT_FAIIntScanStart = POINTER(tagPT_FAIIntScanStart)


class tagPT_FAIDmaStart(Structure):
    _fields_ = [("TrigSrc", c_ushort),
                ("SampleRate", c_uint),
                ("chan", c_ushort),
                ("gain", c_ushort),
                ("buffer", POINTER(c_ushort)),
                ("count", c_ulong)
        ]
PT_FAIDmaStart = tagPT_FAIDmaStart
LPT_FAIDmaStart = POINTER(tagPT_FAIDmaStart)


class tagPT_FAIDmaScanStart(Structure):
    _fields_ = [("TrigSrc", c_ushort),#数据采集触发源: 内部触发 - 0    外部触发 - 1
                ("SampleRate", c_uint),
                ("NumChans", c_ushort),
                ("StartChan", c_ushort),
                ("GainList", POINTER(c_ushort)),
                ("buffer", POINTER(c_ushort)),
                ("count", c_ulong)
        ]
PT_FAIDmaScanStart = tagPT_FAIDmaScanStart
LPT_FAIDmaScanStart = POINTER(tagPT_FAIDmaScanStart)


class tagPT_FAIDmaExStart(Structure):
    _fields_ = [("TrigSrc", c_ushort),#数据采集触发源: 内部触发 - 0    外部触发 - 1
                ("TrigMode", c_ushort),
                ("ClockSrc", c_ushort),
                ("TrigEdge", c_ushort),
                ("SRCType", c_ushort),
                ("TrigVol", c_float),
                ("CyclicMode",c_ushort),
                ("NumChans", c_ushort),
                ("StartChan", c_ushort),
                ("ulDelayCnt",c_ulong),
                ("count", c_ulong),
                ("SampleRate", c_ulong),
                ("GainList", POINTER(c_ushort)),
                ("CondList", POINTER(c_ushort)),
                ("LevelList", POINTER(TRIGLEVEL)),
                ("buffer0", POINTER(c_ushort)),
                ("buffer1", POINTER(c_ushort)),
                ("Pt1", POINTER(c_ushort)),
                ("Pt2", POINTER(c_ushort)),
                ("Pt3", POINTER(c_ushort))
        ]
PT_FAIDmaExStart = tagPT_FAIDmaExStart
LPT_FAIDmaExStart = POINTER(tagPT_FAIDmaExStart)


class tagPT_FAITransfer(Structure):
    _fields_ = [("ActiveBuf", c_ushort),
                ("DataBuffer", c_void_p),
                ("DataType", c_ushort),
                ("start", c_ulong),
                ("count", c_ulong),
                ("overrun", POINTER(c_ushort))
        ]
PT_FAITransfer = tagPT_FAITransfer
LPT_FAITransfer = POINTER(tagPT_FAITransfer)


class tagPT_FAICheck(Structure):
    _fields_ = [("ActiveBuf", POINTER(c_ushort)),
                ("stopped", POINTER(c_ushort)),
                ("retrieved", POINTER(c_ulong)),
                ("overrun", POINTER(c_ushort)),
                ("HalfReady", POINTER(c_ushort))
        ]
PT_FAICheck = tagPT_FAICheck
LPT_FAICheck = POINTER(tagPT_FAICheck)


class tagPT_FAOWaveFormStart(Structure):
    _fields_ = [("TrigSrc", c_ushort),
                ("SampleRate", c_uint),
                ("WaveCount", c_ulong),
                ("count", c_ulong),
                ("buffer", POINTER(c_ushort)),
                ("EnableChannel", c_ushort)
        ]
PT_FAOWaveFormStart = tagPT_FAOWaveFormStart
LPT_FAOWaveFormStart = POINTER(tagPT_FAOWaveFormStart)


class tagPT_FDITransfer(Structure):
    _fields_ = [("usEventType", c_ushort),
                ("ulRetData", POINTER(c_ulong))
        ]
PT_FDITransfer = tagPT_FDITransfer
LPT_FDITransfer = POINTER(tagPT_FDITransfer)


class tagPT_FAODmaStart(Structure):
    _fields_ = [("TrigSrc", c_ushort),
                ("SampleRate", c_uint),
                ("chan", c_ushort),
                ("buffer", POINTER(c_long)),
                ("count", c_ulong)
        ]
PT_FAODmaStart = tagPT_FAODmaStart
LPT_FAODmaStart  = POINTER(tagPT_FAODmaStart)


class tagPT_FAOScale(Structure):
    _fields_ = [("chan", c_ushort),
                ("count", c_ulong),
                ("VoltArray", POINTER(c_float)),
                ("BinArray", POINTER(c_ushort))
        ]
PT_FAOScale = tagPT_FAOScale
LPT_FAOScale  = POINTER(tagPT_FAOScale)


class tagPT_FAOCheck(Structure):
    _fields_ = [("ActiveBuf", POINTER(c_ushort)),
                ("stopped", POINTER(c_ushort)),
                ("CurrentCount", POINTER(c_ulong)),
                ("overrun", POINTER(c_ushort)),
                ("HalfReady", POINTER(c_ushort))
        ]
PT_FAOCheck = tagPT_FAOCheck
LPT_FAOCheck = POINTER(tagPT_FAOCheck)


class tagPT_FAOLoad(Structure):
    _fields_ = [("ActiveBuf", c_ushort),
                ("DataBuffer", POINTER(c_ushort)),
                ("start", c_ushort),
                ("count", c_ulong)
        ]
PT_FAOLoad = tagPT_FAOLoad
LPT_FAOLoad = POINTER(tagPT_FAOLoad)

#------------------Counter函数组-------------------#

class tagPT_CounterEventStart(Structure):
    _fields_ = [("counter", c_ushort),
                ("GateMode", c_ushort)
        ]
PT_CounterEventStart = tagPT_CounterEventStart
LPT_CounterEventStart = POINTER(tagPT_CounterEventStart)


class tagPT_CounterEventRead(Structure):
    _fields_ = [("counter", c_ushort),
                ("overflow", POINTER(c_ushort)),
                ("count", POINTER(c_ulong))
        ]
PT_CounterEventRead = tagPT_CounterEventRead
LPT_CounterEventRead = POINTER(tagPT_CounterEventRead)


class tagPT_CounterFreqStart(Structure):
    _fields_ = [("counter", c_ushort),
                ("GatePeriod", c_ushort),
                ("GateMode", c_ushort)
        ]
PT_CounterFreqStart = tagPT_CounterFreqStart
LPT_CounterFreqStart = POINTER(tagPT_CounterFreqStart)


class tagPT_CounterFreqRead(Structure):
    _fields_ = [("counter", c_ushort),
                ("freq", POINTER(c_float))
        ]
PT_CounterFreqRead = tagPT_CounterFreqRead
LPT_CounterFreqRead = POINTER(tagPT_CounterFreqRead)


class tagPT_CounterPulseStart(Structure):
    _fields_ = [("counter", c_ushort),
                ("period", c_float),
                ("UpCycle", c_float),
                ("GateMode", c_ushort)
        ]
PT_CounterPulseStart = tagPT_CounterPulseStart
LPT_CounterPulseStart = POINTER(tagPT_CounterPulseStart)


class tagPT_TimerCountSetting(Structure):
    _fields_ = [("counter", c_ushort),
                ("Count", c_ulong)
        ]
PT_TimerCountSetting = tagPT_TimerCountSetting
LPT_TimerCountSetting = POINTER(tagPT_TimerCountSetting)


class tagPT_CounterPWMSetting(Structure):
    _fields_ = [("Port", c_ushort),
                ("Period", c_float),
                ("HiPeriod", c_float),
                ("OutCount", c_ulong),
                ("GateMode", c_ushort)
        ]
PT_CounterPWMSetting = tagPT_CounterPWMSetting
LPT_CounterPWMSetting = POINTER(tagPT_CounterPWMSetting)


class tagPT_QCounterConfigSys(Structure):
    _fields_ = [("SysClock", c_ushort),
                ("TimeBase", c_ushort),
                ("TimeDivider", c_ushort),
                ("CascadeMode", c_ushort)
        ]
PT_QCounterConfigSys = tagPT_QCounterConfigSys
LPT_QCounterConfigSys = POINTER(tagPT_QCounterConfigSys)


class tagPT_QCounterStart(Structure):
    _fields_ = [("counter", c_ushort),
                ("InputMode", c_ushort)
        ]
PT_QCounterStart = tagPT_QCounterStart
LPT_QCounterStart = POINTER(tagPT_QCounterStart)


class tagPT_QCounterRead(Structure):
    _fields_ = [("counter", c_ushort),
                ("overflow", POINTER(c_ushort)),
                ("LoCount", POINTER(c_ulong)),
                ("HiCount", POINTER(c_ulong))
        ]
PT_QCounterRead = tagPT_QCounterRead
LPT_QCounterRead = POINTER(tagPT_QCounterRead)


class tagPT_CounterConfig(Structure):
    _fields_ = [("usCounter", c_ushort),
                ("usInitValue", c_ushort),
                ("usCountMode", c_ushort),
                ("usCountDirect", c_ushort),
                ("usCountEdge", c_ushort),
                ("usOutputEnable", c_ushort),
                ("usOutputMode", c_ushort),
                ("usClkSrc", c_ushort),
                ("usGateSrc", c_ushort),
                ("usGatePolarity", c_ushort)
        ]
PT_CounterConfig = tagPT_CounterConfig
LPT_CounterConfig = POINTER(tagPT_CounterConfig)


class tagPT_FreqOutStart(Structure):
    _fields_ = [("usChannel", c_ushort),
                ("usDivider", c_ushort),
                ("usFoutSrc", c_ushort)
        ]
PT_FreqOutStart = tagPT_FreqOutStart
LPT_FreqOutStart = POINTER(tagPT_FreqOutStart)


class tagPT_PWMStartRead(Structure):
    _fields_ = [("usChan", c_ushort),
                ("flHiperiod", POINTER(c_float)),
                ("flLowperiod", POINTER(c_float))
        ]
PT_PWMStartRead = tagPT_PWMStartRead
LPT_PWMStartRead = POINTER(tagPT_PWMStartRead)


#------------------Port I/O函数组-------------------#

class tagPT_ReadPortByte(Structure):
    _fields_ = [("port", c_ushort),
                ("ByteData", POINTER(c_ushort))
        ]
PT_ReadPortByte = tagPT_ReadPortByte
LPT_ReadPortByte = POINTER(tagPT_ReadPortByte)


class tagPT_WritePortByte(Structure):
    _fields_ = [("port", c_ushort),
                ("ByteData", c_ushort)
        ]
PT_WritePortByte = tagPT_WritePortByte
LPT_WritePortByte = POINTER(tagPT_WritePortByte)


class tagPT_ReadPortWord(Structure):
    _fields_ = [("port", c_ushort),
                ("WordData", POINTER(c_ushort))
        ]
PT_ReadPortWord = tagPT_ReadPortWord
LPT_ReadPortWord = POINTER(tagPT_ReadPortWord)


class tagPT_WritePortWord(Structure):
    _fields_ = [("port", c_ushort),
                ("WordData", c_ushort)
        ]
PT_WritePortWord = tagPT_WritePortWord
LPT_WritePortWord = POINTER(tagPT_WritePortWord)


class tagPT_ReadPortDword(Structure):
    _fields_ = [("port", c_ushort),
                ("DWordData", POINTER(c_ulong))
        ]
PT_DioReadPortDword = tagPT_ReadPortDword
LPT_ReadPortDword = POINTER(tagPT_ReadPortDword)


class tagPT_WritePortDword(Structure):
    _fields_ = [("port", c_ushort),
                ("DWordData", c_ulong)
        ]
PT_WritePortDword = tagPT_WritePortDword
LPT_WritePortDword = POINTER(tagPT_WritePortDword)


#------------------温度测量函数-------------------#

class tagPT_TCMuxRead(Structure):
    _fields_ = [("DasChan", c_ushort),
                ("DasGain", c_ushort),
                ("ExpChan", c_ushort),
                ("TCType", c_ushort),
                ("TempScale", c_ushort),
                ("temp", POINTER(c_float))
        ]
PT_TCMuxRead = tagPT_TCMuxRead
LPT_TCMuxRead = POINTER(tagPT_TCMuxRead)


#------------------Watchdog函数-------------------#

class tagPT_WatchdogStart(Structure):
    _fields_ = [("Reserve0", c_long),
                ("Reserve1", c_long)
        ]
PT_WatchdogStart = tagPT_WatchdogStart
LPT_WatchdogStart = POINTER(tagPT_WatchdogStart)










