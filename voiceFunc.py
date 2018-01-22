#2 voice 생성 출력 통합 voicefunc
import datetime
import naver
import pygame
import time
#import weather
from Holiday import Holiday
from TnHdev import I2Cth
from weather import *
weekDay = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
#engine = pyttsx3.init()

class voiceNot:
    def __init__(self):
        self.hol = Holiday()#생성 오래 걸림, 미리 생성자 부르기
        pygame.init()
        print("hol")
        self.weather_list = weather_info
    def voiceFunc(self,content , any = None):
        #content = WEATHER , TH  습도, DATE 
        #default = ANY any:내용
        #음성 겹치지 않도록 함
        while True:
            if pygame.mixer.music.get_busy():
                time.sleep(0.5)
                continue
            break
        
        #텍스트 생성
        txt = ""
        
        if content == "WEATHER":
            #날씨 api 이용해서 구함.
            
            txt = "오늘 날씨는 " + self.weather_list[0] + ", 온도는 " + self.weather_list[1] + "도 입니다."
        elif content == "TH":
            tnh = I2Cth()
            txt = "현재 실내온도는 " + str(round(tnh.checkTemp(),1)) + ", 습도는 " + str(round(tnh.checkHumi(),1)) + " 입니다."
        elif content == "DATE":
            
            dt = datetime.datetime.now()
            wd = datetime.datetime.weekday(dt)
            txt = str(dt.year) + "년 " + str(dt.month) + "월 "+ str(dt.day)+"일 "+weekDay[wd]+" 입니다."
            index = self.hol.isHoliday()
            if index > -1:
                #공휴일 api 이용
                txt += "오늘은 "+self.hol.getDayName(index)+" 입니다."
        elif content == "ANY":
            txt = any
        else:
            raise AttributeError
        
        #네이버 api
        naver.naverVoiceApi(txt)
        
        #음성 로드 출력
        pygame.mixer.music.load("result.mp3")
        pygame.mixer.music.play(1)
        
 