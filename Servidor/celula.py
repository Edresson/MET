# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO

import sys
import hx711 

DT = 23 #dt pino no hx711 
clk = 24 #clk pino no hx711 
GPIO.setwarnings(False)
def cleanAndExit():
    
    GPIO.cleanup()
    sys.exit()

hx = hx711.HX711(DT, clk)
hx.set_reading_format("LSB", "MSB")

hx.set_reference_unit(-57100.26666666644/9.45)

hx.reset()
hx.tare()


def getvalue():
	
        val = hx.get_weight(2)
        
        hx.power_down()
        hx.power_up()
        if(val < 0):
            val = 0.0
        
        return val
    
        


    
def calibrar():
    global hx
    calib = 0
    hx.set_reading_format("LSB", "MSB")


    hx.set_reference_unit(1)

    for i in range(0,10):
        calib += hx.get_weight(1)

    return (calib/10)


def iniciarcel(calib):
    hx.set_reading_format("LSB", "MSB")
    
    hx.set_reference_unit(float(calib))

    hx.reset()
    hx.tare()
    
    
def tare():
    hx.reset()
    hx.tare()
    


    

