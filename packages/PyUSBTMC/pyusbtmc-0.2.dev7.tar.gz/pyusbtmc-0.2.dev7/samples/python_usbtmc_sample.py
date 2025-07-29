#!python
#-*- coding:utf-8 -*-
#
#from __future__ import print_function

import PyUSBTMC

def main():
    dev=next(PyUSBTMC.find_tmc_devices())
    inst=PyUSBTMC.USBTMC_device(dev)

    print (inst.ask("*IDN?"))

    dev=inst
    
    dev.write(":STOP;:SINGLE;:WAV:POINTS:MODE MAX;:WAV:POINTS 50000;")

    print (dev.ask("*IDN?;"))

    maker,model,sn,vers=dev.ask("*IDN?;").split(b",")
    print ("vendor",maker, "model:",model, "sn:",sn)
    
    dev.write(":WAV:SOURCE CH1;\n")
    dev.write(":WAV:POINTS 100000;\n")
    d=dev.ask(":WAV:POINTS?\n")
    print ("WAV:POINT =",d)
    wf=dev.ask_raw(":WAV:DATA?",)
    print "size of waveform",len(wf)

    dev.write(":WAV:SOURCE CH2;\n")
    wf2=dev.ask_raw(":WAV:DATA?")
    print ("size of waveform",len(wf))
    
if __name__ == "__main__":
        
    main()
