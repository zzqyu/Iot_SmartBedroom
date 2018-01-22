import smbus2 as smbus
import time
#from nowTime import *
from threading import Thread
from Fnd import Fnd
from Holiday import Holiday
import pygame
from Cds import selfLEDcontrol

class curTime:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.out_disp = 0
        self.addr = 0x20
        self.config_port = 0x06
        self.out_port = 0x02
        self.data = (0xFC,0x60,0xDA,0xF2,0x66,0xB6,0x3E,0xE0,0xFE,0xF6)
        self.digit = (0x7F, 0xBF, 0xDF, 0xEF,  0xF7, 0xFB)
        self.fnd = Fnd()
        self.hol = Holiday()
        self.a = '0700'
        self.bus.write_word_data(self.addr, self.config_port, 0x0000)
        self.setFlag = False
        pygame.init()
        
    def nowTimeFnd(self, val):
        
        ##timeCheck()에서 return 받은 리스트를 저장
        timeStr = time.strftime('%H  %M')
        ##return받은 리스트의 상태 변화를 확인하기 위해 사용
        tmp = ''

        while True:
            
            timeStr = time.strftime('%H  %M')
            
            if tmp != timeStr :
                tmp = timeStr
                print("now time : %s%s시 %s%s분" % (tmp[0], tmp[1], tmp[4], tmp[5]))
            
            isec = time.localtime().tm_sec
            self.fnd.outputStop()
            self.fnd.strToOutput(tmp)
            if tmp[:1] == "00":
                self.alarmSet()
                
            if (self.a[:1] == tmp[:1] and self.a[-2:] == tmp[-2:]) and self.a != 'no':
                self.play()
            time.sleep(60 - isec)
                
    def start(self,val):
        self.t1 = Thread(target = self.nowTimeFnd, args = (1,))
        self.t1.start()
        return self.t1
    
            
    def play(self, id = None):
        
        pygame.mixer.music.load("sound.mp3")
        pygame.mixer.music.play(5)
        pygame.mixer.music.set_volume(0.5)
        led = selfLEDcontrol()
        led.on()
	
        
    def alarmStop(self):
        pygame.mixer.music.stop()
    
    def alarmSet(self):
        if not self.setFlag:
            if hol.isHoliday() != -1:
                self.a = '1000'
            
        
    def userSet(self, timeStr = 'no'):
        self.a = timeStr
        self.setFlag = True
'''       
tim = curTime()
#tim.userSet('0936')
tim.start(1)
time.sleep(3)
tim.alarmStop()
'''