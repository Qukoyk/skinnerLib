#!/usr/bin/python3

#import文
import RPi.GPIO as GPIO
from time import sleep
import time

#ポート設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#実験開始プロセス
answer2 = input("今回の番号は？:\n")
print ("始めますか？")
answer = input("Press y:\n")
while True:
	if answer == "y":
		print ("")
		print ("=======START!========")
		print ("")	
		break
	else:
		sleep(0.01)
		
#初期化数据
trail = 1
time0 = time.time()														#始まりの時間
time2 = time.time()														#前回反応の時間点
day = time.strftime("%Y-%m-%d")

#データ保存先を指定
mydata = []
myfile = open(day+"."+answer2 + '.txt','w')	

#メインプログラム
try:
	while True:
		if GPIO.input(24) == GPIO.HIGH:									#押すと
			GPIO.output(25, GPIO.HIGH)									#LEDライトのポートに 3.3v の電流を
			time1 = time.time()											#反応瞬間の時間
			print ("Trail ",trail)										#試行数
			print ("Time ",time1-time0)									#最初からかかっていた時間
			print ("TimeBetween ",time1-time2)							#反応間かかった時間
			print ("")
			trail = trail+1
			time2 = time.time()
			mydata = [
				str(trail-1),
				str(
					(
					time.strftime
						("%Y-%m-%d %H:%M:%S", time.localtime()
						)
					)
				),''
			]
			for line in mydata:
				myfile.write(line + '\n')
			while GPIO.input(24) == GPIO.HIGH:							#「保護わく」
				sleep(0.01)												#同じ

		else:
			GPIO.output(25, GPIO.LOW)
		sleep(0.01)

#終了		
except KeyboardInterrupt:
			pass

#ポート釈放			
GPIO.cleanup()
