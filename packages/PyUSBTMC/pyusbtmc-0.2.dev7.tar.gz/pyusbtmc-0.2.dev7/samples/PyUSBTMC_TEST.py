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
from PyUSBTMC import *

#

def test(**args):
    #import usb.core, usb.util,usb.backend,usb.backend.libusb1
    # dev=usb.core.find(idVendor=0x0957, idProduct=0x0407)
    # dev=usb.core.find(backend=usb.backend.libusb10.get_backend()
    #                      , idVendor=0x0957 # Agilent
    #                      , idProduct=0x1724)
    # dev=usb.core.find( backend=usb.backend.libusb10.get_backend()
    #                    , idVendor=0x0699 # Tektronix 0x02, 0x81, 0x83
    #                    , idProduct=0x0407) #DPO4K
    # dev=usb.core.find(idVendor=0x0699 # Tektronix 
    #, idProduct=0x0347) #AFG3022 address 0x1,0x82,0x83
    usbdevs=find_tmc_devices(**args) # 
    if usbdevs == None:
        return
    usbdev=next(usbdevs)
    #tmcdev=USBTMC_device(dev)
    tmcdev=USB488_device(usbdev)
    usbtmclogger.info("Clear:{}".format(tmcdev.clear()))
    usbtmclogger.info("ClearStatsu:{}".format(tmcdev.check_clear_status()))
    try:
        try:
            tmcdev.device_write("*IDN?\n")
        except:
            tmcdev.abort_bulk_out()
            raise
        r=tmcdev.device_read(4096)
        usbtmclogger.info(
            f"btag:{r.bTag}, eom:{r.eom}, msgID:{r.msgID}, Tsize:{r.TransferSize}, data:{r.data.tounicode()}"
        )
        if (tmcdev.device.idVendor == 1689): #0x0699
            tmcdev.device_write(":DATE?\n")
            r=tmcdev.device_read(4096)
            usbtmclogger.info(
                f"btag:{r.bTag}, eom:{r.eom}, msgID:{r.msgID}, Tsize:{r.TransferSize}, data:{r.data.tounicode()}"
            )
            #tmcdev.write("DAT:ENC ASCI\n")
            tmcdev.write("DAT:ENC SRP\n") # 0-255 or 0-16K
            tmcdev.write("DAT:SOU CH1\n")
            tmcdev.write("WFMO:BYT_N 1\n")
            #tmcdev.write(":CURVE?")
            #w=tmcdev.read(2000020)
        elif (tmcdev.device.idVendor == 2391) : #0x0957
            tmcdev.device_write(":WAV:POINTS?\n")
            r=tmcdev.device_read(4096)
            usbtmclogger.info(
                f"btag:{r.bTag}, eom:{r.eom}, msgID:{r.msgID}, Tsize:{r.TransferSize}, data:{r.data.tounicode()}"
            )
    finally:
        sys.stdout.write("Done")
        return tmcdev

def DSO6K_test(dev=None):
    import Gnuplot
    if not dev:
        dev=test()
    sys.stdout.write("\n")
    dev.write(":STOP;:SINGLE;:WAV:POINTS:MODE MAX;:WAV:POINTS 50000;")
    n, d=dev.ask0("*IDN?;")
    sys.stdout.write(d.tostring());sys.stdout.write("\n")
    maker,model,sn,vers=d.tostring().split(",")
    dev.write(":WAV:SOURCE CH1;\n")
    dev.write(":WAV:POINTS 100000;\n")
    n,d=dev.ask0(":WAV:POINTS?\n")
    sys.stdout.write("WAV:POINT = %s \n"%d.tostring())
    n,wf=dev.ask0(":WAV:DATA?",requestSize=20000000)
    sys.stdout.write("size of waveform %s \n",n)

    dev.write(":WAV:SOURCE CH2;\n")
    n,wf2=dev.ask0(":WAV:DATA?",requestSize=20000000)

    gp=Gnuplot.Gnuplot()
    gp.title("Python USBTMC module example \\n from %s"%model)
    hl=int(wf[1:2].tostring())+2
    gp.plot(wf[hl:-2][::10],wf2[hl:-2][::10])
    x0=wf[-1]
    return dev

def DSO6K_test_pylab(dev=None):
    import pylab
    if not dev:
        dev=test()
    dev.write(":STOP;:SINGLE;:WAV:POINTS:MODE MAX;:WAV:POINTS 50000;")
    n,d=dev.ask("*IDN?;")
    sys.stdout.write(d.tostring());sys.stdout.write("\n")
    maker,model,sn,vers=d.tostring().split(",")
    dev.write(":WAV:SOURCE CH1;\n")
    dev.write(":WAV:POINTS 100000;\n")
    n,d=dev.ask(":WAV:POINTS?\n")
    sys.stdout.write("WAV:POINT = %s \n"%d.tostring())
    n,wf=dev.ask0(":WAV:DATA?",requestSize=20000000)
    sys.stdout.write("size of waveform %s \n",n)

    dev.write(":WAV:SOURCE CH2;\n")
    n,wf2=dev.ask0(":WAV:DATA?",requestSize=20000000)

    pylab.clf()
    pylab.title("Python USBTMC module example from %s"%model)
    hl=int(wf[1:2].tostring())+2
    pylab.xlabel("points")
    pylab.ylabel("signal")
    pylab.plot(range(0,n-hl-2,10),wf[hl:-2][::10], range(0,n-hl-2,10),pylab.array(wf2[hl:-2][::10])-127.)
    pylab.show(False)
    x0=wf[-1]
    return dev

def DPO4K_test():
    import pylab,time
    dev=test(idVendor=0x0699) # pickup
    print()
    if not dev:
        raise RuntimeError("No device was found")
    dev.write("STOP;\n")
    dev.write("DAT:ENC ASCI\n")
    dev.write("DAT:ENC SRP\n") # 0-255 or 0-16K
    dev.write("DAT:SOU CH1\n")
    dev.write("WFMO:BYT_N 1\n")
    s=time.time()
    dev.write("CURVE?")
    n,wf=dev.read0(2000020)
    e=time.time()
    sys.stdout.write(
        "read {:d} bytes in {:f} seconds {:f} bytes/second\n".format(
            n, e-s, n/(e-s)
        )
    )
    pylab.clf()
    hl=int(wf[1:2].tobytes())+2
    pylab.xlabel("points")
    pylab.ylabel("signal")
    pylab.title("Waveform from DPO4034B")
    pylab.plot(wf[hl:-1][::100], color="yellow")
    #
    dev.write("DAT:SOU CH2\n")
    s=time.time()

    dev.write("CURVE?")
    n,wf=dev.read0(2000020)
    pylab.plot(wf[hl:-1][::100], color="cyan")
    e=time.time()
    sys.stdout.write(
        "read {:d} bytes in {:f} seconds {:f} bytes/second\n".format(
            n, e-s, n/(e-s)
        )
    )
    pylab.show()
    sys.stdout.flush()
    return dev

def DPO3K_test():
    import pylab,time
    dev=test()
    dev.write("DAT:ENC ASCI\n")
    dev.write("DAT:ENC SRP\n") # 0-255 or 0-16K
    dev.write("DAT:SOU CH1\n")
    dev.write("WFMO:BYT_N 1\n")
    s=time.time()
    dev.write("CURVE?")
    n,wf=dev.read0(2000020)
    e=time.time()
    sys.stdout.write("read %d bytes in %f seconds %f bytes/second"%(
            n, e-s,n/(e-s)))
    pylab.clf()
    hl=int(wf[1:2].tostring())+2
    pylab.xlabel("points")
    pylab.ylabel("signal")
    pylab.title("Waveform from DPO30xx")
    pylab.plot(wf[hl:-1][::100])
    pylab.show(False)
    return dev

def SL1K_test():
    import pylab
    dev=test()
    
    sys.stdout.write(dev.ask(":DATA?\n")[1].tostring());sys.stdout.write("\n")
    sys.stdout.write(dev.ask(":ACQ?\n")[1].tostring());sys.stdout.write("\n")
    sys.stdout.write( dev.ask(":WAV?\n")[1].tostring());sys.stdout.write("\n")
    sys.stdout.write( dev.ask(":TRIG?\n")[1].tostring());sys.stdout.write("\n")
    sys.stdout.write( dev.ask(":MEAS?\n")[1].tostring());sys.stdout.write("\n")
    sys.stdout.write( dev.ask(":ALARM?\n")[1].tostring());sys.stdout.write("\n")
    sys.stdout.write( dev.ask(":CONTROL?\n")[1].tostring());sys.stdout.write("\n")
    sys.stdout.write( dev.ask(":CHAN1?\n")[1].tostring());sys.stdout.write("\n")
    res=dev.ask(":WAV:LENGTH?")[1].tostring()
    dev.write("WAV:FORMAT BYTE\n")
    dev.write("WAV:TRACE 1\n")
    #dev.write(":DATA:FRAW?\n")
    dev.write(":STOP\n")
    dev.write(":WAV:SEND?\n")
    n,wf=dev.read0(2000020)
    pylab.clf()
    hl=int(wf[1:2].tostring())+2
    nd=int(wf[2:hl].tostring())
    pylab.plot(wf[hl:nd])
    pylab.xlabel("points")
    pylab.ylabel("signal")
    pylab.title("Waveform from Yokogawa SL1000")
    return dev

def AFG3K_test():
    import pylab,time
    devs=find_tmc_devices() # 
    if devs == None:
        return
    dev=USB488_device(devs[0])
    dev.write("*RST\n");time.sleep(3); 
    sys.stdout.write( dev.IDN()[1].tostring());sys.stdout.write("\n")
    AFG3K_setup_test(dev)

def AFG3K_setup_test(dev):
    import pylab
    #'Set CH1 output parameters
    dev.write ("FUNCTION SIN\n") #Set output waveform SIN
    dev.write ("FREQUENCY 10E3\n") #Set frequency 10kHz
    dev.write ("VOLTAGE:AMPLITUDE 2.00\n") #Set amplitude 2Vpp
    dev.write ("VOLTAGE:OFFSET 1.00\n") #Set offset 1V
    dev.write ("PHASE:ADJUST 0DEG\n") #Set phase 0degree
    #Set CH2 output parameters
    dev.write ("SOURCE2:FUNCTION SIN\n") #Set output waveform SIN
    dev.write ("SOURCE2:FREQUENCY 10E3\n") #Set frequency 10kHz
    dev.write ("SOURCE2:VOLTAGE:AMPLITUDE 1.00\n") #Set amplitude 1Vpp
    dev.write ("SOURCE2:VOLTAGE:OFFSET 0.00\n") #Set offset 0V
    dev.write ("SOURCE2:PHASE:ADJUST 90DEG\n") #Set phase 90degrees
    n,wf=dev.ask0("DATA:DATA? EMEM\n")
    hl=int(wf[1:2].tostring())+2
    nd=int(wf[2:hl].tostring())
    pylab.plot(wf[hl:nd])
    pylab.xlabel("points")
    pylab.ylabel("signal")
    pylab.title("EMEM data from Tektronix AFG3000 series")
    #Save settings and output on
    #dev.write ("*SAV 1\n") #Save settings to Setup1
    #dev.write ("*RCL 1\n") #Recall settings from Setup1
    return dev
