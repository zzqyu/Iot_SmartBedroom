#1 온습도 모듈 temp humi

import smbus2 as smbus
import time
import RPi.GPIO as GPIO
from threading import Thread
from HumidifierClient import HumidifierClient

addr = 0x40

cmd_temp = 0xf3
cmd_humi = 0xf5
soft_reset = 0xfe

temp = 0.0
humi = 0.0
val = 0
data = [0, 0]
	
class I2Cth:

	
	def __init__(self):
		self.bus = smbus.SMBus(1)
		self.bus.write_byte (addr, soft_reset)
		time.sleep(0.260)
		
	def checkTemp(self):
		# temperature
		self.bus.write_byte(addr, cmd_temp)
		time.sleep(0.260)
		for i in range(0, 2, 1):
			data[i] = self.bus.read_byte(addr)
		val = data[0] << 8 | data[1]
		temp = -46.85+175.72/65536*val
		
		return temp
	
	def checkHumi(self):
		self.bus.write_byte(addr, cmd_humi)
		time.sleep(0.260)
		
		for i in range(0,2,1):
			data[i] = self.bus.read_byte(addr)
		val = data[0] << 8 | data[1]
		humi = -6.0+125.0/65536*val;
		return humi
	

class Motor:
	GPIO_RP = 4
	GPIO_RN = 25
	GPIO_EN = 12
	
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.GPIO_RP = 4
		self.GPIO_RN = 25
		self.GPIO_EN = 12
		GPIO.setwarnings(False)
		GPIO.setup(self.GPIO_RP, GPIO.OUT)
		GPIO.setup(self.GPIO_RN, GPIO.OUT)
		GPIO.setup(self.GPIO_EN, GPIO.OUT)
		self.p = GPIO.PWM(self.GPIO_EN, 100)
		self.p.start(0)		
	def __del__(self):
		GPIO.cleanup()
	
	def setDir(self, cw):
		if cw:
			GPIO.output(self.GPIO_RP, True)
			GPIO.output(self.GPIO_RN, False)
		else:
			GPIO.output(self.GPIO_RP, False)
			GPIO.output(self.GPIO_RN, True)
		
		
	def shortBreak(self):
		GPIO.output(self.GPIO_EN, False)
		
	def stop(self):
		GPIO.output(self.GPIO_RP, False)
		GPIO.output(self.GPIO_RN, False)
		GPIO.output(self.GPIO_EN, True)
	
	def setSpeed(self, speedLevel):
		self.p.ChangeDutyCycle(speedLevel*10)
		
	
	def run(self, speedLevel, cw = True):
		self.setDir(cw)
		self.setSpeed(speedLevel)
		
class Humidifier:
	def on(self):
		HumidifierClient.on()
	def off(self):
		HumidifierClient.off()
		
	def isState(self):
		return HumidifierClient.isState()
		
		
