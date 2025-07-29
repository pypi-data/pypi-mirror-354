#!python
#-*- coding:utf-8 -*-
#
import PyUSBTMC

def get_first_inst():
    devs=PyUSBTMC.USB488_device.find_all()
    inst=devs[0]
    return inst

def main():
    devs=PyUSBTMC.USB488_device.find_all()
    inst=devs[0]

    print inst.ask("*IDN?")

    inst.write(":STOP;:SINGLE;:WAV:POINTS:MODE MAX;:WAV:POINTS 50000;")

    print inst.ask("*IDN?;")

    maker,model,sn,vers=inst.ask("*IDN?;").split(",")
    print "vendor",maker, "model:",model, "sn:",sn
    
    inst.write(":WAV:SOURCE CH1;\n")
    inst.write(":WAV:POINTS 100000;\n")

    d=inst.ask(":WAV:POINTS?;\n")
    print "WAV:POINT =",d
    wf=inst.ask(":WAV:DATA?")
    print "size of waveform",len(wf)

    inst.write(":WAV:SOURCE CH2;\n")
    wf2=inst.ask(":WAV:DATA?")
    print "size of waveform",len(wf)


if __name__ == "__main__":
    main()
