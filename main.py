''' 2018. 01. 19  16:00  main'''
from BluetoothCommand import BluetoothCommand
from HumidifierClient import HumidifierClient
from smartBedRoom import smartBedRoom
from voiceFunc import voiceNot
import sys


def humidOn():
	'''global humidifier
	humidifier.on()'''
	HumidifierClient.on()
	
def humidOff():
	'''global humidifier
	humidifier.off()'''
	HumidifierClient.off()


def programExit():
	global bc
	bc.stopRecvCommand()
	bc.close()
	sys.exit()
	
def date():
	global sbr
	sbr.notification("DATE")
	print("date")
	
def weather(): ##날씨 구현 완료
	global sbr
	sbr.notification("WEATHER")

def morningCall(): ##모닝콜 재구현
	global sbr, bc, voice
	print("모닝콜설정")
	voice.voiceFunc("ANY", "모닝콜 설정입니다.")
	voice.voiceFunc("ANY", "몇시 몇분으로 설정할지 숫자 4개를 입력하세요.")
	hour= []
	hour.append(BluetoothCommand.binToUtf8(bc.client_sock.recv(1024)))
	hour.append(BluetoothCommand.binToUtf8(bc.client_sock.recv(1024)))
	
	minute= []
	minute.append(BluetoothCommand.binToUtf8(bc.client_sock.recv(1024)))
	minute.append(BluetoothCommand.binToUtf8(bc.client_sock.recv(1024)))
	
	tempList = hour[:]+minute[:]
	
	try:
		hour = int("".join(hour))
		minute = int("".join(minute))
		if not (0<=hour<=23 and 0<=minute<=59):
			voice.voiceFunc("ANY", "잘못입력해서 모닝콜 설정을 종료합니다.")
			return None
			
	except :
		voice.voiceFunc("ANY", "잘못입력해서 모닝콜 설정을 종료합니다.")
		return None
		
	voice.voiceFunc("ANY", "입력한 시간이 %d시 %d분이 맞는지 예 아니오를 누르세요" % (hour, minute))
	answer = BluetoothCommand.binToUtf8(bc.client_sock.recv(1024))
	if answer == "yes" :
		
		#sbr.addSchdule(1, 18, hour, minute)	
		sbr.setAlarm("".join(tempList))
		voice.voiceFunc("ANY", "모닝콜이 설정되었습니다.")
	else :
		voice.voiceFunc("ANY", "모닝콜 설정을 종료합니다.")
		
	
def lightOff():
	global sbr
	print("lightOff")
	sbr.ledonoff(False)

def lightOn():
	global sbr
	print("lightOn")
	sbr.ledonoff(True)
	
def offAlarm():
	global sbr
	sbr.offAlarm()
	sbr.notification("WEATHER")
	print("Func offAlarm")
	
def tempHumi(): ## 온습도 구현완료
	global sbr
	sbr.notification("TH")
	


def autoTempHumi():
	global sbr
	sbr.autoTHonoff(None)
def autoLED():
	global sbr
	sbr.autoLEDonoff(None)

## 가습기 제어 인스턴스 생성
try:
	humidifier = HumidifierClient()	
except:
	print("가습기 제어 기기에서 블루투스나 서버프로그램을 실행했는지 확인하세요!!")
	sys.exit(0)

##기능통합인스턴스 생성
sbr = smartBedRoom()
##음성출력인스턴스 생성
voice = voiceNot()
##폰-라즈 블루투스 인스턴스 생성
try:
	bc=BluetoothCommand()
except:
	print("이 프로그램은 root권한이 필요합니다. sudo명령어를 이용해 실행하세요!!")
	sys.exit(0)
	

	
	
'''
##인자없는 명령어 추가
bc.addCommand("time", func0)
##인자 1개인 명령어 추가
bc.addCommand("weather", func1, 10000)
##인자 여려개인 명령어 추가
bc.addCommand("lightON", func3, (10000, 20000, 30000))
'''

bc.addCommand("EXIT", programExit)
bc.addCommand("date", date)
bc.addCommand("weather", weather)
bc.addCommand("morningCall", morningCall)
bc.addCommand("humidOn", humidOn)
bc.addCommand("humidOff", humidOff)
bc.addCommand("lightOff", lightOff)
bc.addCommand("lightOn", lightOn)
bc.addCommand("offAlarm", offAlarm)
bc.addCommand("tempHumi", tempHumi)
bc.addCommand("autoTempHumi", autoTempHumi)
bc.addCommand("autoLED", autoLED)
##기기 접속대기
bc.waitConnection()
## LED제어 자동모드
sbr.autoLEDonoff(None)
##명령받기모드 시작
bc.runRecvCommand()
'''
##명령받기모드 종료
bc.stopRecvCommand()

##블루투스통신 종료
bc.close()
'''
	

