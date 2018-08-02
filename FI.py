#!/usr/bin/python3

'''
FI.py
基礎統制libのFIスクリプト

デフォルトはFI10s, ITI10s, 10試行
'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"


#前置き宣言
x = 10 # FI x s
iti = 10 # ITI 10s
trailsMax = 10 # 総回数

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
trail = 0
timeCount = 0
time0 = time.time()
time2 = time.time()
timePast = 0
day = time.strftime("%Y-%m-%d")

with open(day + "_" + answer2 + '.csv' , 'a+') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(['Trail','Time'])
    
#データ保存先を指定
leverLeftActData = []

#メインプログラム
try:
    while True:
        GPIO.output(leverLeftMove,GPIO.LOW)
        for timeCount in range(x):
            print (timeCount+1,"s/",x,"s")
            sleep(1)
        while GPIO.input(leverLeftAct) == GPIO.LOW:
            sleep(0.01)

        if GPIO.input(leverLeftAct) == GPIO.HIGH:
            GPIO.output(feeder,GPIO.HIGH)
            time1 = time.time()
            trail = trail+1
            timePast = round(time1-time0,2)
            print ("Trail ",trail,"/",trailsMax)
            print ("Time ",timePast,"\n")
            time2 = time.time()
            leverLeftActData = [str(trail),str(timePast)]
            with open(day+"_"+answer2+'.csv','a+') as myfile:
                writer = csv.writer(myfile)
                writer.writerow(leverLeftActData)
            print ("ITI",iti,"s:\n")
            GPIO.output(leverLeftMove,GPIO.HIGH)
            sleep(iti)
            time0 = time.time()
            while GPIO.input(leverLeftAct) == GPIO.HIGH:
                sleep(0.01)

        if trail == trailsMax:
            myfile.close()
            GPIO.cleanup()
            break

        else:
            GPIO.output(feeder,GPIO.HIGH)
        sleep(0.01)

# 終了
except KeyboardInterrupt:
    pass

#ポート釈放
myfile.close()
GPIO.cleanup()