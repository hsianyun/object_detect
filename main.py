from Interface import serialInterface
from ObjectDetect import ObjectDetection

class Main:
    def __init__(self):
        self.ser = serialInterface()
        self.detect = ObjectDetection(self.ser)

    def run(self):
        msg = self.ser.SerialReadString()
        if msg == 'Detected.':
            self.detect()

if __name__ == '__main__':
    main = Main()
    while True:
        main.run()