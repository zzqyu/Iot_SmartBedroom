''' 2018. 01. 18  15:00  class HumidifierClient'''
##가습기 제어 서버에 접속해서 가습기 제어 신호 보냄
import bluetooth
##가습기 제어 클라이언트
class HumidifierClient:
	clientCnt = 0
	def __init__(self):
		if HumidifierClient.clientCnt == 0:
			HumidifierClient.classInit()
		HumidifierClient.clientCnt+=1
		
	def __del__(self):
		HumidifierClient.sendExit()
		HumidifierClient.sock.close()
		
	def classInit():
		HumidifierClient.state = False
		bd_addr = "B8:27:EB:5A:DB:65" ##가습기 블루투스 맥주소
		port =3 
		HumidifierClient.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		HumidifierClient.sock.connect((bd_addr, port))
		print("가습기 제어 준비 완료")
		
	def on():
		HumidifierClient.sock.send("ON")
		HumidifierClient.state = True
		
	def off():
		HumidifierClient.sock.send("OFF")
		HumidifierClient.state = False
	def sendExit():
		HumidifierClient.sock.send("EXIT")
		HumidifierClient.state = False
		
	def isState():
		return HumidifierClient.state

import time
	##테스트코드
if __name__ == "__main__" :
	humidifier = HumidifierClient()
	while True:
		print("On")
		humidifier.on()
		time.sleep(1)
		
		print("Off")
		humidifier.off()
		time.sleep(1)