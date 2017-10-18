#!/usr/bin/python3

'''
VR.py
基礎統制libのVRスクリプト

デフォルトはVR10, ITI10s, 10試行
'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"


#前置き宣言
x = 10 # VR x
iti = 10 # ITI 10s
trialsMax = 10 # 総試行数

#ポート宣言
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

#import文
import RPi.GPIO as GPIO
from time import sleep
import time
import csv
import math,random

#ポート設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(feeder, GPIO.OUT)
GPIO.setup(leverLeftMove, GPIO.OUT)
GPIO.setup(leverRightMove, GPIO.OUT)
GPIO.setup(lightLeft, GPIO.OUT)
GPIO.setup(lightRight, GPIO.OUT)
GPIO.setup(houseLight, GPIO.OUT)
GPIO.setup(leverLeftAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leverRightAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(handShaping, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(leverLeftMove,GPIO.HIGH)

average = 0
myList = []
tenList = []

# 乱数生成
for values in range(1, 55):
    # gauss = random.gauss(x,math.sqrt(trialsMax))   #正規分布に従う乱数
    # myList.append(int(gauss))                #を使いたいならこれ
    myList.append(values)                      #そしてこれをコメントアウト

print ("乱数生成中……")

try:
    while True:
        tenList = random.sample(myList, trialsMax)
        average = sum(tenList) / trialsMax

        if average == float(x):
            print(tenList)
            print("average= ",average)
            break

except KeyboardInterrupt:
    pass

#実験開始プロセス
answer2 = input("今回の番号は？:\n")
print ("始めますか？")
answer = input("Press y:\n")
while True:
	if answer == "y":
		print ("")
		print ("=======START!=======")
		print ("")
		break
	else:
		sleep(0.1)
		
#データ初期化
trial = 0
react = 0
time0 = time.time()
time2 = time.time()
timePast = 0
day = time.strftime("%Y-%m-%d")
listPosition = 0


with open(day + "_" + answer2 + '.csv' , 'a+') as myfile:
	writer = csv.writer(myfile)
	writer.writerow(['Trial','Time'])
	
#データ保存先を指定
leverLeftActData = []


#メインプログラム
try:
	while True:
		GPIO.output(leverLeftMove,GPIO.LOW)
		if GPIO.input(leverLeftAct) == GPIO.HIGH:
			react = react + 1
			print(react,"/",tenList[listPosition])
			if react == tenList[listPosition]:
				GPIO.output(feeder,GPIO.HIGH)
				react = 0
				time1 = time.time()
				trial = trial+1
				listPosition = listPosition + 1
				timePast = round(time1-time0,2)
				print ("Trial ", trial,"/",trialsMax)
				print ("Time ",timePast,"\n")
				time2 = time.time()
				leverLeftActData = [str(trial),str(timePast)]
				with open(day+"_"+answer2+'.csv','a+') as myfile:
					writer = csv.writer(myfile)
					writer.writerow(leverLeftActData)
				while GPIO.input(leverLeftAct) == GPIO.HIGH:
					sleep(0.01)
				print ("ITI",iti,"s","\n")
				GPIO.output(leverLeftMove,GPIO.HIGH)
				sleep(iti)
				time0 = time.time()
			while GPIO.input(leverLeftAct) == GPIO.HIGH:
				sleep(0.01)
				
			if trial == trialsMax:
				myfile.close()
				break
				
		else:
			GPIO.output(feeder,GPIO.HIGH)
		sleep(0.01)	
		

#終了
except KeyboardInterrupt:
	pass
	
#ポート釈放
myfile.close()
GPIO.cleanup()
