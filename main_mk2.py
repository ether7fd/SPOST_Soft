#!/usr/bin/env python
import time
import os
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

import spidev
from time import sleep

import sprd
import mvservo
import jud
import opcv
import ldcl
import snwv
#import psmt
import scrn
import lint

#-----Roadcell
#PIN_DAT = 5
#PIN_CLK = 6
PIN_DAT = 29
PIN_CLK = 31
referenceUnit = 177 #<=算出した値
#--------------

interTyou = 0.5
RotVal = []
omosa = 0
atusa = 0

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

def calcatusa(rot): #-----------potention meta- max -> atusa calculation
    if rot < 0.1:
        return 1
    else :
        return 3

def sokumain():
    atusa = calcatusa(max(RotVal))
    print(atusa)
    #omosa = loadcell()
    #print(omosa)
    size = opcv.sizeopencv()
    if size[0] > size[1]:
        naga = size[0]
        mizika = size[1]
    else :
        naga = size[1]
        mizika = size[0]
    print(naga, mizika)
    kingaku = jud.judge(naga, mizika, atusa, omosa)
    print(kingaku)
    scrn.screenpri(kingaku, atusa, omosa, naga, mizika)
    mvservo.moveservo()
    lint.send_line_notify("郵便物が投函されました！")
    sprd.wrspr(naga, mizika, atusa, omosa, kingaku)
    
    return 0

def main():
    global omosa
    global atusa
    global RotVal
    RotVal.append(0)

    hx = HX711(PIN_DAT, PIN_CLK)
    #-----setupLoad()
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()
    #----------------
    #-----setupPotentionmeta
    #V_REF = 3.29476 # input Voltage
    V_REF = 5.0
    CHN = 0 # 接続チャンネル

    spi = spidev.SpiDev()
    spi.open(0, 0) # 0：SPI0、0：CE0
    spi.max_speed_hz = 1000000 # 1MHz SPIのバージョンアップによりこの指定をしないと動かない

    #------------------------

    old = time.time()
    try:
        while True:
            now = time.time()
            # preGlobalCounter = globalCounter
            
            #--------Measuring Potention me-ta--------------
            dout = spi.xfer2([((0b1000+CHN)>>2)+0b100,((0b1000+CHN)&0b0011)<<6,0]) # Din(RasPi→MCP3208）を指定
            bit12 = ((dout[1]&0b1111) << 8) + dout[2] # Dout（MCP3208→RasPi）から12ビットを取り出す
            volts = round((bit12 * V_REF) / float(4095),4)  # 取得した値を電圧に変換する（12bitなので4095で割る）
            RotVal.append(volts)
            #print(volts)

            if((now-old) > interTyou): #interval inteTyou
                tyou = snwv.tyouonpa()
                print(tyou)
                if tyou < 15 and tyou > 10:
                    GPIO.setmode(GPIO.BOARD)
                    GPIO.setup(11, GPIO.OUT)
                    GPIO.output(11, 1)

                    #GPIO.cleanup() #Rotary gpio clean
                    #setupLoad()
                    #print(max(RotVal))
                    spi.close()
                    #-----loadcell
                    sleep(3)
                    listload = []
                    for x in range(10):
                        try:
                            # Prints the weight.
                            val = hx.get_weight(5)
                            # データの表示
                            print("val:%f" % val)
                            listload.append(val)
                            hx.power_down()
                            hx.power_up()
                            time.sleep(0.1)
                        except (KeyboardInterrupt, SystemExit):
                            cleanAndExit()
                    
                    omosa = max(listload)
                    #--------------
                    #print(RotVal)

                    sokumain() #測定メインプログラム
                    
                    #------------全行程終了後，初期化
                    RotVal = []
                    RotVal.append(0)
                    # globalCounter = 0
                    GPIO.output(11, 0)
                    GPIO.cleanup()
                    hx = HX711(PIN_DAT, PIN_CLK)
                    #-----setupLoad()
                    hx.set_reading_format("MSB", "MSB")
                    hx.set_reference_unit(referenceUnit)
                    hx.reset()
                    hx.tare()
                    spi.open(0, 0) # 0：SPI0、0：CE0
                    #----------------
                old = time.time()

    except KeyboardInterrupt:
       print("Catch 'KeyboardInterrupt'")
    
    print("End process")

    return 0
        
if __name__ == "__main__":
    main()
