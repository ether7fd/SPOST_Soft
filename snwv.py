import time
import RPi.GPIO as GPIO

#-----Tyouonpa
inteTyou = 0.5
signaloff = 0
signalon = 0
TRIG = 18
ECHO = 16

def tyouonpa():
    global signaloff
    global signalon
    
    GPIO.setwarnings(False)
     
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, GPIO.LOW)
    #time.sleep(0.2)
        
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        signaloff = time.time()
        
    while GPIO.input(ECHO) == 1:
        signalon = time.time()

    timepassed = signalon - signaloff
    distance = timepassed * 17000
    #GPIO.cleanup()
    return distance
