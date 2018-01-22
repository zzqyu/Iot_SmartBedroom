''' 2018. 01. 18  16:00  class BluetoothCommand'''
from bluetooth import *
import time
import types
import signal
import subprocess
from threading import Thread

##블루투스SSP통신과 명령을 관리하는 클래스
class BluetoothCommand:
	##생성자
	def __init__(self, clist={}):
			self.classInit(clist)
			
	##소멸자
	def __del__(self):
		self.close()
		
	def classInit(self, clist={}):
		self.loopThread = None
		self.client_sock = None
		self.commandList = None
		self.server_sock=BluetoothSocket( RFCOMM )
		
		##명령 묶음 초기화
		self.setCommandList(clist)
		
		self.server_sock.bind(("",1)) ##PORT_ANY
		self.server_sock.listen(1)
		
		self.port = self.server_sock.getsockname()[1]
		
		##채널 1번이 아닐때 블루투스 껐다 켬
		if self.port != 1:
			print("블루투스 채널  ch%d" % self.port)
			bluetoothStopCmd = ["sudo", "service", "bluetooth",  "stop"]
			subprocess.call(bluetoothStopCmd)
			time.sleep(2)
			bluetoothStartCmd = ["sudo", "service", "bluetooth",  "start"]
			subprocess.call(bluetoothStartCmd)
			
			
			print("블루투스 재시작 4초 대기")
			time.sleep(4)
			self.classInit()	
		else :
			uuid = "00000000-0000-1000-8000-00805F9B34FB"
			
			advertise_service( self.server_sock, "raspberrypi",
							   service_id = uuid,
							   service_classes = [ uuid, SERIAL_PORT_CLASS ],
							   profiles = [ SERIAL_PORT_PROFILE ],
							  )
		
	##블루투스 통신종료	
	def close(self):
		self.client_sock.close()
		self.server_sock.close()
	
	##명령어 묶음 세팅 함수
	def  setCommandList(self, clist):
		self.commandList=clist
		
	##명령어 추가 함수 (cmd: 명령어이름, funcName: 해당명령어의 실행 함수이름, args: 함수 인자)
	def addCommand(self, cmd, funcName, args=None):
		if args == None:
			self.commandList[cmd] = funcName
		else :
			self.commandList[cmd] = [funcName,  args]
		
	##블루투스 기기 접속 대기 함수				  
	def waitConnection(self):
		print("Waiting for connection on RFCOMM channel %d" % self.port)
		self.client_sock, client_info = self.server_sock.accept()
		print("[client_sock]", type(self.client_sock))
		print("Accepted connection from ", client_info)
	
	## 명령받기종료 함수
	def stopRecvCommand(self):
		if self.loopThread!=None:
			print("아래 오류 문구 무시")
			signal.pthread_kill(self.loopThread.ident, signal.SIGINT)
		
	##연결된 기기에서 명령을 받아 해당 명령의 함수를 실행하는 함수	
	def runRecvCommand(self):
		def run():
			try:
				while True:
					##연결 기기에서 받아온 메시지(바이너리)를  UTF8로 변경
					data = BluetoothCommand.binToUtf8(self.client_sock.recv(1024))
					if data == 'exit':
						break
					print("received [%s]" % data)
					if data in self.commandList.keys():
						BluetoothCommand.runFunction(self.commandList[data])
			except KeyboardInterrupt:
				pass
			except IOError:
				pass
			
		self.loopThread = Thread(target = run)
		self.loopThread.start()	

	##명령과 매칭된 함수 실행하는 함수
	def runFunction(funcComponent):
		##인자가 없을때
		if type(funcComponent) == types.FunctionType:
			funcComponent()
		else :
			##인자가 1개
			if type(funcComponent[1]) != tuple:
				funcComponent[0](funcComponent[1])
			##인자가 2개이상
			else:
				funcComponent[0](*(funcComponent[1]))
	## 바이너리 to utf8	
	def binToUtf8(data):
		# 바이너리 데이터를 utf-16으로 디코딩한다
		# 수직 탭을 삭제한다
		return data.decode("utf-8").replace(u"\u000B", u"")
		
		
def func0():
	print("func0 실행")
	
def func1(args0):
	print("func1 실행", args0)
	
def func2(args0, args1):
	print("func2 실행", args0, args1)
	
def func3(args0, args1, args2):
	print("func3 실행", args0, args1, args2)
		
##테스트코드
if __name__ == "__main__" :
	
	##인스턴스 생성시 명령어 추가
	bc=BluetoothCommand({"morningCall":[func2, (10000, 20000)]})
	##인자없는 명령어 추가
	bc.addCommand("time", func0)
	##인자 1개인 명령어 추가
	bc.addCommand("weather", func1, 10000)
	##인자 여려개인 명령어 추가
	bc.addCommand("lightON", func3, (10000, 20000, 30000))
	##기기 접속대기
	bc.waitConnection()
	##명령받기모드 시작
	bc.runRecvCommand()
	time.sleep(5)
	##명령받기모드 종료
	bc.stopRecvCommand()
	##블루투스통신 종료
	bc.close()
	

