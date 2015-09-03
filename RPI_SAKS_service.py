#!/usr/bin/env python
# coding=utf-8
# 

import RPi.GPIO as GPIO
import time
import threading
import os, sys
import string

# 使用BCM编码
GPIO.setmode(GPIO.BCM)
LED_D1 		= 5
LED_D2 		= 6
LED_D3 		= 13
LED_D4 		= 19
LED_D5 		= 0
LED_D6 		= 1
LED_D7 		= 7
LED_D8 		= 8
BUZZER_B1 	= 11
KEY_K1 		= 23
KEY_K2 		= 18
KEY_K3 		= 24
KEY_K4 		= 25
LED_A 		= 21
LED_B 		= 16
LED_C 		= 19
LED_D 		= 6
LED_E 		= 5
LED_F 		= 20
LED_G 		= 26
LED_DP		= 13
LED_COM1 	= 17
LED_COM2 	= 27
LED_COM3 	= 22
LED_COM4 	= 10
IR_LED 		= 12
IR_RECEIVER = 9
DS18B20 	= 4
UART_TXD 	= 14
UART_RXD 	= 15
IC2_SDA 	= 2
IC2_SLC 	= 3

# 预设变量
LED_OFF = -1 # 数码管关闭
NUM = [{0:LED_OFF, 1:LED_OFF, 2:LED_OFF, 3:1, 'p0':False, 'p1':False, 'p2':False, 'p3':False}, 
	   {0:LED_OFF, 1:LED_OFF, 2:LED_OFF, 3:2, 'p0':False, 'p1':False, 'p2':False, 'p3':False},
	   {0:LED_OFF, 1:LED_OFF, 2:LED_OFF, 3:3, 'p0':False, 'p1':False, 'p2':False, 'p3':False},
	   {0:LED_OFF, 1:LED_OFF, 2:LED_OFF, 3:4, 'p0':False, 'p1':False, 'p2':False, 'p3':False}]

def init():
	# 电源按钮
	GPIO.setup(KEY_K1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(LED_D7, GPIO.OUT, initial = GPIO.HIGH)
	GPIO.setup(LED_D8, GPIO.OUT, initial = GPIO.HIGH)
	# 数码管显示模式选择开关
	GPIO.setup(KEY_K3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(KEY_K4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	# 数码管位选
	GPIO.setup(LED_COM1, GPIO.OUT, initial = GPIO.HIGH)
	GPIO.setup(LED_COM2, GPIO.OUT, initial = GPIO.HIGH)
	GPIO.setup(LED_COM3, GPIO.OUT, initial = GPIO.HIGH)
	GPIO.setup(LED_COM4, GPIO.OUT, initial = GPIO.HIGH)
	# 数码管段选
	GPIO.setup(LED_A, GPIO.OUT, initial = GPIO.HIGH)
	GPIO.setup(LED_B, GPIO.OUT, initial = GPIO.HIGH)
	GPIO.setup(LED_C, GPIO.OUT, initial = GPIO.HIGH)
	GPIO.setup(LED_D, GPIO.OUT, initial = GPIO.HIGH)
	GPIO.setup(LED_E, GPIO.OUT, initial = GPIO.HIGH)
	GPIO.setup(LED_F, GPIO.OUT, initial = GPIO.HIGH)
	GPIO.setup(LED_G, GPIO.OUT, initial = GPIO.HIGH)
	GPIO.setup(LED_DP, GPIO.OUT, initial = GPIO.HIGH)


def deinit():
	GPIO.cleanup()


# 电源按钮点击事件
def powerButtonClick(channel):
	global powerButtonClickTimes, powerCountDown
	powerButtonClickTimes += 1
	# 等待确认
	if powerButtonClickTimes == 1:
		print "If you really want to reboot or shut down please continue click!"
		powerCountDown = 3
	# 重启模式
	if powerButtonClickTimes == 2:
		GPIO.output(LED_D7, GPIO.LOW)
		GPIO.output(LED_D8, GPIO.HIGH)
		print "System will restart in 10s!"
		powerCountDown = 10
	# 关机模式
	if powerButtonClickTimes == 3:
		GPIO.output(LED_D7, GPIO.HIGH)
		GPIO.output(LED_D8, GPIO.LOW)
		print "System will halt in 10s!"
		powerCountDown = 10
	# 模式取消
	if powerButtonClickTimes == 4:
		GPIO.output(LED_D7, GPIO.HIGH)
		GPIO.output(LED_D8, GPIO.HIGH)
		print "Cancel"
		powerButtonClickTimes = 0
		powerCountDown = 10


# 电源按钮响应服务
def powerButton():
	global powerButtonClickTimes, powerCountDown
	powerButtonClickTimes = 0
	powerCountDown = 10
	while True:
		# 等待确认
		if powerButtonClickTimes == 1 and powerCountDown == 0:
			print "Cancel"
			powerButtonClickTimes = 0
		# 重启模式if
		if powerButtonClickTimes == 2 and powerCountDown == 0:
			print "Reboot"
			os.system("reboot")
			sys.exit()
		# 关机模式
		if powerButtonClickTimes == 3 and powerCountDown == 0:
			print "Halt"
			os.system("halt")
			sys.exit()
		if powerButtonClickTimes == 1 or powerButtonClickTimes == 2 or powerButtonClickTimes == 3:
			print powerCountDown
			powerCountDown -= 1
			time.sleep(1)
		else:
			time.sleep(0.2)


# 数码管段选函数
def setWE(n, p):
	GPIO.output(LED_A, GPIO.HIGH)
	GPIO.output(LED_B, GPIO.HIGH)
	GPIO.output(LED_C, GPIO.HIGH)
	GPIO.output(LED_D, GPIO.HIGH)
	GPIO.output(LED_E, GPIO.HIGH)
	GPIO.output(LED_F, GPIO.HIGH)
	GPIO.output(LED_G, GPIO.HIGH)
	GPIO.output(LED_DP, GPIO.HIGH)
	if p:
		GPIO.output(LED_DP, GPIO.LOW)
	if n == 0:
		GPIO.output(LED_A, GPIO.LOW)
		GPIO.output(LED_B, GPIO.LOW)
		GPIO.output(LED_C, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		GPIO.output(LED_E, GPIO.LOW)
		GPIO.output(LED_F, GPIO.LOW)
	if n == 1:
		GPIO.output(LED_B, GPIO.LOW)
		GPIO.output(LED_C, GPIO.LOW)
	if n == 2:
		GPIO.output(LED_A, GPIO.LOW)
		GPIO.output(LED_B, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		GPIO.output(LED_E, GPIO.LOW)
		GPIO.output(LED_G, GPIO.LOW)
	if n == 3:
		GPIO.output(LED_A, GPIO.LOW)
		GPIO.output(LED_B, GPIO.LOW)
		GPIO.output(LED_C, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		GPIO.output(LED_G, GPIO.LOW)
	if n == 4:
		GPIO.output(LED_B, GPIO.LOW)
		GPIO.output(LED_C, GPIO.LOW)
		GPIO.output(LED_F, GPIO.LOW)
		GPIO.output(LED_G, GPIO.LOW)
	if n == 5:
		GPIO.output(LED_A, GPIO.LOW)
		GPIO.output(LED_C, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		GPIO.output(LED_F, GPIO.LOW)
		GPIO.output(LED_G, GPIO.LOW)
	if n == 6:
		GPIO.output(LED_A, GPIO.LOW)
		GPIO.output(LED_C, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		GPIO.output(LED_E, GPIO.LOW)
		GPIO.output(LED_F, GPIO.LOW)
		GPIO.output(LED_G, GPIO.LOW)
	if n == 7:
		GPIO.output(LED_A, GPIO.LOW)
		GPIO.output(LED_B, GPIO.LOW)
		GPIO.output(LED_C, GPIO.LOW)
	if n == 8:
		GPIO.output(LED_A, GPIO.LOW)
		GPIO.output(LED_B, GPIO.LOW)
		GPIO.output(LED_C, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		GPIO.output(LED_E, GPIO.LOW)
		GPIO.output(LED_F, GPIO.LOW)
		GPIO.output(LED_G, GPIO.LOW)
	if n == 9:
		GPIO.output(LED_A, GPIO.LOW)
		GPIO.output(LED_B, GPIO.LOW)
		GPIO.output(LED_C, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		GPIO.output(LED_F, GPIO.LOW)
		GPIO.output(LED_G, GPIO.LOW)

# 数码管位选函数
def setP0(n):
	GPIO.output(LED_COM1, GPIO.HIGH)
	GPIO.output(LED_COM2, GPIO.HIGH)
	GPIO.output(LED_COM3, GPIO.HIGH)
	GPIO.output(LED_COM4, GPIO.HIGH)
	if n == 0:
		GPIO.output(LED_COM1, GPIO.LOW)
	if n == 1:
		GPIO.output(LED_COM2, GPIO.LOW)
	if n == 2:
		GPIO.output(LED_COM3, GPIO.LOW)
	if n == 3:
		GPIO.output(LED_COM4, GPIO.LOW)

# 数码管显示服务
def show():
	i = 0
	while True:
		if GPIO.input(KEY_K3):
			if GPIO.input(KEY_K4):
				mode = 0
			else:
				mode = 1
		else:
			if GPIO.input(KEY_K4):
				mode = 2
			else:
				mode = 3
		if i == 0:
			setP0(i)
			setWE(NUM[mode][0], NUM[mode]['p0'])
		if i == 1:
			setP0(i)
			setWE(NUM[mode][1], NUM[mode]['p1'])
		if i == 2:
			setP0(i)
			setWE(NUM[mode][2], NUM[mode]['p2'])
		if i == 3:
			setP0(i)
			setWE(NUM[mode][3], NUM[mode]['p3'])
			i = -1
		time.sleep(0.004)
		i = i + 1


# 时间获取函数
def getTime():
	lastSec = 0
	while True:
		localtime = time.localtime(time.time())
		NUM[0][1] = localtime.tm_hour % 10
		NUM[0][0] = (localtime.tm_hour - NUM[0][1]) / 10
		NUM[0][3] = localtime.tm_min % 10
		NUM[0][2] = (localtime.tm_min - NUM[0][3]) /10
		if lastSec == localtime.tm_sec:
			time.sleep(0.02)
		else:
			NUM[0]['p1'] = True
			lastSec = localtime.tm_sec
			time.sleep(0.35)
			NUM[0]['p1'] = False


# CPU温度获取函数
def getCPUTemp():
	while True:
		ts = os.popen('vcgencmd measure_temp').readline()
		t = string.atof(ts.replace("temp=","").replace("'C\n",""))
		t = t * 10
		NUM[1][3] = t % 10
		t = (t - NUM[1][3]) / 10
		NUM[1][2] = t % 10
		t = (t - NUM[1][2]) / 10
		NUM[1][1] = t % 10
		NUM[1]['p2'] = True
		time.sleep(0.5)


def main():
	# 添加电源按钮服务线程
	powerButtonThread = threading.Thread(target = powerButton)
	powerButtonThread.setDaemon(True)
	powerButtonThread.start()
	GPIO.add_event_detect(KEY_K1, GPIO.RISING, callback = powerButtonClick, bouncetime = 200) # 注册电源按钮监听事件

	# 添加时间刷新服务线程
	getTimeThread = threading.Thread(target = getTime)
	getTimeThread.setDaemon(True)
	getTimeThread.start()
	# 添加CPU温度刷新服务线程
	getCPUTempThread = threading.Thread(target = getCPUTemp)
	getCPUTempThread.setDaemon(True)
	getCPUTempThread.start()
	# 添加数码管显示服务线程
	showThread = threading.Thread(target = show)
	showThread.setDaemon(True)
	showThread.start()

	print "You can press Ctrl+c or input \"exit\" to close this service!"
	try:
		while True:
			usrCmd = raw_input(">")
			if usrCmd == "exit":
				return
	except KeyboardInterrupt:
	    print "User press Ctrl+c, exit!"


if __name__ == "__main__":
	init()
	main()
	deinit()

