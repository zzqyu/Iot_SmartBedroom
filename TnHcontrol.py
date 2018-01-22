#2 온습도 관련 중간 모듈
from TnHdev import *
import time
from threading import Thread
class THcontrol:
    def __init__(self):
        self.motor = Motor()
        self.tnh = I2Cth()
        self.humidifier = Humidifier()
    def __del__(self):
        del self.motor
        del self.humidifier
        
class autoTHcontrol(THcontrol):
    def __init__(self):
        self.motor = Motor()
        self.tnh = I2Cth()
        self.humidifier = Humidifier()
        self.threadStop = False
    
    def TnHcheck(self, val):#Thread(self):
    #체온조절의 부담이 가장 적은 온도, 다시 말하면 덥지도 춥지도 않는 최적온도는 18℃ 정도이며,
    #15.6~20℃ 정도에서 쾌적함을 느낄 수 있습니다.   20-22// 40-60
    #실내의 쾌적함을 유지하려면 온도 외에도 습도를 고려해야 하는데,
    #습도가 30% 미만이거나 80% 이상이면 좋지 않고,
    #40~70% 정도면 대체로 쾌적함을 느낄 수 있습니다.
    #실제로 쾌적함을 주는 습도는 온도에 따라 달라지는데 15℃에서는 70%정도,
    #18~20℃에서는 60%, 21~23℃에서는 50%, 24℃ 이상에서는 40%가 적당한 습도입니다.
    #기상청
        self.threadStop = False
        while not self.threadStop:
            
            temp = self.tnh.checkTemp()
            humi = self.tnh.checkHumi()
            print("temp: ", temp, "humi: ", humi)
                
            if temp < 15:#1단계 난방(모터 반시계) 강
                self.motor.run(8, False)
                if humi<50 and not self.humidifier.isState():
                    self.humidifier.on()
                elif humi>60 and self.humidifier.isState():
                    self.humidifier.off()
                    
            elif temp < 17:#2단계 난방(모터 반시계) 중
                self.motor.run(5, False)
                if humi<50 and not self.humidifier.isState():
                    self.humidifier.on()
                if humi>60 and self.humidifier.isState():
                    self.humidifier.off()
                    
            elif temp < 20:#3단계 난방(모터 반시계) 약
                self.motor.run(2, False)
                if humi<50 and not self.humidifier.isState():
                    self.humidifier.on()
                if humi>60 and self.humidifier.isState():
                    self.humidifier.off()
                    
            elif temp > 30:#4단계 냉방(모터 반시계) 강
                self.motor.run(8)
                if humi<30:
                    self.humidifier.on()
                if humi>40 and self.humidifier.isState():
                    self.humidifier.off()
                    
            elif temp > 28:#5단계 냉방(모터 반시계) 중
                self.motor.run(5)
                if humi<30 and not self.humidifier.isState():
                    self.humidifier.on()
                if humi>40 and self.humidifier.isState():
                    self.humidifier.off()
                    
                        
            elif temp > 25:#6단계 냉방(모터 반시계) 약
                self.motor.run(2)
                if humi<30 and not self.humidifier.isState():
                    self.humidifier.on()
                if humi>40 and self.humidifier.isState():
                    self.humidifier.off()
                        
            else:
                self.motor.stop()
                if humi>55 and self.humidifier.isState():
                    self.humidifier.off()
                if humi < 40 and not self.humidifier.isState():
                    self.humidifier.on()
                        
            #time.sleep(300)
            time.sleep(1)#테스트용)
        print("루프 나옴")
        self.motor.stop()
        self.humidifier.off()
    #def stop(self):
        #self.motor.stop()
        #self.humidifier.off()
    def start(self, val):
        self.t1 = Thread(target=self.TnHcheck, args=(val,) )
        self.t1.start()
        return self.t1
    
    def stop(self):
        self.threadStop=True
        time.sleep(0.1) # Waiting Thread exit
        
class selfTHcontrol(THcontrol):
    
    #자동은 지속적으로 적정온습도 유지
    #수동의 prop메소드는 한번 적정온습도까지 set하고 동작 종료
    def properTemp(self):
        temp = 0
        while True:
            temp = self.tnh.checkTemp()
            if temp<15:
                self.motor.run(8,False)
            elif temp<17:
                self.motor.run(5,False)
            elif temp<20:
                self.motor.run(3,False)
            else:
                self.motor.stop()
                break
           
    def properHumi(self):
        while True:
            temp = self.tnh.checkTemp()
            humi = self.tnh.checkHumi()
            if temp<15:
                if humi<70:
                    self.humidifier.on()
                elif humi>70:
                    self.humidifier.off()
            elif temp<20:
                if humi<60:
                    self.humidifier.on()
                elif humi>60:
                    self.humidifier.off()
            elif temp<22:
                if humi<50:
                    self.humidifier.on()
                elif humi>50:
                    self.humidifier.off()
            else:
                self.humidifier.off()
                break
            
    def tempUP(self, isUP, degree = 1):
        #isUP:  True: up False: down
        if not isUP:
            degree = -degree
        dest = self.tnh.checkTemp()+degree
        while self.tnh.checkTemp()<dest:
            temp = self.tnh.checkTemp()
            if dest-temp>10:
                self.motor.run(isUP, 6)
            else:
                self.motor.run(isUP, 3)
        self.motor.stop()
        
    def humidUP(self, isUP, degree = 1):
        #isUP:  True: up False: down
        if not isUP:
            degree = -degree
        dest = self.tnh.checkHumi()+degree
        while self.tnh.checkHumi()<dest:
            self.humidifier.on()
        self.humidifier.off()
    def fanStop(self):
        self.motor.stop()