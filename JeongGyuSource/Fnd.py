import smbus2 as smbus
import time
from threading import Thread
import re ##문자 정규식 처리


class Fnd:
	def __init__(self):
		Fnd.bus = smbus.SMBus(1)
		Fnd.addr = 0x20
		Fnd.config_port = 0x06
		Fnd.out_port = 0x02
		Fnd.unitSec = 0.001
		
		Fnd.reCondition = re.compile("[0-9 .]")
		
		self.threadSignal = False
		self.loopThread = None
		
		Fnd.bus.write_word_data(Fnd.addr, Fnd.config_port, 0x0000)
		
	def isCorrectString(inputStr):
		return len(inputStr) == len(Fnd.reCondition.findall(inputStr))
		
	##쓰레드 종료 시그널 보내기
	def sendThreadKillSignal(self, isKill):
		self.threadSignal = isKill
	##쓰레드 종료 시그널 받기
	def recvThreadKillSignal(self):
		return self.threadSignal
		
	## 출력(쓰레드) 종료 
	def outputStop(self):
		if self.loopThread!=None:
			self.sendThreadKillSignal(True)
			self.loopThread.join()
			self.sendThreadKillSignal(False)
		Fnd.bus.write_word_data(Fnd.addr, Fnd.out_port, 0)
		

	## Fnd 출력 값 세팅
	def intToOutDisp(num, digit, dot):
			#             0     1      2     3      4     5     6     7     8     9
		data = (0xFC,0x60,0xDA,0xF2,0x66,0xB6,0x3E,0xE0,0xFE,0xF6)
		#         seg1, seg2, seg3, seg4, seg5, seg6
		digitCode = (0x7F, 0xBF, 0xDF, 0xEF,  0xF7, 0xFB)
		
		return (data[num] |int(dot))<< 8 | digitCode[digit]
		
	## 한 세트(세그먼트6개) 출력
	def loopOutput(sixDigitsList):
		outputList = sixDigitsList[:]
		if outputList[0]==".":
			pass
		else :
			for i in range(6):
				if outputList[i]==" ":
					continue
				dot = False
				## 점 추가 작업 시작
				if len(outputList)!=i+1 and outputList[i+1]=="." :
					dot=True
					outputList.pop(i+1)
				##끝
				
				##출력값 받아오기
				out_disp = Fnd.intToOutDisp(int(outputList[i]), i, dot)
				##출력
				Fnd.bus.write_word_data(Fnd.addr, Fnd.out_port, out_disp)
				##0.001 sleep
				time.sleep(Fnd.unitSec)
		
	##인자로 받은 문자열을 처리해 출력		
	def strToOutput(self, inputStr, sec=0):
		def run():
			totalTime = 0
			condition = True
			if sec>0:
				condition = totalTime<sec		
			while condition:
				Fnd.loopOutput(list(inputStr))
				totalTime+=Fnd.unitSec*6
				condition = bool(  (int(self.recvThreadKillSignal())+1) %2  )
		
		if not Fnd.isCorrectString(inputStr):
			print("잘못된 문자열이 섞여있습니다. ")
		else :
		
			excludePointLen = len(inputStr)-inputStr.count(".")
			inputStr = " "*(6-excludePointLen)+inputStr
			if excludePointLen>6 :
				self.flowOutput(inputStr, False)
			else :
				self.loopThread = Thread(target = run)
				self.loopThread.start()	
		
	'''	
	def intToOutput(self, num, sec=0, isEmptyZero=False):
		def run():
			numStr = ("%6d" % num)
			if isEmptyZero:
				numStr = ("%06d" % num)
			totalTime = 0
			condition = True
			if sec>0:
				condition = totalTime<sec		
			while condition:
				Fnd.loopOutput(numStr)
				totalTime+=Fnd.unitSec*6
				condition = bool(  (int(self.recvThreadKillSignal())+1) %2  )
		if len(str(num))>6 :
			self.flowOutput(num, False)
		else :
			self.loopThread = Thread(target = run)
			self.loopThread.start()	
	'''		
	
	def flowOutput(self, inputStr, direcRight=True, changeSec=0.5,  sec=0):
		
		def run():
			if type(inputStr) == type(" "):
				strList = list(inputStr+"   ")
				
			elif len(str(num))>4 :
				strList = list(str("%d   " % inputStr))
			else :
				strList = list(str("%6d" % inputStr))
			totalTime ,totalChangeSec = 0, 0
			condition = True
			
			if sec>0:
				condition = totalTime<sec
			while condition:
				Fnd.loopOutput(strList)
				totalTime+=Fnd.unitSec*6
				totalChangeSec+=Fnd.unitSec * 6
				condition = bool(  (int(self.recvThreadKillSignal())+1) %2  )
				if totalChangeSec>changeSec:
					totalChangeSec=0
					if direcRight:
						strList.insert(0, strList.pop()) ##오른쪽으로
					else :
						strList.append(strList.pop(0)) ##왼쪽으로
				
		if not Fnd.isCorrectString(inputStr):
			print("잘못된 문자열이 섞여있습니다. ")
		else :
			self.loopThread = Thread(target = run)
			self.loopThread.start()	
		
	
##테스트코드
if __name__ == "__main__" :
	f=Fnd()
	try:
		while True:
			inputNum = input("숫자를 입력하세요: ")
			f.outputStop()
			f.strToOutput(inputNum)
		
	except KeyboardInterrupt:
		f.outputStop()
		pass