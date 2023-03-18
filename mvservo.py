import time
import RPi.GPIO as GPIO
import sys

Servo_pin = 12                      #変数"Servo_pin"に12を格納

def moveservo():
    #GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Servo_pin, GPIO.OUT)     #GPIO18を出力モードに設定

    #PWMの設定
    #サーボモータSG90の周波数は50[Hz]
    Servo = GPIO.PWM(Servo_pin, 50)     #GPIO.PWM(ポート番号, 周波数[Hz])

    Servo.start(0)                      #Servo.start(デューティ比[0-100%])

    try:
        #servo_angle(-90)               #サーボモータ -90°
        angle = -60
        duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180   #角度からデューティ比を求める
        Servo.ChangeDutyCycle(duty)     #デューティ比を変更
        time.sleep(0.3)                 #0.3秒間待つ
        
        time.sleep(1)
        #servo_angle(-60)               #サーボモータ -60°
        #servo_angle(-30)               #サーボモータ -30°
        #servo_angle(0)                 #サーボモータ  0°
        
        angle = 0
        duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180   #角度からデューティ比を求める
        Servo.ChangeDutyCycle(duty)     #デューティ比を変更
        time.sleep(0.3)                 #0.3秒間待つ
        time.sleep(1)
        
        #servo_angle(30)                #サーボモータ  30°
        #servo_angle(60)                #サーボモータ  60°
        #servo_angle(90)                #サーボモータ  90°
    except KeyboardInterrupt:          #Ctrl+Cキーが押された
        Servo.stop()                   #サーボモータをストップ
        GPIO.cleanup()                 #GPIOをクリーンアップ
        sys.exit()                     #プログラムを終了
        
    Servo.stop()                   #サーボモータをストップ
    #GPIO.cleanup()                 #GPIOをクリーンアップ

def main():
    moveservo()

if __name__ == "__main__":
    main()
