from Interface import serialInterface
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.IN)


serial = serialInterface()
while True:
    read = serial.SerialReadString()
    print(read)
    serial.SerialWriteString('Hello')
    sleep(1)
