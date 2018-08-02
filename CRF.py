#!/usr/bin/python3

'''
CRF_100Trials.py
基礎統制libのCRFスクリプト
'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"


#ポート宣言
ratLever = 21
handShaping = 20
feeder = 26

#import文
import RPi.GPIO as GPIO
from time import sleep
import time
import csv

#ポート設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(feeder, GPIO.OUT)
GPIO.setup(ratLever, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(handShaping, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
        sleep(0.1)
        
#初期化数据
trial = 0
time0 = time.time() #始まりの時間
time2 = time.time() #前回反応の時間点
day = time.strftime("%Y-%m-%d")
with open(day+"_"+answer2 + '.csv','a+') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(['Trial','Switches','Time'])

#データ保存先を指定
ratLeverData = []
handShapingData = []


#メインプログラム
try:
    while True:
        if GPIO.input(ratLever) == GPIO.HIGH: #押されると
            GPIO.output(feeder, GPIO.HIGH)
            time1 = time.time() #反応瞬間の時間
            trial = trial+1
            print ("Trial ",trial) #試行数
            print ("ratLever")
            print ("Time ",round(time1-time0,2)) #最初からかかっていた時間
            print ("")
            # GPIO.output(23,GPIO.HIGH)       #Feeder on
            time2 = time.time()
            ratLeverData = [str(trial),str("ratLever"),str(round(time1-time0,2))]
            with open(day+"_"+answer2 + '.csv','a+') as myfile:
                writer = csv.writer(myfile)
                writer.writerow(ratLeverData)
            while GPIO.input(ratLever) == GPIO.HIGH: #「保護わく」
                sleep(0.01)                          #同じ

        if GPIO.input(handShaping) == GPIO.HIGH:
            GPIO.output(feeder, GPIO.HIGH)
            time1 = time.time()
            trial = trial+1
            print ("Trial ",trial)
            print ("handShaping")
            print ("Time ",round(time1-time0,2))
            print ("")
            time2 = time.time()
            handShapingData = [str(trial-1),str("handShaping"),str(round(time1-time0,2))]
            with open(day+"_"+answer2 + '.csv','a+') as myfile:
                writer = csv.writer(myfile)
                writer.writerow(handShapingData)
            while GPIO.input(handShaping) == GPIO.HIGH:
                sleep(0.01)
        
        if trial == 100:
            myfile.close()
            break
            
        else:
            GPIO.output(feeder, GPIO.LOW)
			pass
        sleep(0.1)
        
    

#終了        
except KeyboardInterrupt:
    pass

#ポート釈放
myfile.close()    
GPIO.cleanup()