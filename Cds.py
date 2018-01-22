#!/usr/bin/python
import smbus2 as smbus
import time
from Cds_led import *
from threading import Thread

class LEDcontrol:
    def __init__(self):
        self.myLed = led()
        self.myCds = cds()
    
    def __del__(self):
        del self.myLed

class autoLEDcontrol(LEDcontrol):
    def __init__(self):
        self.myLed = led()
        self.myCds = cds()
        self.threadStop = False
        
    def cds_led(self, val):
        self.threadStop = False
        while not self.threadStop:
                
            #print("Light level : "+ str(readLight()) + " lx")
                
            self.myLed.ledCheck(self.myCds.readLight())
                  
            time.sleep(0.5)
    def start(self, val):
        self.t1 = Thread(target = self.cds_led, args = (val, ))
        self.t1.start()
        return self.t1
    
    def stop(self):
        self.threadStop = True

class selfLEDcontrol(LEDcontrol):
    
    def on(self, led = True):
        self.myLed.ledOn(led)
        
## main
#cds_led()

