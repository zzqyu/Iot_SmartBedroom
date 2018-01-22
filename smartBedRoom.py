from voiceFunc import voiceNot
from TnHcontrol import *
from Cds import *
from curTime import curTime

#기능
#base 모닝콜, 시간 띄우기, 온습도 자동조절
#온습도 자동조절 끄기
#조명 자동조절/수동조절, 날씨 알림, 날짜 알림, 실내 온습도 알림

class smartBedRoom:
	def __init__(self):
		self.autoLED = False
		self.autoTNH = False
		self.morningcallOn = True
		
		self.voi = voiceNot()
		self.tictoc = curTime()
		self.tictoc.start(1)
		print("tic init")
		self.autoTHcon = autoTHcontrol()	   
		self.selfTHcon = selfTHcontrol()
		self.autoLEDcon = autoLEDcontrol()
		self.selfLEDcon = selfLEDcontrol()
		print("hi")
	'''
	def __del__(self):
		print("뭘 넣어야 될 지 모르겠음")
	'''	
	def autoTHonoff(self, val):
		#자동이면 수동으로, 수동이면 자동으로 바꿔주는 메소드
		if not self.autoTNH:
			self.autoTHcon.start(val)
			self.autoTNH = True
			print("온습도 자동모드")
		else:
			self.autoTHcon.stop()
			self.autoTNH = False
			print("온습도 수동모드")
			
	def autoLEDonoff(self, val):
		#자동이면 수동으로, 수동이면 자동으로 바꿔주는 메소드
		if not self.autoLED:
			self.autoLEDcon.start(val)
			self.autoLED = True
			print("조명 자동모드")
		else:
			self.autoLEDcon.stop()
			self.autoLED = False
			print("조명 수동모드")
			
	def notification(self,  content):
		if content == 'DATE' or content == 'STOP':
			self.voi.voiceFunc('DATE')
		if content == 'WEATHER' or content == 'STOP':
			self.voi.voiceFunc('WEATHER')
		elif content == 'TH':
			self.voi.voiceFunc(content)
			
		
	def properTH(self,val, th):
		#th  1: 온도 2: 습도
		if not autoTNH:
			if th == 1 :
				self.selfTHcon.properTemp()
			elif th == 2:
				self.selfTHcon.properHumi()
	
	def THUP(self,val, th , up = True, degree = 1):
		if not autoTNH:
			if th == 1 :
				self.selfTHcon.tempUP(up, degree)
			elif th == 2:
				self.selfTHcon.humidUP(up, degree)
	def ledonoff(self, lon = True):
		if self.autoLED:
			self.autoLEDonoff(None)
		self.selfLEDcon.on(lon)
		
	def setAlarm(self, timeStr):
		self.tictoc.userSet(timeStr)
		
	def offAlarm(self):
		self.tictoc.alarmStop()
		
if __name__ == "__main__" : 
	#mainloop = True
	#while mainloop:
	sbr = smartBedRoom()
	sbr.addSchdule(1, 18, hour = 5, minute = 16 )
	while True:
		sel = input("종료 0:")
		if sel == '0':
			sbr.notification("STOP")
			break
