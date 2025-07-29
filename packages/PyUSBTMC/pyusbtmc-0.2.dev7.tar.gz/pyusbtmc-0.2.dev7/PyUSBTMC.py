#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
PyUSBTMC:python module to handle USB-TMC(Test and Measurement class)　devices.
It requires pyusb module and libusb or openusb libraries.
(C) 2012-2015, Noboru Yamamot, Accl. Lab, KEK, JAPAN
contact: noboru.yamamoto_at_kek.jp
"""
import struct,array,time,sys
from typing import Union, List

# from usbtmc.h
# Size of driver internal IO buffer. Must be multiple of 4 and at least as
# large as wMaxPacketSize (which is usually 512 bytes). 
USBTMC_SIZE_DEFAULT   = 4096
#USBTMC_SIZE_IOBUFFER = 32768*10
USBTMC_SIZE_IOBUFFER  = 64*1024
USBTMC_DEFAULT_TIMEOUT = 3000 #msec
USBTMC_MAX_READS_TO_CLEAR_BULK_IN = 100
USBTMC_HEADER_SIZE=12

#import usb
from usb import USBError
#from usb.core import *
import usb.core
usb.core.Device.default_timeout=USBTMC_DEFAULT_TIMEOUT

#from usb.util import *
from usb.util import dispose_resources,build_request_type
from usb.util import CTRL_IN, CTRL_OUT, CTRL_RECIPIENT_DEVICE, CTRL_RECIPIENT_ENDPOINT, CTRL_RECIPIENT_INTERFACE, CTRL_RECIPIENT_OTHER
from usb.util import CTRL_TYPE_CLASS, CTRL_TYPE_RESERVED, CTRL_TYPE_STANDARD, CTRL_TYPE_VENDOR
from usb.util import DESC_TYPE_CONFIG, DESC_TYPE_DEVICE, DESC_TYPE_ENDPOINT, DESC_TYPE_INTERFACE, DESC_TYPE_STRING
from usb.util import ENDPOINT_IN, ENDPOINT_OUT, ENDPOINT_TYPE_BULK, ENDPOINT_TYPE_CTRL, ENDPOINT_TYPE_INTR, ENDPOINT_TYPE_ISO
import usb.control as usbctrl

#from lsusb import show_endpoint

import logging
logging.getLogger().setLevel(logging.INFO)
usbtmclogger=logging.getLogger("PyUSBTMC")
usbtmclogger.setLevel(logging.INFO)

# from  USB-TMC table2
class USBTMC_MsgID:
    # 0 : Reserved
    DEV_DEP_MSG_OUT        = 1
    REQUEST_DEV_DEP_MSG_IN = 2
    DEV_DEP_MSG_IN         = 2
    #3-125 Reserved for USBTMC use.
    VENDOR_SPECIFIC_OUT    = 126
    REQUEST_VENDOR_SPECIFIC_IN = 127
    VENDOR_SPECIFIC_IN     = 127
    # 128-191 Reserved for USBTMC subclass use.
    TRIGGER                = 128 # for USB488
    # 192-255  Reserved for VISA specification use.
    
Mandatory_LANGID=0x0409 # English,United State

#
USBTMC_bInterfaceClass   =254 #0xfe
USBTMC_bInterfaceSubClass=3 # usbtmc
USBTMC_bInterfaceProtocol=0 
USB488_bInterfaceSubClass=1


#USB2.0 Specification
# #8.1 Byte/Bit Ordering
# Bits are sent out onto the bus least-significant bit (LSb) first, 
# followed by the next LSb, through to the mostsignificant
# bit (MSb) last. 
# Multiple byte fields in standard descriptors, requests, and 
# responses are interpreted as and moved over the
# bus in little-endian order, i.e., LSB to MSB.
#
# NY memo:
# it means 'use "<" in pack/unpack of struct module.'

def find_tmc_devices(**args):
    """
    get the list of USB devices which belongs USBTMC Class.
    BaseInterface class/Sub class/Protcol=0xfe/0x03/(0x00 for TMC, 0x01 for USB488)
    This function returns a list of usb device objects but not usbtmc object.
    User must create USBTMC_device object or USB488_device object from the return 
    value from this function.  The user can use USBTMC_device.find_all() and
    USB488_device.find_all().
    """
    def is_usbtmc(d):
        """
        check if device:d is USBTMC device or not.
        """
        for cfg in d:
            # USBTMC_bInterfaceClass = 0xfe, USBTMC_bInterfaceSubClass = 3
            # strictry speaking, TMC or USB488 devices will be selected
            if (usb.util.find_descriptor(cfg, bInterfaceClass=0xfe, bInterfaceSubClass=3) != None):
                return True
        return False

    devs=usb.core.find(find_all=True, custom_match=is_usbtmc, **args) # now returns generator. Not a list.
    return devs # a list of usb.core.Device

# Table11 Bulk-IN protocol error
class USBTMCError(USBError):
    pass

class USBTMC_BulkInError(USBTMCError):
    pass

# 
class usbtmc_dev_capabilities:
    def __init__(self):
        self.interface_capabilities=""
        self.device_capabilities=""
        self.usb488_interface_capabilities=""
        self.usb488_device_capabilities=""

class usbtmc_attribute:
    def __init__(self):
        self.attribute=0
        self.value=0
        
# USBTMC status values/USBTMC Table 16
class USBTMC_Status:
    """
     USBTMC status values/USBTMC Table 16
    """
    SUCCESS = 0x01
    PENDING = 0x02
    FAILED  = 0x80
    TRANSFER_NOT_IN_PROGRESS = 0x81
    SPLIT_NOT_IN_PROGRESS    = 0x82
    SPLIT_IN_PROGRESS        = 0x83
    # only fo USB488
    INTERRUPT_IN_BUSY       = 0x20
    
    @classmethod
    def msg(cls,i):
        if (i == cls.SUCCESS):
            return "Success"
        elif (i == cls.PENDING):
            return "Pending"
        elif (i == cls.FAILED):
            return "Failed"
        elif (i == cls.TRANSFER_NOT_IN_PROGRESS):
            return "Transfer not in progress"
        elif (i == cls.SPLIT_NOT_IN_PROGRESS):
            return "Split not in progress"
        elif (i == cls.SPLIT_IN_PROGRESS):
            return "Split in progress"
        return "Reserved"
#
class IEEE488_Status_Byte_Reg:
    def __init__(self,byte):
        self.raw    = byte
        self.OPER   =(byte & 0x80)>>7
        self.RQS_MSS=(byte & 0x40)>>6
        self.ESB    =(byte & 0x20)>>5
        self.MAV    =(byte & 0x10)>>4
        self.MSG    =(byte & 0x04)>>2
        self.USR    =(byte & 0x02)>>1
        self.TRG    =(byte & 0x01)>>0

class USB488_Status(USBTMC_Status):
    """
    """
    INTERRUPT_IN_BUSY=0x20
    
    def __init__(self, bytes):
        self.USBTMC_status=bytes[0]
        self.bTag=bytes[1]
        self.SBR=IEEE488_Status_Byte_Reg(bytes[2])
        
    @classmethod
    def msg(cls,i):
        if (i == cls.INTERRUPT_IN_BUSY):
            return "Interrupt in busy"
        else:
            return USBTMC_Status.msg(i)

#USBTMC requests values/USBTMC Table 15
class USBTMC_REQUEST:
    INITIATE_ABORT_BULK_OUT     = 1
    CHECK_ABORT_BULK_OUT_STATUS = 2
    INITIATE_ABORT_BULK_IN      = 3
    CHECK_ABORT_BULK_IN_STATUS  = 4
    INITIATE_CLEAR              = 5
    CHECK_CLEAR_STATUS          = 6
    GET_CAPABILITIES            = 7
    INDICATOR_PULSE             = 64

class USB488_REQUEST(USBTMC_REQUEST):# USB488 Table 9
    READ_STATUS_BYTE = 128
    REN_CONTROL      = 160
    GOTO_LOCAL       = 161
    LOCAL_LOCKOUT    = 162

class StandardFeature:# usb2.0 table 9-6
    DEVICE_REMOTE_WAKEUP = 1
    ENDPOINT_HALT = 0
    TEST_MODE = 2

class SREmask:
    OPER = 1<<7
    ESB  = 1<<5
    MAV  = 1<<4
    MSG  = 1<<2
    USR  = 1<<1
    TRG  = 1<<0

class USBTMC_device:
    """
    USB device act as a TMC device
    """
    @classmethod
    def find_all(cls,**args):
        usbdevs=find_tmc_devices(**args)
        return [cls(dev) for dev in usbdevs]

    def __init__(self,device):
        # device:usb.core.Device
        self.device=device
        if self.device.is_kernel_driver_active(0):
            self.device.detach_kernel_driver(0)
        self.device.set_configuration()
        self.device.set_interface_altsetting()
        
        for cnf in self.device:
            for intf in cnf:
                #check if this device has TMC/USB488 interface             
                if ((intf.bInterfaceClass == USBTMC_bInterfaceClass) and
                    (intf.bInterfaceSubClass == USBTMC_bInterfaceSubClass)):
                    self.__init_data__()
                    self.getendpoints(cnf, intf)
                    time.sleep(0.01)
                    self.get_capabilities() # set self.capabilities

                    self.bulk_in.clear_halt()
                    self.bulk_out.clear_halt()
                    if self.intr_in:
                        self.intr_in.clear_halt()
                    return
        raise USBError("the device is not USBTMC/USB488 Class device")

    def __init_data__(self):
        self.last_write_bTag=0
        self.last_read_bTag=0
        self.eof=0
        self.retry_buf=""
        self.timeout=USBTMC_DEFAULT_TIMEOUT
        self.term_char_enabled=False
        self.term_char="\n"
        
    def __del__(self):
        # # you may not need all three of them here. But should not cause any problem anyway.

        if self.device :
            # try:
            #     self.clear_bulk_out_halt()
            # except:
            #     raise USBError("clear_bulk_out_halt")
            # try:
            #     self.clear_bulk_in_halt()
            # except:
            #     raise USBError("clear_bulk_in_halt")
            # #self.clear() # this call cause a pipe error the after access on Aglilent Oscilloscope 
            # # on Linux(Ubuntu 14.04), you must dispose resorces.
            # # othewise other program cannot access device later, until the connection to the device is reset
            # # by power off/on or diconnecting/reconnecting USB cable, etc.
            try:
                dispose_resources(self.device)
            except:
                raise USBError("dispose_resoruce")
            finally:
                self.device=None
        return

    @property
    def product(self):
        return self.device.product

    @property
    def manufacturer(self):
        return self.device.manufacturer

    @property
    def serial_number(self):
        return self.device.serial_number
    
    def getendpoints(self, cnf, intf):
        self.intf = intf
        #intf.set_altsetting()
        #self.setting = self.intf.get_active_setting()
        num_endpoints = self.intf.bNumEndpoints
        if (num_endpoints < 2):
            raise USBError("USBTMC should have at least 2  endpoints but not %d"%num_endpoints)
        #find and setup endpoints
        self.bulk_out = None #intf[0]normally
        self.bulk_in = None  #intf[1] 
        self.intr_in = None  #intf[2]
        
        for ep in intf:
            attr = ep.bmAttributes
            direction = ep.bEndpointAddress & usb.ENDPOINT_DIR_MASK # can be replaced with usb.util.endpoint_direction(e.bEndpointAddress)
            ep_type = attr & usb.ENDPOINT_TYPE_MASK # can be replaced with usb.util.endpoint_type(e.bmAttributes)
            #show_endpoint(self.device, self.intf.configuration,self.intf,ep)
            if (ep_type == usb.ENDPOINT_TYPE_BULK):
                if (direction == usb.ENDPOINT_IN):
                    self.bulk_in=ep
                elif (direction == usb.ENDPOINT_OUT):
                    self.bulk_out=ep
            elif (ep_type == usb.ENDPOINT_TYPE_INTERRUPT):
                if (direction == usb.ENDPOINT_IN):
                    self.intr_in = ep
        if (self.bulk_in and self.bulk_out):
            return
        else:
            raise USBError("TMC device must have both Bulk-In and Bulk-out endpoints.")
        
        #return # unreachable 


    def isUSB488(self):
        if (self.intf.bInterfaceProtocol == 1):
            return True
        else:
            return False

    def usb_get_status(self,recipient=None):
        """
        recipient can be None(default) or Interfae or endpoint.
        return values:
            device:D1-Remote wakeup/D0-self powered
            interface : 0x00,0x00
            endpoint: D0-halt
        """
        return  usb.control.get_status(self.device, recipient)

    def reset(self):
        return self.device.reset()

    def clear_halt(self):
        """
        re-establish synchronization in all end-points.
        """
        self.bulk_in.clear_halt()
        self.bulk_out.clear_halt()
        if self.intr_in:
            self.intr_in.clear_halt()
            
    def ask0(self, cmd:str = "*IDN?\n", requestSize = 0,
             termChar = "\n", termCharFlag = True, io_timeout = 1000):
        """ 
        A name borrowed from PyVISA module 
        return value: tuple of (data size, binary array of data)
        """
        self.device_write(cmd)
        return self.read0(io_timeout = io_timeout
                          , termChar = termChar
                          , flag = termCharFlag
                          , requestSize = requestSize)

    def ask(self, cmd:str="*IDN?\n",
            requestSize=0, 
            termChar="\n",
            termCharFlag=True,
            io_timeout=1000):
        """ 
        A name borrowed from PyVISA module 
        now return value as string. Old behaviour is available as ask0.
        "termCharFlag=False" is 10 times faster than "termChanFlag=True" (at lease in some cases).
        """
        self.device_write(cmd)
        data=self.read(requestSize=requestSize
                       , io_timeout=io_timeout
                       , termChar=termChar
                       , flag=termCharFlag
                       )
        return data

    askS=ask
    
    def read(self, requestSize=USBTMC_SIZE_IOBUFFER, io_timeout=1000
             , lock_timeout=0, flag=False, termChar='\x00') -> bytes:
        """
        returns values as bytes. Old behaviour is now available as read0
        """
        data=array.array('B') # null array
        eom=False
        termCharFlag=(True if (flag and (termChar != '\x00')) else False)
        requestSize=max(requestSize,USBTMC_SIZE_IOBUFFER)
        usbtmclogger.debug(f"{eom=}, {requestSize=}")
        while (requestSize > 0) and (not eom):
            rsize=min(requestSize, USBTMC_SIZE_IOBUFFER)
            resp=self.device_read(rsize,
                                  termCharFlag=termCharFlag, 
                                  termchar=termChar,
                                  timeout=io_timeout)
            usbtmclogger.debug(f"resp:{resp.data[:resp.TransferSize]}, {eom=}, {requestSize=}")
            data.extend(resp.data[:resp.TransferSize])
            eom = resp.eom
            requestSize -=resp.TransferSize
        return data.tobytes()
    # for compatibility
    readS=read

    def read0(self,requestSize=0, io_timeout=1000
              , lock_timeout=0, flag=False, termChar='\x00'):
        """
        returns values as tuple of (data size, binary array data)
        """
        data=array.array('B') # null array
        ndata=0
        eom=False
        if 0 < requestSize < USBTMC_SIZE_IOBUFFER:
            rsize=requestSize
        else:
            rsize=USBTMC_SIZE_IOBUFFER
        while not (eom or
                   ((0 < requestSize) and (requestSize <= ndata))
                   ):
            resp=self.device_read(rsize, termCharFlag=flag,
                                  termchar=termChar,timeout=io_timeout)
            usbtmclogger.info("read_resp: {resp.TransferSize}")
            ndata += resp.TransferSize
            #data  += resp.data
            data.extend(resp.data[:resp.TransferSize])
            eom = resp.eom
            if eom:
                break
        return (ndata,data)

    def write(self, cmd="*IDN?\n") :
        return self.device_write(cmd)

    def device_write(self,  message:Union[str,bytes])  :
        if type(message) == str:
            message=message.encode('ascii')
        remaining=len(message)
        while (remaining > 0):
            #transferSize=remaining
            # bulk_out message includes 12bytes usbtmc header.
            if ((remaining + USBTMC_HEADER_SIZE ) < USBTMC_SIZE_IOBUFFER):# do we need it in python?
                eom=True
                transferSize=remaining # can send all remaining data
            else:
                eom=False
                transferSize=USBTMC_SIZE_IOBUFFER-USBTMC_HEADER_SIZE # send data as much as possible
            btag, h=mkDevDepMSGOUTHeader(transferSize, eom=eom)
            if ((transferSize % 4) == 0):
                command=b"%s%s"%(h,
                                 message[:transferSize])
            else:# padding data for 4bytes boundary
                command=b"%s%s%s"%(h,
                                   message[:transferSize],
                                   (4-(transferSize % 4))*b'\0')
            command=array.array('B',command)
            #command=array.array('B',command.encode('utf-8'))
            usbtmclogger.info(
                f"device_write: {btag},{command!s},{len(command)},{transferSize}"
            )
            try:
                self.bulk_out.write(command)
                self.last_write_bTag=btag
            except:
                #self.abort_bulk_out() # is it reasonable?
                sys.stdout.write("aborting\n")
                raise
            message=message[transferSize:]
            remaining=len(message)
        return 

    def device_read(self,
                    transferSize=USBTMC_SIZE_DEFAULT, 
                    termCharFlag=False,
                    termchar="\0",
                    timeout=1000):
        # bulkin header size = 12 standard headr
        #                    + 4bytes for Deivce Responce (msgID, TransferSize, termChar, eom)
        ndata=0
        btag, buf=mkReqDevDepMSGINHeader(transferSize, termCharFlag, termchar)
        buf=array.array('B',buf) # convert string to byte array
        # buf=array.array('B',buf.encode("utf-8")) # convert string to byte array
        usbtmclogger.info(f"ReqHeader: {buf}, {len(buf)}, transferSize:{transferSize}")
        try:
            self.bulk_out.write(buf, timeout=self.timeout)
        except:
            #self.abort_bulk_out() #?
            sys.stdout.write("aborting\n")
            raise
        self.last_write_bTag=btag
        try:
            # add 12+4 for usb header size (NY, 2015.1.21)
            raw_resp=self.bulk_in.read(transferSize+16, timeout = timeout)
            usbtmclogger.info(raw_resp)
            resp=DevDep_Responce(raw_resp)
        except:
            raise
        self.last_read_bTag=resp.bTag
        return resp

    def vender_write(self,message):
        """
        Vender specific bulk write method. Should be 
        """
        raise USBTMCError("Not Implemented")

    def vender_read(self,maxsize=None):
        raise USBTMCError("Not Implemented")

    def check_SRQ(self):
        rv=self.intr_in.read(self.intr_in.wMaxPacketSize, timeout=self.intr_in.bInterval)
        sb=Interrupt_IN_Data(rv)
        # assert(sb.bTag == 0x1) for SRQ
        return sb

    # class standard control messages
    """ctrl_transfer(self, bmRequestType, bRequest, 
                     wValue=0, wIndex=0, data_or_wLength=None, timeout=None) 
    unbound usb.core.Device method
    Do a control transfer on the endpoint 0.
    
    This method is used to issue a control transfer over the
    endpoint 0(endpoint 0 is required to always be a control endpoint).
    
    The parameters bmRequestType, bRequest, wValue and wIndex are the
    same of the USB Standard Control Request format.
    
    Control requests may or may not have a data payload to write/read.
    In cases which it has, the direction bit of the bmRequestType
    field is used to infere the desired request direction. For
    host to device requests (OUT), data_or_wLength parameter is
    the data payload to send, and it must be a sequence type convertible
    to an array object. In this case, the return value is the number of data
    payload written. For device to host requests (IN), data_or_wLength
    is the wLength parameter of the control request specifying the
    number of bytes to read in data payload. In this case, the return
    value is the data payload read, as an array object."""

    def abort_bulk_out(self):
        rv=self.device.ctrl_transfer(
            usb.util.build_request_type(# bmRequest type
                CTRL_IN, CTRL_TYPE_CLASS, CTRL_RECIPIENT_ENDPOINT
                #usb.ENDPOINT_IN | usb.TYPE_CLASS|usb.RECIP_ENDPOINT,
            ),
            USBTMC_REQUEST.INITIATE_ABORT_BULK_OUT,
            self.last_write_bTag,
            self.bulk_out.bEndpointAddress,
            data_or_wLength=2,
            timeout=self.timeout)
        if (rv[0] == USBTMC_Status.SUCCESS):
            rv=self.check_abort_bulk_out_status()
            while(rv[0] == USBTMC_Status.PENDING):
                rv=self.check_abort_bulk_out_status()
            if (rv[0] == USBTMC_Status.SUCCESS):
                self.clear_bulk_out_halt()
            return rv
        elif (rv[0] == USBTMC_Status.TRANSFER_NOT_IN_PROGRESS):
                raise USBTMCError("Transfer not in progress")
        else:
            usbtmclogger.warning( f"Abort_bulk_out Error {rv}")
            raise USBTMCError("Initiate abort_bulk_out failed")

    def check_abort_bulk_out_status(self):
        # usb.control.get_status(self.device, self.bulk_out.bEndpointAddress)
        rv=self.device.ctrl_transfer(
            build_request_type(CTRL_IN, CTRL_TYPE_CLASS, CTRL_RECIPIENT_ENDPOINT),
            USBTMC_REQUEST.CHECK_ABORT_BULK_OUT_STATUS, # CHECK_STATUS
            0,
            self.bulk_out.bEndpointAddress,
            data_or_wLength=8,
            timeout=self.timeout)
        return rv
    
    def clear_bulk_out_halt(self):#USBTMC 3.2.2.4
        #usb.control.clear_feature(self.device,usb.ENDPOINT_HALT,self.bulk_out.bEndpointAddress)
        rv=self.device.ctrl_transfer(
            build_request_type(CTRL_OUT, CTRL_TYPE_STANDARD, CTRL_RECIPIENT_ENDPOINT),
            usb.REQ_CLEAR_FEATURE, # Clear feature request
            usbctrl.ENDPOINT_HALT, # Feature ENDPOINT_HALT
            self.bulk_out.bEndpointAddress,
            data_or_wLength=None,# Although we don't really want data this time
            timeout=self.timeout)
        if(rv==None):
            sys.stdout.write("USBTMC: usb_control_msg returned None\n")

        return rv

    def abort_bulk_in(self):
        rv=self.device.ctrl_transfer(
            build_request_type(# bmRequest type
                CTRL_IN, CTRL_TYPE_CLASS, CTRL_RECIPIENT_ENDPOINT
            ), 
            USBTMC_REQUEST.INITIATE_ABORT_BULK_IN, # INITIATE_ABORT
            self.last_read_bTag, # Last transaction's bTag value
            self.bulk_in.bEndpointAddress, # Endpoint
            2, # Number of characters to read
            self.timeout); # Timeout in miliseconds
        if (rv[0] == USBTMC_Status.SUCCESS):
            rv=self.check_abort_bulk_in_status()
            while(rv[0] == USBTMC_Status.PENDING):
                rv=self.check_abort_bulk_int_status()
            return rv
        elif (rv[0] == USBTMC_Status.TRANSFER_NOT_IN_PROGRESS):
            return
        elif (rv[0] == USBTMC_Status.FAILED):
            return 
        else:
            raise USBTMCError("Initiate abort_bulk_in failed %d"%rv[0])
        
    def check_abort_bulk_in_status(self):
        n=0
        max_size=self.bulk_in.wMaxPacketSize
        # clear buffer 
        while(1):
            rv=self.bulk_in.read(USBTMC_SIZE_IOBUFFER, self.timeout)
            n +=1
            if (len(rv) < max_size): #receive a short packet. 
                break 
            elif  (n >= USBTMC_MAX_READS_TO_CLEAR_BULK_IN):
                raise USBTMCError("Couldn't clear device buffer "
                                  "within %d cycles\n"%USBTMC_MAX_READS_TO_CLEAR_BULK_IN)

        rv=self.device.ctrl_transfer(
            build_request_type(CTRL_IN, CTRL_TYPE_CLASS,
                               CTRL_RECIPIENT_ENDPOINT), # bmRequest type
            USBTMC_REQUEST.CHECK_ABORT_BULK_IN_STATUS, # CHECK_STATUS
            0, # Reserved
            self.bulk_in.bEndpointAddress, # Endpoint
            0x08, # Number of characters to read
            self.timeout)  # Timeout (jiffies)
        return rv

    def clear_bulk_in_halt(self):#USBTMC 3.3.2.4/4.1.1.2
        # rv=usb.control.clear_feature(self.device, usb.control.ENDPOINT_HALT,
        #                              self.bulk_in.bEndpointAddress)
        rv=self.device.ctrl_transfer(        
            build_request_type(CTRL_OUT, CTRL_TYPE_STANDARD,
                               CTRL_RECIPIENT_ENDPOINT), # bmRequest type
            usb.REQ_CLEAR_FEATURE, # Clear feature request
            usbctrl.ENDPOINT_HALT, # Feature ENDPOINT_HALT
            self.bulk_in.bEndpointAddress,
            None, # Although we don't really want data this time
            self.timeout)
        return rv

    #
    def clear(self):
        rv=self.device.ctrl_transfer(        
            bmRequestType=build_request_type(
                CTRL_IN, CTRL_TYPE_CLASS, CTRL_RECIPIENT_INTERFACE), # bmRequest type
            bRequest=USBTMC_REQUEST.INITIATE_CLEAR, # INITIATE_CLEAR
            wValue=0, # Interface number (always zero for USBTMC)
            wIndex=0, # Reserved
            data_or_wLength=1, # Number of characters to read
            timeout=self.timeout) # Timeout (jiffies)
        if (rv[0] == USBTMC_Status.SUCCESS):
            rv=self.check_clear_status()
            n=0
            while (rv[0] == USBTMC_Status.PENDING):
                time.sleep(0.1)
                rv=self.check_clear_status()
                n+=1
                if n > 1000:
                    raise USBTMCError("clear status failed: too many iteration")
            # re-establish synchronization
            self.clear_halt()
            return
        return rv

    def check_clear_status(self):
        rv=self.device.ctrl_transfer(        
            build_request_type(CTRL_IN, CTRL_TYPE_CLASS,
                               CTRL_RECIPIENT_INTERFACE), # bmRequest type
            USBTMC_REQUEST.CHECK_CLEAR_STATUS, # INITIATE_CLEAR
            0, # Interface number (always zero for USBTMC)
            0, # Reserved
            2, # Number of characters to read
            self.timeout)
        return rv

    def get_capabilities(self):
        # see Table 36 - Get_Capabilities setup packet
        b=self.device.ctrl_transfer(
            build_request_type(CTRL_IN, CTRL_TYPE_CLASS,
                               CTRL_RECIPIENT_INTERFACE), # bmRequest type
            USBTMC_REQUEST.GET_CAPABILITIES,
            wValue=0x0000,wIndex=0,
            data_or_wLength=0x0018,
            timeout=self.timeout)
        if (b[0] == USBTMC_Status.SUCCESS):
            self.capabilities = USBTMC_Capabilities(b)
            return self.capabilities
        return None
        
    def indicator_pulse(self):
        if self.capabilities.indicator_pulse:
            # see Table 38- Indicator_pulse setup packet            
            b=self.device.ctrl_transfer(
                build_request_type(CTRL_IN, CTRL_TYPE_CLASS,
                                   CTRL_RECIPIENT_INTERFACE), # bmRequest type
                USBTMC_REQUEST.INDICATOR_PULSE,
                data_or_wLength=0x0001,
                timeout=self.timeout)
        else:
            raise USBError("INDICATOR_PULSE is not supported on this device")

class USB488_device(USBTMC_device):
    #mandatory commands
    def CLS(self):
        self.write("*CLS\n")

    def ESE(self,query=False):
        if query:
            return self.ask("*ESE?;\n")
        else:
            self.write("*ESE;\n")

    def ESR(self):
        return self.ask("*ESQ?;\n")

    def IDN(self):
        return self.ask("*IDN?;\n")

    def OPC(self,query=False):
        if query:
            return self.ask("*OPC?;\n")
        else:
            self.write("*OPC;\n")

    def RST(self):
        self.write("*RST;\n")

    def SRE(self,mask=None):
        if mask == None:
            return self.ask("*SRE?;\n")
        else:
            self.write("*SRE %d;\n"%mask)

    def STB(self):
        return self.ask("*STB?;\n")
    
    def TRG(self):
        self.write("*TRG\n")

    def TST(self):
        return self.ask("*TST?\n")

    def WAI(self):
        self.write("*WAI\n")
    
    # optional commands

    def CAL(self):
        """
        """
        return self.ask("*CAL?\n")

    def DDT(self,query=False):
        if query:
            return self.ask("*DDT?\n")
        else:
            self.write("*DDT\n")

    def DMC(self):
        self.write("*DMC\n")

    def EMC(self,query=False):
        if query:
            return self.ask("*EMC?\n")
        else:
            self.write("*EMC\n")
    def GMC(self):
        return self.ask("*GMC?\n")

    def LMC(self):
        return self.ask("*LMC?\n")

    def LRN(self):
        return self.ask("*LRN?\n")

    def PSC(self,query=False):
        if query:
            return self.ask("*PSC?\n")
        else:
            self.write("*PSC\n")

    def PUD(self):
        self.write("*PUD\n")

    def RCL(self):
        self.write("*RCL\n")

    def RDT(self,query=False):
        if query:
            return self.ask("*RDT?\n")
        else:
            self.write("*RDT")

    def RMC(self):
        self.write("*RMC\n")

    def SAV(self):
        self.write("*SAV\n")

    def SAD(self):
        self.write("*SDS")
        
    def SDS(self):
        self.write("*SDS")
    #
    def OPT(self):
        return self.ask("*OPT?\n")

    def TER(self):
        return self.ask("*TER?\n")
    #
    def RemoteEnable(self,enable=True):#Table 15
        if enable:
            b=self.device.ctrl_transfer(
                build_request_type(CTRL_IN, CTRL_TYPE_CLASS,
                                   CTRL_RECIPIENT_INTERFACE), # bmRequest type
                USB488_REQUEST.REN_CONTROL,
                wValue= 1, # should I use struct? to avoide endianess
                wIndex= 0, # Interface number (always zero for USBTMC)
                data_or_wLength=0x1,
                timeout=self.timeout)
        else:
            b=self.device.ctrl_transfer(
                build_request_type(CTRL_IN, CTRL_TYPE_CLASS,
                                   CTRL_RECIPIENT_INTERFACE), # bmRequest type
                USB488_REQUEST.REN_CONTROL,
                wValue= 0, # should I use struct? to avoide endianess
                wIndex= 0, # Interface number (always zero for USBTMC)
                data_or_wLength=0x1,
                timeout=self.timeout)

        return b #USBTMC_Status

    def LocalLockOut(self):
        b=self.device.ctrl_transfer(
            build_request_type(CTRL_IN, CTRL_TYPE_CLASS,
                               CTRL_RECIPIENT_INTERFACE), # bmRequest type
            USB488_REQUEST.LOCAL_LOCKOUT,
            wValue= 0, # tabel 19
            wIndex= 0, # Interface number (always zero for USBTMC)
            data_or_wLength=0x0001,
            timeout=self.timeout)
        return b #USBTMC_Status

    def GoToLocal(self):
        b=self.device.ctrl_transfer(
            build_request_type(CTRL_IN, CTRL_TYPE_CLASS,
                               CTRL_RECIPIENT_INTERFACE), # bmRequest type
            USB488_REQUEST.GOTO_LOCAL,
            wValue= 0, # should I use struct? to avoide endianess
            wIndex= 0, # Interface number (always zero for USBTMC)
            data_or_wLength=0x0001,
            timeout=self.timeout)
        return b #USBTMC_Status

    def Read_Status_Byte(self):
        # see Table 9,
        b=self.device.ctrl_transfer(
            build_request_type(CTRL_IN, CTRL_TYPE_CLASS,
                               CTRL_RECIPIENT_INTERFACE), # bmRequest type
            USB488_REQUEST.READ_STATUS_BYTE,
            wValue=bTag.next()&0x7f,
            wIndex= 0, # Interface number (always zero for USBTMC)
            data_or_wLength=0x0003,# USB2.0 specification, section 9.3.5
            timeout=self.timeout)
        if self.intr_in:
            sb=USB488_Status(b)
            bytes=self.intr_in.read(self.intr_in.wMaxPacketSize, self.intr_in.bInterval)
            sb.SBR=Interrupt_IN_Data(bytes).SBR
            return sb
        else:
            return USB488_Status(b)

    def TRIGGER(self):
        if self.capabilities.DT1:
            btag,h=mkTriggerHeader()
            try:
                self.bulk_out.write(h)
                self.last_write_bTag=btag
            except:
                #self.abort_bulk_out() # is it reasonable?
                sys.stdout.write("aborting\n")
                raise
            
    def GetExecuteTrigger(self):
        if self.capabilities.DT1:
            self.TRIGGER()
        else:
            self.TRG()
    
    def SelectedDeviceClear(self):#table 26
        self.clear()
    
    # @classmethod
    # def DeviceClear(cls):
    #     for ent in cls.instances():
    #         ent.clear()

    def DCL(self):
        """
        send DCL(Device CLear)
        """
        self.write("*DCL\n")

    # @classmethod
    # def LockOut(cls):
    #     for ent in cls.instances():
    #         ent.RemoteEnable()
    #         ent.LocalLockOut()

class USBTMC_Capabilities:
    def __init__(self, bdata):
        self.bcdUSBTMC="0x%.2x%.2x"%(bdata[3],bdata[2])
        if (bdata[4]&0x4):
            self.indicator_pulse=True
        else:
            self.indicator_pulse=False

        if (bdata[4]&0x2):
            self.talk_only=True
        else:
            self.talk_only=False

        if (bdata[4]&0x1):
            self.listen_only=True
        else:
            self.listen_only=False
        if (bdata[5] &0x1):
            self.termchar_enable=True
        else:
            self.termchar_enable=False
        if(len(bdata) > USBTMC_HEADER_SIZE):
            self.bcdUSB488="0x%.2x%.2x"%(bdata[13],bdata[12])
            if bdata[14]&0x4:
                self.USB488=True
            else:
                self.USB488=False
                
            if bdata[14]&0x2:
                self.REN_CONTROL=True
            else:
                self.REN_CONTROL=False
                
            if bdata[14]&0x1:
                self.TRIGGER=True
            else:
                self.TRIGGER=False
                
            if bdata[15]&0x8:
                self.SCPI=True
            else:
                self.SCPI=False
                
            if bdata[15]&0x4:
                self.SR1=True
            else:
                self.SR1=False
                
            if bdata[15]&0x2:
                self.RL1=True
            else:
                self.RL1=False
                
            if bdata[15]&0x1:
                self.DT1=True
            else:
                self.DT1=False

    def __str__(self):
        msg=""
        if self.indicator_pulse:
            msg +="indicator pulse,"
        if self.talk_only:
            msg +="talk only,"
        if self.listen_only:
            msg +="listen only,"
        if self.termchar_enable:
            msg +="termchar enable"
        return msg

# bTag generator
class bTag:
    __lastbtag=0
    @classmethod
    def next(cls):
        cls.__lastbtag=( (cls.__lastbtag + 1) & 0xff
                         if (cls.__lastbtag < 0xff) else 1)
        return cls.__lastbtag
    @classmethod
    def last(cls):
        return cls.__lastbtag

def mkCommonHeader(msgid):
    btag=bTag.next()
    h=b"%1c%1c%1c\0"%(msgid&0xff, btag, (~btag)&0xff) # USBTMC spec table 1.
    return (btag,h)


def mkTriggerHeader():
    btag, h=mkCommonHeader(USBTMC_MsgID.TRIGGER)
    h=b"%s\0\0\0\0\0\0\0\0"%(h)
    return (btag,h)

def mkDevDepMSGOUTHeader(tsize, eom=False):
    btag, h=mkCommonHeader(USBTMC_MsgID.DEV_DEP_MSG_OUT)
    if eom:
        h=b"%s%1c%1c%1c%1c\1\0\0\0"%(h,
                                    tsize & 0xff,
                                    (tsize>>8) & 0xff,
                                    (tsize>>16) & 0xff,
                                    (tsize>>24) & 0xff)
    else:
        h=b"%s%1c%1c%1c%1c\0\0\0\0"%(h,
                                    tsize & 0xff,
                                    (tsize>>8) & 0xff,
                                    (tsize>>16) & 0xff,
                                    (tsize>>24) & 0xff)
    return (btag,h)

def mkReqDevDepMSGINHeader(tsize:int,
                           TermCharEnable:bool,
                           TermChar:Union[str, bytes]=b'\n'):
    if type(TermChar) == str:
        TermChar=TermChar.encode("ascii")[0]
    usbtmclogger.info(f"mkReqDevDepMSGINHeader: {tsize=}, {TermCharEnable=}, {TermChar=}")
        
    btag, h=mkCommonHeader(USBTMC_MsgID.DEV_DEP_MSG_IN)
    if TermCharEnable:
        h=b"%s%1c%1c%1c%1c\2%1c\0\0"%(h,
                                     tsize & 0xff,
                                     (tsize>>8) & 0xff,
                                     (tsize>>16) & 0xff,
                                     (tsize>>24) & 0xff,
                                     TermChar & 0xff)
    else:
        h=b"%s%1c%1c%1c%1c\0\0\0\0"%(h,
                                     tsize & 0xff,
                                     (tsize>>8) & 0xff,
                                     (tsize>>16) & 0xff,
                                     (tsize>>24) & 0xff,
                                     )
    return (btag, h)
    

def mkVendorSpecMSGOUTHeader(tsize):
    btag, h=mkCommonHeader(USBTMC_MsgID.VENDOR_SPECIFIC_OUT)
    h=b"%s%1c%1c%1c%1c\0\0\0\0"%(h,
                                tsize & 0xff,
                                (tsize>>8) & 0xff,
                                (tsize>>16) & 0xff,
                                (tsize>>24) & 0xff
                                )
    return (btag,h)

def mkReqVendorSpecMSGINHeader(tsize):
    btag,h=mkCommonHeader(USBTMC_MsgID.VENDOR_SPECIFIC_IN)
    h=b"%s%1c%1c%1c%1c\0\0\0\0"%(h,
                                tsize & 0xff,
                                (tsize>>8) & 0xff,
                                (tsize>>16) & 0xff,
                                (tsize>>24) & 0xff
                                )
    return (btag,h)
        
class BulkIn_Header:
    """
    convert return value header to structure
    """
    def __init__(self,bytes):
        self.msgID=bytes[0]
        self.bTag=bytes[1]
        self.bTagInverse=bytes[2]
        self.resMsg=bytes[4:12]
        try:
            self.data=bytes[12:]
        except:
            self.data=None

class DevDep_Responce(BulkIn_Header):
    def __init__(self,bytes):
        BulkIn_Header.__init__(self, bytes)
        if self.msgID != USBTMC_MsgID.DEV_DEP_MSG_IN :
            raise TypeError
        #self.TransferSize=struct.unpack("<l",self.resMsg[:4])[0]
        self.TransferSize = ( self.resMsg[0]+
                             (self.resMsg[1]<<8)+
                             (self.resMsg[2]<<16)+
                             (self.resMsg[3]<<24))
        self.TermChar=(self.resMsg[4]>>1)&0x1
        self.eom=self.resMsg[4]&0x1

class VendorSpec_Responce(BulkIn_Header):
    def __init__(self,bytes):
        BulkIn_Header.__init__(self, bytes)
        if self.msgID != USBTMC_MsgID.VENDOR_SPECIFIC_IN :
            raise TypeError
        self.TransferSize = (self.resMsg[0]+
                             (self.resMsg[1]<<8)+
                             (self.resMsg[2]<<16)+
                             (self.resMsg[3]<<24))
#
class Interrupt_IN_Data:# Table 6, USB488
    def __init__(self, bytes):
        self.SBR=None
        self.statusBytes=None
        if (bytes[0] & 0x80):# USB488
            self.bTag=bytes[0]&0x7f # 0x01 for SRQ responce or bTag_id for READ_Status
            self.SBR=IEEE488_Status_Byte_Reg(bytes[1])
        elif (bytes[0] & 0x40): # vendor specific
            self.statusBytes=bytes[1:]
        else:
            self.statusBytes=bytes[1:]

# test functions are moved to sample/PyUSBTMC_test.py
