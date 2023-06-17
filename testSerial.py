from Interface import serialInterface
from time import sleep

serial = serialInterface()
while True:
    read = serial.SerialReadString()
    print(read)
    sleep(1)
