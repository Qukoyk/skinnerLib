#!/usr/bin/python3

'''
magazineShaping.py

行動形成用スクリプト
'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"


iti = 10

# ポート宣言
leverLeftAct = 22
leverLeftMove = 17
leverRightAct = 23
leverRightMove = 18
lightLeft = 6
lightRight = 12
houseLight = 24
feeder = 27
buzzer = 25
handShaping = 5

# import文
import RPi.GPIO as GPIO
from time import sleep
import time
import csv

# ポート設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(feeder, GPIO.OUT)
GPIO.setup(leverLeftMove, GPIO.OUT)
GPIO.setup(leverRightMove, GPIO.OUT)
GPIO.setup(handShaping, GPIO.OUT)
GPIO.setup(leverLeftAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leverRightAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(leverLeftMove, GPIO.HIGH)
GPIO.output(leverRightMove, GPIO.HIGH)

# 実験開始プロセス
answer2 = input("今回の番号は？:\n")
print("始めますか？")
answer = input("Press y:\n")
while True:
    if answer == "y":
        print("")
        print("=======START!========")
        print("")
        break
    else:
        sleep(0.1)

# 初期化数据
trail = 0
time0 = time.time()  # 始まりの時間
time2 = time.time()  # 前回反応の時間点
day = time.strftime("%Y-%m-%d")
with open(day + "_" + answer2 + '.csv', 'a+') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(['Trail', 'Switches', 'Time'])

# データ保存先を指定
ratLeverData = []
handShapingData = []


# メインプログラム
try:
	while True:
		if trail < 50:
			GPIO.output(leverLeftMove, GPIO.LOW)
			if GPIO.input(leverLeftAct) == GPIO.HIGH:  # 押すと
				GPIO.output(feeder, GPIO.HIGH)
				time1 = time.time()  # 反応瞬間の時間
				trail = trail + 1
				print("Trail ", trail)  # 試行数
				print("leftLever")
				print("Time ", round(time1 - time0, 2))  # 最初からかかっていた時間
				print("")
				# GPIO.output(23,GPIO.HIGH)       #Feeder on
				time2 = time.time()
				ratLeverData = [str(trail), str("leftLever"),
								str(round(time1 - time0, 2))]
				with open(day + "_" + answer2 + '.csv', 'a+') as myfile:
					writer = csv.writer(myfile)
					writer.writerow(ratLeverData)
				while GPIO.input(leverLeftAct) == GPIO.HIGH:  # 「保護わく」
					sleep(0.01)  # 同じ
				#GPIO.output(leverLeftMove, GPIO.HIGH)
				#sleep(iti)

		if trail >= 50:
			GPIO.output(leverLeftMove, GPIO.HIGH)
			GPIO.output(leverRightMove, GPIO.LOW)
			if GPIO.input(leverRightAct) == GPIO.HIGH:
				GPIO.output(feeder, GPIO.HIGH)
				time1 = time.time()
				trail = trail + 1
				print("Trail ", trail)
				print("rightLever")
				print("Time ", round(time1 - time0, 2), "\n")
				time2 = time.time()
				ratLeverData = [str(trail), str("rightLever"),
				                    str(round(time1 - time0, 2))]
				with open(day + "_" + answer2 + '.csv', 'a+') as myfile:
					writer = csv.writer(myfile)
					writer.writerow(ratLeverData)
				while GPIO.input(leverRightAct) == GPIO.HIGH:  # 「保護わく」
					sleep(0.01)  # 同じ
				GPIO.output(leverRightMove, GPIO.HIGH)
				#sleep(iti)

		if GPIO.input(handShaping) == GPIO.HIGH:
			GPIO.output(feeder, GPIO.HIGH)
			time1 = time.time()
			print("Trail ", trail)
			print("handShaping")
			print("Time ", round(time1 - time0, 2))
			print("")
			time2 = time.time()
			handShapingData = [
				str(trail - 1), str("handShaping"), str(round(time1 - time0, 2))]
			with open(day + "_" + answer2 + '.csv', 'a+') as myfile:
				writer = csv.writer(myfile)
				writer.writerow(handShapingData)
			while GPIO.input(handShaping) == GPIO.HIGH:
				sleep(0.01)

		if trail >= 100:
			myfile.close()
			break

		else:
			GPIO.output(feeder, GPIO.LOW)
		sleep(0.1)


# 終了
except KeyboardInterrupt:
    pass

# ポート釈放
myfile.close()
GPIO.cleanup()
