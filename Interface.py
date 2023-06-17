import serial
from time import sleep
# these codes are for bluetooth
# hint: please check the function "sleep". how does it work?


class serialInterface:
    def __init__(self):
        self.ser = serial.Serial()
        self.port = '/dev/ttyAMA0'
        self.do_connect(self.port)
        self.ser.reset_input_buffer()

    def do_connect(self, port):
        self.ser.close()
        print("Connecting...")
        try:
            self.ser = serial.Serial(port, 9600, timeout=2)
            print("connect success")
            print("")
        except serial.serialutil.SerialException:
            print("fail to connect")
            print("")
            return False
        return True

    def disconnect(self):
        self.ser.close()

    def SerialWriteString(self, data: str):
        send = data.encode("utf-8")
        self.ser.write(send)

    def SerialWriteBytes(self, data: bytes):
        self.ser.write(data)

    def SerialReadString(self):
        waiting = self.ser.in_waiting
        if waiting >= 0:
            line = self.ser.readline().decode('utf-8').rstrip()
            return line
        return ""

    def SerialReadByte(self):
        sleep(0.05)
        waiting = self.ser.in_waiting
        rv = self.ser.read(waiting)
        if (rv):
            readByte = hex(int.from_bytes(rv, byteorder='big', signed=False))
            self.ser.flushInput()
            return readByte
        else:
            return 0
