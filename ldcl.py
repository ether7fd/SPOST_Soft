import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

def loadcell():
    global hx
    #hx = HX711(PIN_DAT, PIN_CLK)
    # データの並び順を指定
    #hx.set_reading_format("MSB", "MSB")
    #hx.set_reference_unit(referenceUnit)
    #hx.reset()
    #hx.tare()
    
    listload = []
    for x in range(10):
        try:
            # Prints the weight.
            val = hx.get_weight(5)
            # データの表示
            #print("val:%f" % val)
            listload.append(val)
            hx.power_down()
            hx.power_up()
            time.sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
    
    return max(listload)