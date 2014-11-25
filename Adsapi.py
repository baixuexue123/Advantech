#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'baixue'


from ctypes import *
from AdsStruct import *


ads_lib = windll.LoadLibrary('Adsapi32.dll')


#---------------------------------------------------------------------#
#                         Device functions                            #
#---------------------------------------------------------------------#

def DRV_DeviceOpen(DeviceNum):
    DriverHandle = c_long()
    ret = ads_lib.DRV_DeviceOpen(DeviceNum, byref(DriverHandle))
    check_return(ret)
    return DriverHandle


def DRV_DeviceClose(DriverHandle):
    ret = ads_lib.DRV_DeviceClose(byref(DriverHandle))
    check_return(ret)
    return None


def DRV_SelectDevice(hCaller, GetModule):
    '''
    Description:显示设备列表对话框，供用户选择已安装的设备，并得到选中设备的设备号
    Paramaters:
    hCaller--指定调用该对话框的父窗口句柄;
    GetModule == TRUE，且已经安装了模块，则这些模块将显示在树形列表中;
    GetModule == FALSE，或没有安装模块，则不会显示;
    DeviceNum--返回的是该模块(子设备)的编号和其主设备号的组合;
    Description--指向设备描述信息存储区的指针
    '''
    DeviceNum = c_ulong()
    Description = create_string_buffer(256)
    ret = ads_lib.DRV_SelectDevice(hCaller, GetModule, byref(DeviceNum), Description)
    check_return(ret)
    return (DeviceNum.value, repr(Description.value))


def DRV_DeviceGetFeatures(DriverHandle):
    '''
    Description:获取由设备句柄DriverHandle指向的设备的设备特性
    '''
    PT_DeviceGetFeatures = tagPT_DeviceGetFeatures()
    ret = ads_lib.DRV_DeviceGetFeatures(DriverHandle, byref(PT_DeviceGetFeatures))
    check_return(ret)
    return PT_DeviceGetFeatures


def DRV_DeviceGetNumOfList():
    '''
    Description:获取已安装设备列表中已安装设备的个数
    '''
    NumOfDevices = c_short()
    ret = ads_lib.DRV_DeviceGetNumOfList(byref(NumOfDevices))
    check_return(ret)
    return NumOfDevices.value


def DRV_DeviceGetList(MaxEntries):
    '''
    Description:返回已安装设备的设备列表
    '''
    DEVLIST = tagPT_DEVLIST()
    OutEntries = c_short()
    ret = ads_lib.DRV_DeviceGetList(byref(DEVLIST), MaxEntries, byref(OutEntries))
    check_return(ret)
    return (DEVLIST, OutEntries.value)


def DRV_DeviceGetSubList(DeviceNum, MaxEntries):
    '''
    Description:返回DeviceNum指定设备的子设备(模块)列表
    '''
    DEVLIST = tagPT_DEVLIST
    OutEntries = c_short()
    ret = ads_lib.DRV_DeviceGetSubList(DeviceNum, byref(DEVLIST), MaxEntries, byref(OutEntries))
    check_return(ret)
    return (DEVLIST, OutEntries)


def DRV_DeviceGetProperty(DriverHandle, nPropertyID):
    '''
    Description:在设备句柄 DriverHandle 指向的设备上,使用预定义的属性ID(nPropertyID)获取设备属性
    '''
    pBuffer = c_void_p()
    pLength = c_ulong()
    ret = ads_lib.DRV_DeviceGetProperty(DriverHandle, nPropertyID, pBuffer, byref(pLength))
    check_return(ret)
    return (pBuffer.value, pLength)


def DRV_DeviceSetProperty(DriverHandle, nPropertyID, Length):
    '''
    Description:在设备句柄DriverHandle指向的设备上，通过预定义的属性ID(nPropertyID)设置设备属性
    '''
    pBuffer = c_void_p()
    ret = ads_lib.DRV_DeviceSetProperty(DriverHandle, nPropertyID, pBuffer, Length)
    check_return(ret)
    return pBuffer.value

#---------------------------------------------------------------------#
#                            Event Functions                          #
#---------------------------------------------------------------------#

def DRV_EnableEvent(DriverHandle, EventType=0xf, Enabled=0, Count=512):
    '''
    Paramaters:
    EventType--具体查看相应采集卡手册
    Enabled--enable(1) or disable(0)
    Count--用中断模式进行数据采集时,硬件发生多少个中断才发送事件给用户
    '''
    PT_EnableEvent = tagPT_EnableEvent(EventType, Enabled, Count)
    ret = ads_lib.DRV_EnableEvent(DriverHandle, byref(PT_EnableEvent))
    check_return(ret)
    return None


def DRV_CheckEvent(DriverHandle, Milliseconds):
    PT_CheckEvent = tagPT_CheckEvent()
    eventType = c_ushort()
    PT_CheckEvent.EventType = pointer(eventType)
    PT_CheckEvent.Milliseconds = Milliseconds
    ret = ads_lib.DRV_CheckEvent(DriverHandle, byref(PT_CheckEvent))
    check_return(ret)
    return eventType.value


def DRV_EnableEventEx(DriverHandle, Filter, Pattern, Counter, Status):
    '''未完成'''
    PT_EnableEventEx = tagPT_EnableEventEx(Filter, Pattern, Counter, Status)
    ret = ads_lib.DRV_EnableEventEx(DriverHandle, byref(PT_EnableEventEx))
    check_return(ret)
    return None

#---------------------------------------------------------------------#
#                   Analog Input/Output Functions                     #
#---------------------------------------------------------------------#

#-----------------Analog Input(software triggering)-------------------#
def DRV_AIConfig(DriverHandle, chan, gain=0):
    PT_AIConfig = tagPT_AIConfig()
    PT_AIConfig.DasChan = chan
    PT_AIConfig.DasGain = gain
    ret = ads_lib.DRV_AIConfig(DriverHandle, byref(PT_AIConfig))
    check_return(ret)
    return None


def DRV_MAIConfig(DriverHandle, numChan, startChan, gains=None):
    PT_MAIConfig = tagPT_MAIConfig()
    PT_MAIConfig.NumChan = numChan
    PT_MAIConfig.StartChan = startChan
    GainArray = c_ushort*numChan
    GainArray= GainArray()
    if gains == None:
        gains = [0]*numChan
    for i, e in enumerate(gains):
        GainArray[i] = e
    PT_MAIConfig.GainArray = GainArray
    ret = ads_lib.DRV_MAIConfig(DriverHandle, byref(PT_MAIConfig))
    check_return(ret)
    return None


def DRV_AIGetConfig(DriverHandle):
    PT_AIGetConfig = tagPT_AIGetConfig()
    ret = ads_lib.DRV_AIGetConfig(DriverHandle, byref(PT_AIGetConfig))
    check_return(ret)
    return PT_AIGetConfig


def DRV_AIVoltageIn(DriverHandle, chan, gain=0, trigMode=0):
    PT_AIVoltageIn = tagPT_AIVoltageIn()
    PT_AIVoltageIn.chan = chan
    PT_AIVoltageIn.gain = gain
    # 0: internal trigger, 1: external trigger
    PT_AIVoltageIn.TrigMode = trigMode
    voltage = c_float()
    PT_AIVoltageIn.voltage = pointer(voltage)
    ret = ads_lib.DRV_AIVoltageIn(DriverHandle, byref(PT_AIVoltageIn))
    check_return(ret)
    return voltage.value

def DRV_MAIVoltageIn(DriverHandle, numChan, startChan, gains=None, trigMode=0):
    PT_MAIVoltageIn = tagPT_MAIVoltageIn()
    PT_MAIVoltageIn.NumChan = numChan
    PT_MAIVoltageIn.StartChan = startChan
    GainArray = c_ushort*numChan
    GainArray = GainArray()
    if gains == None:
        gains = [0 for i in range(numChan)]
    for i, e in enumerate(gains):
        GainArray[i] = e
    PT_MAIVoltageIn.GainArray = GainArray
    # 0: internal trigger, 1: external trigger
    PT_MAIVoltageIn.TrigMode = trigMode
    voltageArray = c_float*numChan
    # malloc buffer
    voltageArray = voltageArray()
    PT_MAIVoltageIn.VoltageArray = voltageArray
    ret = ads_lib.DRV_MAIVoltageIn(DriverHandle, byref(PT_MAIVoltageIn))
    check_return(ret)
    return [voltageArray[i] for i in range(numChan)]


def DRV_AIBinaryIn(DriverHandle, chan=0, TrigMode=0):
    PT_AIBinaryIn = tagPT_AIBinaryIn()
    PT_AIBinaryIn.chan = chan
    PT_AIBinaryIn.TrigMode = TrigMode
    ret = ads_lib.DRV_AIBinaryIn(byref(DriverHandle), byref(PT_AIBinaryIn))
    check_return(ret)
    return PT_AIBinaryIn.reading.value


def DRV_MAIBinaryIn(DriverHandle, NumChan=0, StartChan=0, TrigMode=0):
    PT_MAIBinaryIn = tagPT_MAIBinaryIn()
    PT_MAIBinaryIn.NumChan = NumChan
    PT_MAIBinaryIn.StartChan = StartChan
    PT_MAIBinaryIn.TrigMode = TrigMode
    ret = ads_lib.DRV_MAIBinaryIn(byref(DriverHandle), byref(PT_MAIBinaryIn))
    check_return(ret)
    return [i for i in PT_MAIBinaryIn.ReadingArray.contents]


def DRV_AIScale(DriverHandle, AIScale):
    PT_AIScale = tagPT_AIScale()
    PT_AIScale.reading = AIScale[0]
    PT_AIScale.MaxVolt = AIScale[1]
    PT_AIScale.MaxCount = AIScale[2]
    PT_AIScale.offset = AIScale[3]
    ret = ads_lib.DRV_AIScale(byref(DriverHandle), byref(PT_AIScale))
    check_return(ret)
    return PT_AIScale.voltage.value


def DRV_AIVoltageInExp(DriverHandle, AIVoltageInExp):
    PT_AIVoltageInExp = tagPT_AIVoltageInExp()
    PT_AIVoltageInExp.DasChan = AIVoltageInExp[0]
    PT_AIVoltageInExp.DasGain = AIVoltageInExp[1]
    PT_AIVoltageInExp.ExpChan = AIVoltageInExp[2]
    ret = ads_lib.DRV_AIVoltageInExp(byref(DriverHandle), byref(PT_AIVoltageInExp))
    check_return(ret)
    return PT_AIVoltageInExp.voltage.value


def DRV_MAIVoltageInExp(DriverHandle, MAIVoltageInExp):
    PT_MAIVoltageInExp = tagPT_MAIVoltageInExp()
    PT_MAIVoltageInExp.NumChan = MAIVoltageInExp[0]
    DasChanArray = c_ushort*len(MAIVoltageInExp[1])
    for i, e in enumerate(MAIVoltageInExp[1]):
        DasChanArray[i] = e
    PT_MAIVoltageInExp.DasChanArray = pointer(DasChanArray)
    DasGainArray = c_ushort*len(MAIVoltageInExp[2])
    for i, e in enumerate(MAIVoltageInExp[2]):
        DasGainArray[i] = e
    PT_MAIVoltageInExp.DasGainArray = pointer(DasGainArray)
    ExpChanArray = c_ushort*len(MAIVoltageInExp[3])
    for i, e in enumerate(MAIVoltageInExp[3]):
        ExpChanArray[i] = e
    PT_MAIVoltageInExp.ExpChanArray = pointer(ExpChanArray)
    ret = ads_lib.DRV_MAIVoltageInExp(DriverHandle, byref(PT_MAIVoltageInExp))
    check_return(ret)
    return [i for i in PT_MAIVoltageInExp.VoltageArray.contents]

#---------Analog Input--High-speed AI Functions(interrupt transfer)---------#
def AllocateDataBuffer(count):
    usINTBuf = c_ushort*count
    usINTBuf = usINTBuf()
    pUserBuf = c_float*count
    pUserBuf = pUserBuf()
    return (usINTBuf, pUserBuf)


def GetBufferData(UserBuf, count):
    return [UserBuf[i] for i in range(count)]


def WaitFAIEvent(DriverHandle, timeout):
    eventType = DRV_CheckEvent(DriverHandle, timeout)
    if eventType > 10240:
        #AO
        pass
    else:
        #AI
        AI_OverRun = (eventType^0x8 == 0x8)
        AI_Terminated = (eventType^0x4 == 0x4)
        if eventType^0x2 == 0x2:
            FAICheck = DRV_FAICheck(DriverHandle)
            HalfReady = FAICheck[4]
            AI_BufferHalfReady = (HalfReady==1)
            AI_BufferFullReady = (HalfReady==2)
    return (AI_Terminated, AI_BufferHalfReady, AI_BufferFullReady, AI_OverRun)


def SplitArray1DTo2D(data, numChan):
    '''
    将采集到的数据按通道分配成2D Array
    '''
    return[data[i::numChan] for i in range(numChan)]



def DRV_FAIIntStart(DriverHandle, SampleRate, chan, gain, count, usINTBuf, TrigSrc=0, cyclic=0, IntrCount=1):
    '''
    Description:单通道FAI
    Paramaters:
    count--number of samples:该值必须被设置为大于零的偶数,或如果使用FIFO,还必须为FIFO一半大小的整数倍
    TrigSrc--0: internal trigger; 1: external trigger
    cyclic--0: non-cyclic mode; 1: cyclic-mode
    IntrCount--设置多少次A/D数据转换产生一个中断,当没有或不使用FIFO时,该值必须设为1;/
    当使用FIFO时,该值必须是FIFO大小的一半
    '''
    PT_FAIIntStart = tagPT_FAIIntStart()
    PT_FAIIntStart.TrigSrc = TrigSrc
    PT_FAIIntStart.SampleRate = SampleRate
    PT_FAIIntStart.chan = chan
    PT_FAIIntStart.gain = gain
    #buffer--给驱动的缓冲区
    PT_FAIIntStart.buffer = usINTBuf
    PT_FAIIntStart.count = count
    PT_FAIIntStart.cyclic = cyclic
    PT_FAIIntStart.IntrCount = IntrCount
    ret = ads_lib.DRV_FAIIntStart(DriverHandle, byref(PT_FAIIntStart))
    check_return(ret)
    return None


def DRV_FAIIntScanStart(DriverHandle, SampleRate, NumChans, StartChan, count, pusINTBuf, GainList=None,TrigSrc=0, cyclic=0, IntrCount=1):
    '''
    Description:多通道FAI
    '''
    PT_FAIIntScanStart = tagPT_FAIIntScanStart()
    PT_FAIIntScanStart.TrigSrc = TrigSrc
    PT_FAIIntScanStart.SampleRate = SampleRate
    PT_FAIIntScanStart.NumChans = NumChans
    PT_FAIIntScanStart.StartChan = StartChan
    GainList = c_ushort*NumChans
    GainList= GainList()
    if GainList == None:
        GainList = [0]*NumChans
    for i, e in enumerate(GainList):
        GainArray[i] = e
    PT_MAIConfig.GainList = GainList
    PT_FAIIntScanStart.buffer = pusINTBuf
    PT_FAIIntScanStart.count = count
    PT_FAIIntScanStart.cyclic = cyclic
    PT_FAIIntScanStart.IntrCount = IntrCount
    ret = ads_lib.DRV_FAIIntScanStart(DriverHandle, byref(PT_FAIIntScanStart))
    check_return(ret)
    return None

def DRV_FAITerminate(DriverHandle):
    ret = ads_lib.DRV_FAITerminate(DriverHandle)
    check_return(ret)
    return None


def DRV_FAITransfer(DriverHandle, UserBuf, count, start=0, DataType=1):
    '''
    Description:
    Paramaters:
    ActiveBuf--0，1  保留，目前全部置0
    DataBuffer-- 用户buffer 其大小不应小于2*count(当DataType为Unsigned short)
    或不小于4*count(当DataType为Float)
    DataType--0:原始数据(ushort),1:浮点型(float)
    count--为采样个数
    start--(0 ~ N-1), N是启动FAI时, 分配采样buffer的采样个数.Start+count < N
    overrun--0:无溢出; 1:溢出
    当采样buffer前/后半数据未被及时取走时,溢出标志位会被置位,缓冲区的数据会被新的数值覆盖
    '''
    PT_FAITransfer = tagPT_FAITransfer()
    PT_FAITransfer.ActiveBuf = 0
    PT_FAITransfer.DataBuffer = cast(UserBuf, c_void_p)
    PT_FAITransfer.DataType = DataType
    PT_FAITransfer.start = start
    PT_FAITransfer.count = count
    overrun = c_ushort()
    PT_FAITransfer.overrun = pointer(overrun)
    ret = ads_lib.DRV_FAITransfer(DriverHandle, byref(PT_FAITransfer))
    check_return(ret)
    return overrun.value
        

def DRV_FAICheck(DriverHandle):
    '''
    Description:
    Paramaters:
    ActiveBuf--reserved(0)
    stopped-- returned status: 1: complete, 0: imcomplete
    retrieved--采样buffer中已转换的数据个数
    overrun--0:未覆盖;1:已覆盖
    HalfReady--0:未准备好;1:前半buffer准备好;2:后半buffer准备好
    '''
    PT_FAICheck = tagPT_FAICheck()
    ActiveBuf = c_ushort()
    PT_FAICheck.ActiveBuf =pointer(ActiveBuf)
    stopped = c_ushort()
    PT_FAICheck.stopped = pointer(stopped)
    retrieved = c_ulong()
    PT_FAICheck.retrieved = pointer(retrieved)
    overrun = c_ushort()
    PT_FAICheck.overrun = pointer(overrun)
    HalfReady = c_ushort()
    PT_FAICheck.HalfReady = pointer(HalfReady)
    ret = ads_lib.DRV_FAICheck(DriverHandle, byref(PT_FAICheck))
    check_return(ret)
    return(ActiveBuf.value, stopped.value, retrieved.value, overrun.value, HalfReady.value)

def DRV_ClearOverrun(DriverHandle):
    '''
    Description:清除FAI溢出标志位
    '''
    ret = ads_lib.DRV_ClearOverrun(DriverHandle)
    check_return(ret)
    return None


def DRV_FAIStop(DriverHandle):
    '''
    手册中没有这个函数
    '''
    ret = ads_lib.DRV_FAIStop(DriverHandle)
    check_return(ret)
    return None


def DRV_GetFIFOSize(DriverHandle):
    lSize = c_long()
    ret = ads_lib.DRV_GetFIFOSize(DriverHandle, byref(lSize))
    check_return(ret)
    return lSize.value


#------------------Analog Input--High-speed AI Functions(DMA triggering)-------------------#
def DRV_AllocateDMABuffer(DriverHandle, RequestBufSize, CyclicMode=1):
    '''
    Description:
    Paramaters:
    RequestBufSize--指定所需要的内存大小
    RequestBufSize 和用户将要转换的数据量有关,
    由于每个数据在DMA传输时将占用两个字节,所以该参数的大小就是欲转换的数据量的两倍.
    ActualBufSize--实际分配缓冲区大小
    Buffer--缓冲区地址
    '''
    PT_AllocateDMABuffer = tagPT_AllocateDMABuffer()
    PT_AllocateDMABuffer.CyclicMode = CyclicMode
    PT_AllocateDMABuffer.RequestBufSize = RequestBufSize
    ActualBufSize = c_ulong()
    buf = c_long()
    PT_AllocateDMABuffer.ActualBufSize = pointer(ActualBufSize)
    PT_AllocateDMABuffer.buffer = pointer(buf)
    ret = ads_lib.DRV_AllocateDMABuffer(DriverHandle, byref(PT_AllocateDMABuffer))
    check_return(ret)
    return (ActualBufSize.value, buf)


def DRV_FreeDMABuffer(DriverHandle, buf):
    ret = ads_lib.DRV_FreeDMABuffer(DriverHandle, buf)
    check_return(ret)
    return None


def DRV_FAIDmaStart(DriverHandle, SampleRate, chan, gain, buf, count, TrigSrc=0):
    '''
    Description:DMA单通道
    Paramaters:
    '''
    PT_FAIDmaStart = tagPT_FAIDmaStart()
    PT_FAIDmaStart.TrigSrc = TrigSrc
    PT_FAIDmaStart.SampleRate = SampleRate
    PT_FAIDmaStart.chan = chan
    PT_FAIDmaStart.gain = gain
    PT_FAIDmaStart.buffer = buf
    PT_FAIDmaStart.count = count
    ret = ads_lib.DRV_FAIDmaStart(DriverHandle, byref(PT_FAIDmaStart))
    check_return(ret)
    return None


def DRV_FAIDmaScanStart(DriverHandle, SampleRate, NumChans, StartChan, buf, count, GainList=None, TrigSrc=0):
    '''
    Description:DMA多通道
    Paramaters:
    '''
    PT_FAIDmaScanStart = tagPT_FAIDmaScanStart()
    PT_FAIDmaScanStart.TrigSrc = TrigSrc
    PT_FAIDmaScanStart.SampleRate = SampleRate
    PT_FAIDmaScanStart.NumChans = NumChans
    PT_FAIDmaScanStart.StartChan = StartChan
    GainList = c_ushort*NumChans
    GainList= GainList()
    if GainList == None:
        GainList = [0]*NumChans
    for i, e in enumerate(GainList):
        GainArray[i] = e
    PT_FAIDmaScanStart.GainList = GainList
    PT_FAIDmaScanStart.buffer = buf
    PT_FAIDmaScanStart.count = count
    ret = ads_lib.DRV_FAIDmaScanStart(DriverHandle, byref(PT_FAIDmaScanStart))
    check_return(ret)
    return None


def DRV_FAIDmaExStart(DriverHandle):
    pass


#------------------Analog Output(software triggering)-------------------#
def DRV_AOConfig(DriverHandle, chan, MaxValue, MinValue, RefSrc=0):
    '''
    RefSrc--0:internal;1:external
    '''
    PT_AOConfig = tagPT_AOConfig()
    PT_AOConfig.chan = chan
    PT_AOConfig.RefSrc = RefSrc
    PT_AOConfig.MaxValue = MaxValue
    PT_AOConfig.MinValue = MinValue
    ret = ads_lib.DRV_AOConfig(DriverHandle, byref(PT_AOConfig))
    check_return(ret)
    return None


def DRV_AOVoltageOut(DriverHandle, chan, OutputValue):
    PT_AOVoltageOut = tagPT_AOVoltageOut()
    PT_AOVoltageOut.chan = chan
    PT_AOVoltageOut.OutputValue = OutputValue
    ret = ads_lib.DRV_AOVoltage(DriverHandle, byref(PT_AOVoltageOut))
    check_return(ret)
    return None


def DRV_AOCurrentOut(DriverHandle, chan, OutputValue):
    PT_AOCurrentOut = tagPT_AOCurrentOut()
    PT_AOCurrentOut.chan = chan
    PT_AOCurrentOut.OutputValue = OutputValue
    ret = ads_lib.DRV_AOCurrentOut(DriverHandle, byref(PT_AOCurrentOut))
    check_return(ret)
    return None


def DRV_AOBinaryOut(DriverHandle, chan, BinData):
    PT_AOBinaryOut = tagPT_AOCurrentOut()
    PT_AOBinaryOut.chan = chan
    PT_AOBinaryOut.BinData = BinData
    ret = ads_lib.DRV_AOBinaryOut(DriverHandle, byref(PT_AOBinaryOut))
    check_return(ret)
    return None


def DRV_AOScale(DriverHandle, chan , OutputValue):
    PT_AOScale = tagPT_AOScale()
    PT_AOScale.chan = chan
    PT_AOScale.OutputValue = OutputValue
    BinData = c_ushort()
    PT_AOScale.BinData = pointer(BinData)
    ret = ads_lib.DRV_AOScale(DriverHandle, byref(PT_AOScale))
    check_return(ret)
    return None


def DRV_EnableSyncAO(DriverHandle, Enable):
    '''
    使能或解除所有AO通道同步输出功能
    '''
    ret = ads_lib.DRV_EnableSyncAO(DriverHandle, Enable)
    check_return(ret)
    return None


def DRV_WriteSyncAO(DriverHandle):
    '''
    使所有AO通道依据之前的设置同步输出
    '''
    ret = ads_lib.DRV_WriteSyncAO(DriverHandle)
    check_return(ret)
    return None

#------------------Analog Output--High-speed AO Functions(DMA)-------------------#
def DRV_FAODmaStart(DriverHandle):
    pass


def DRV_FAODmaExStart(DriverHandle):
    pass


def DRV_FAOWaveFormStart(DriverHandle):
    pass

def DRV_FAOLoad(DriverHandle):
    pass


def DRV_FAOCheck(DriverHandle):
    pass


def DRV_FAOCheckEx(DriverHandle):
    pass


def DRV_FAOScale(DriverHandle):
    pass

def DRV_FAOStop(DriverHandle):
    pass

def DRV_FAOTerminate(DriverHandle):
    pass

#---------------------------------------------------------------------#
#                   Digital Input/Output Functions                    #
#---------------------------------------------------------------------#

def DRV_DioGetConfig(DriverHandle):
    pass


def DRV_DioSetPortMode(DriverHandle):
    pass


def DRV_ClearFlag(DriverHandle):
    pass
#------------------Digital Input Functions(software triggering)-------------------#
def AdxDioReadDiPorts(DriverHandle, dwPortStart, dwPortCount):
    '''
    未测--pBuffer的设置有问题
    '''
    pBuffer = c_byte()
    ret = ads_lib.AdxDioReadDiPorts(DriverHandle, dwPortStart, dwPortCount, byref(pBuffer))
    check_return(ret)
    return pBuffer.value


def DRV_DioReadPortByte(DriverHandle, port=0):
    PT_DioReadPortByte = tagPT_DioReadPortByte()
    PT_DioReadPortByte.port = port
    byteData = c_ushort()
    PT_DioReadPortByte.value = pointer(byteData)
    ret = ads_lib. DRV_DioReadPortByte(DriverHandle, byref(PT_DioReadPortByte))
    check_return(ret)
    return byteData.value


def DRV_DioReadBit(DriverHandle, port=0, bit=0):
    PT_DioReadBit = tagPT_DioReadBit()
    PT_DioReadBit.port = port
    PT_DioReadBit.bit = bit
    state = c_ushort()  # 0 or 1
    PT_DioReadBit.state = pointer(state)
    ret = ads_lib.DRV_DioReadBit(DriverHandle, byref(PT_DioReadBit))
    check_return(ret)
    return state.value


def DRV_DioReadPortWord(DriverHandle, port=0):
    PT_DioReadPortWord = tagPT_DioReadPortWord()
    PT_DioReadPortWord.port = port
    wordData = c_ushort()
    PT_DioReadPortWord.value = pointer(wordData)
    ValidChannelMask = c_ushort()
    PT_DioReadPortWord.ValidChannelMask = pointer(ValidChannelMask)
    ret = ads_lib.DRV_DioReadPortWord(DriverHandle, byref(PT_DioReadPortWord))
    check_return(ret)
    return (wordData.value, ValidChannelMask.value)


def DRV_DioReadPortDword(DriverHandle, port=0):
    PT_DioReadPortDWord = tagPT_DioReadPortDWord()
    PT_DioReadPortDWord.port = port
    DwordData = c_ulong()
    PT_DioReadPortDWord.value = pointer(DwordData)
    ValidChannelMask = c_ulong()
    PT_DioReadPortDWord.ValidChannelMask = pointer(ValidChannelMask)
    ret = ads_lib.DRV_DioReadPortDword(DriverHandle, byref(PT_DioReadPortDWord))
    check_return(ret)
    return (DwordData.value, ValidChannelMask.value)


#------------------Digital Input Functions(interrupt transfer)-------------------#
def AdxDioDisableEvent(DriverHandle, dwEventID):
    ret = ads_lib.AdxDioDisableEvent(DriverHandle, dwEventID)
    check_return(ret)
    return None


def AdxDioGetLatestEventDiPortsState(DriverHandle, dwEventID, dwLength):
    pBuffer = c_char_p()
    ret = ads_lib.AdxDioGetLatestEventDiPortsState(DriverHandle, dwEventID, pBuffer, dwLength)
    check_return(ret)
    return None


def AdxDioEnableEventAndSpecifyDiPorts(DriverHandle, dwEventID, dwScanStart, dwScanCount):
    ret = ads_lib.AdxDioEnableEventAndSpecifyDiPorts(DriverHandle, dwEventID, dwScanStart, dwScanCount)
    check_return(ret)
    return None


def DRV_FDITransfer(DriverHandle):
    pass


#------------------Digital Input Functions(DMA Triggering)-------------------#
def DRV_FDIStart(DriverHandle):
    pass


def DRV_FDIStop(DriverHandle):
    pass


def DRV_FDICheck(DriverHandle):
    pass

#------------------Digital Onput Functions(software triggering)-------------------#
def AdxDioGetCurrentDoPortsState(DriverHandle, dwPortStart, dwPortCount):
    '''
    未测--pBuffer的设置有问题
    '''
    pBuffer = c_byte()
    ret = ads_lib.AdxDioGetCurrentDoPortsState(DriverHandle, dwPortStart, dwPortCount, byref(pBuffer))
    check_return(ret)
    return pBuffer.value


def AdxDioWriteDoPorts(DriverHandle, dwPortStart, dwPortCount):
    '''
    未测--pBuffer的设置有问题
    '''
    pBuffer = c_byte()
    ret = ads_lib.AdxDioWriteDoPorts(DriverHandle, dwPortStart, dwPortCount, byref(pBuffer))
    check_return(ret)
    return None


def DRV_DioWriteBit(DriverHandle, port=0, bit=0, state=0):
    PT_DioWriteBit = tagPT_DioWriteBit(port, bit, state)
    ret = ads_lib.DRV_DioWriteBit(DriverHandle, byref(PT_DioWriteBit))
    check_return(ret)
    return None


def DRV_DioWritePortByte(DriverHandle, port=0, mask=0, state=0):
    PT_DioWritePortByte = tagPT_DioWritePortByte(port, mask, state)
    ret = ads_lib.DRV_DioWritePortByte(DriverHandle, byref(PT_DioWritePortByte))
    check_return(ret)
    return None


def DRV_DioWritePortWord(DriverHandle, port=0, mask=0, state=0):
    PT_DioWritePortWord = tagPT_DioWritePortWord(port, mask, state)
    ret = ads_lib.DRV_DioWritePortWord(DriverHandle, byref(PT_DioWritePortWord))
    check_return(ret)
    return None


def DRV_DioWritePortDword(DriverHandle, port=0, mask=0, state=0):
    PT_DioWritePortDWord = tagPT_DioWritePortDWord(port, mask, state)
    ret = ads_lib.DRV_DioWritePortDword(DriverHandle, byref(PT_DioWritePortDWord))
    check_return(ret)
    return None


def DRV_DioGetCurrentDOBit(DriverHandle, port=0, bit=0):
    PT_DioGetCurrentDOBit = tagPT_DioGetCurrentDOBit()
    PT_DioGetCurrentDOBit.port = port
    PT_DioGetCurrentDOBit.bit = bit
    state = c_ushort()
    PT_DioGetCurrentDOBit.state = pointer(state)
    ret = ads_lib.DRV_DioGetCurrentDOBit(DriverHandle, byref(PT_DioGetCurrentDOBit))
    check_return(ret)
    return state.value


def DRV_DioGetCurrentDOByte(DriverHandle, port=0):
    PT_DioGetCurrentDOByte = tagPT_DioGetCurrentDOByte()
    PT_DioGetCurrentDOByte.port = port
    byteData = c_byte()
    PT_DioGetCurrentDOByte.value = pointer(byteData)
    ret = ads_lib.DRV_DioGetCurrentDOByte(DriverHandle, byref(PT_DioGetCurrentDOByte))
    check_return(ret)
    return byteData.value


def DRV_DioGetCurrentDOWord(DriverHandle, port=0):
    PT_DioGetCurrentDOWord = tagPT_DioGetCurrentDOWord()
    PT_DioGetCurrentDOWord.port = port
    wordData = c_ushort()
    PT_DioGetCurrentDOWord.value = pointer(wordData)
    ValidChannelMask = c_ushort()
    PT_DioGetCurrentDOWord.ValidChannelMask = pointer(PT_DioGetCurrentDOWord)
    ret = ads_lib.DRV_DioGetCurrentDOWord(DriverHandle, byref(PT_DioGetCurrentDOWord))
    check_return(ret)
    return (wordData.value, ValidChannelMask.value)


def DRV_DioGetCurrentDODword(DriverHandle, port=0):
    PT_DioGetCurrentDODword = tagPT_DioGetCurrentDODword()
    PT_DioGetCurrentDODword.port = port
    DwordData = c_ulong()
    PT_DioGetCurrentDODword.value = pointer(DwordData)
    ValidChannelMask = c_ulong()
    PT_DioGetCurrentDODword.ValidChannelMask = pointer(ValidChannelMask)
    ret = ads_lib.DRV_DioGetCurrentDODword(DriverHandle, byref(PT_DioGetCurrentDODword))
    check_return(ret)
    return (DwordData.value, ValidChannelMask.value)

#------------------Digital Output Functions(DMA Triggering)-------------------#
def DRV_FDOStart(DriverHandle):
    pass


def DRV_FDOCheck(DriverHandle):
    pass


def DRV_FDOStop(DriverHandle):
    pass

#---------------------------------------------------------------------#
#                         Port I/O Functions                          #
#---------------------------------------------------------------------#

def DRV_ReadPortByte(DriverHandle, port):
    PT_ReadPortByte = tagPT_ReadPortByte()
    PT_ReadPortByte.port = port
    byteData = c_byte()
    PT_ReadPortByte.ByteData = pointer(byteData)
    ret = ads_lib.DRV_ReadPortByte(DriverHandle, byref(PT_ReadPortByte))
    check_return(ret)
    return byteData.value


def DRV_WritePortByte(DriverHandle, port, byteData):
    PT_WritePortByte = tagPT_WritePortByte()
    PT_WritePortByte.port = port
    PT_WritePortByte.ByteData = byteData
    ret = ads_lib.DRV_WritePortByte(DriverHandle, byref(PT_WritePortByte))
    check_return(ret)
    return None


def DRV_ReadPortWord(DriverHandle, port):
    PT_ReadPortWord = tagPT_ReadPortWord()
    PT_ReadPortWord.port = port
    wordData = c_ushort()
    PT_ReadPortWord.WordData = pointer(wordData)
    ret = ads_lib.DRV_ReadPortWord(DriverHandle, byref(PT_ReadPortWord))
    check_return(ret)
    return wordData.value


def DRV_WritePortWord(DriverHandle, port, wordData):
    PT_WritePortWord = tagPT_WritePortWord()
    PT_WritePortWord.port = port
    PT_WritePortWord.WordData = wordData
    ret = ads_lib.DRV_WritePortWord(DriverHandle, byref(PT_WritePortWord))
    check_return(ret)
    return None


def DRV_ReadPortDword(DriverHandle, port):
    PT_ReadPortDword = tagPT_ReadPortDword()
    PT_ReadPortDword.port = port
    DwordData = c_ulong()
    PT_ReadPortDword.DWordData = pointer(DwordData)
    ret = ads_lib.DRV_ReadPortDword(DriverHandle, byref(PT_ReadPortDword))
    check_return(ret)
    return DwordData.value


def DRV_WritePortDword(DriverHandle, port, DwordData):
    PT_WritePortDword = tagPT_WritePortDword()
    PT_WritePortDword.port = port
    PT_WritePortDword.WordData = DwordData
    ret = ads_lib.DRV_WritePortDword(DriverHandle, byref(PT_WritePortDword))
    check_return(ret)
    return None

#---------------------------------------------------------------------#
#                          Countor Functions                          #
#---------------------------------------------------------------------#

def DRV_CounterReset():
    pass


def DRV_DICounterReset():
    pass


#--------------Countor Functions(Event)---------------#
def DRV_CounterEventStart():
    pass


def DRV_CounterEventRead():
    pass


def DRV_CounterConfig():
    pass


#--------------Countor Functions(interrupt triggering)---------------#
def DRV_TimerCountSetting():
    pass


#--------------Countor Functions(QCounter)---------------#
def DRV_QCounterConfig():
    pass


def DRV_QCounterConfigSys():
    pass


def DRV_QCounterStart():
    pass


def DRV_QCounterRead():
    pass


#--------------Countor Functions(frequency measurement function)---------------#
def DRV_CounterFreqStart():
    pass


def DRV_CounterFreqRead():
    pass


def DRV_PWMStartRead():
    pass


#--------------Countor Functions(PWM Out)---------------#
def DRV_CounterPulseStart():
    pass


def DRV_CounterPWMSetting():
    pass


def DRV_CounterPWMEnable():
    pass


def DRV_FreqOutStart():
    pass


def DRV_FreqOutReset():
    pass


#---------------------------------------------------------------------#
#                            Temperature                              #
#---------------------------------------------------------------------#

def DRV_TCMuxRead():
    pass

#---------------------------------------------------------------------#
#                    Hardware Read/Write Functions                    #
#---------------------------------------------------------------------#

def AdxPrivateHWRegionRead():
    pass


def AdxPrivateHWRegionWrite():
    pass

#---------------------------------------------------------------------#
#                          Watchdog Functions                         #
#---------------------------------------------------------------------#

def DRV_WatchdogStart():
    pass


def DRV_WatchdogFeed():
    pass


def DRV_WatchdogStop():
    pass


#---------------------------------------------------------------------#
#                               Others                                #
#---------------------------------------------------------------------#

ErrorMsg = ("Fail to Get Error Message",
            "Invalid Error Code",
            "Configuration data lost")

def DRV_GetErrorMessage(errcode):
    P_ErrMsg = create_string_buffer(128)
    ads_lib.DRV_GetErrorMessage(errcode, P_ErrMsg)
    ret = P_ErrMsg.value
    try:
        errcde = int(ret)
        if errcde in (1, 2, 3):
            return ErrorMsg[ret-1]
    except ValueError:
        return ret

##def DRV_GetAddress():
##    #此函数用于在Visual Basic语言中得到一个指针（lpVoid）所指向的变量的地址值，如数组的首地址等
##    ret = ads_lib.DRV_GetAddress(c_void_p)
##    return ret
    
#---------------------------------------------------------------------#
#                            Exception                                #
#---------------------------------------------------------------------#

class Ads_Error(Exception):
    def __init__(self, errcode):
        super(Ads_Error, self).__init__()
        self.errcode = errcode

    def __str__(self):
        return "Advantech:%d--%s" % (self.errcode, DRV_GetErrorMessage(self.errcode))


def check_return(errcode):
    if errcode != 0:
        raise Ads_Error(errcode)
