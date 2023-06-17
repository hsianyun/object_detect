from picamera2 import Picamera2
from time import time, sleep
import torch
import numpy as np
from Interface import serialInterface
from ultralytics import YOLO
from enum import IntEnum


class actions(IntEnum):
    LEFT = 1
    RIGHT = 2
    FRONT = 3
    BACK = 4
    THROW = 5


class ObjectDetection:

    def __init__(self):

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # self.ser = ser
        print("Using Device: ", self.device)

        self.model = self.load_model()

    def load_model(self):

        model = YOLO("can_detect_n.pt")  # load a pretrained YOLOv8n model
        model.fuse()

        return model

    def predict(self, frame):

        results = self.model(frame)

        return results

    def center_calculate(self, cor: list):
        cor_x = (cor[0]+cor[2])/2
        cor_y = (cor[1]+cor[3])/2
        return (cor_x, cor_y)

    def area_calculate(self, cor: list):
        delta_x = abs(cor[2]-cor[0])
        delta_y = abs(cor[3]-cor[1])
        area = delta_x * delta_y
        return area

    def direction(self, cor_x: float, cor_y: float, area: float):
        if 0 <= cor_x < 0.45:
            print('turn left')
            dir = actions.LEFT
        elif 0.55 <= cor_x <= 1:
            print('turn right')
            dir = actions.RIGHT
        elif 0.45 <= cor_x < 0.55:
            print('go forward or throw ball')
            if area > 0.25:
                print('throw ball')
                dir = actions.THROW
            else:
                print('Go forward')
                dir = actions.FRONT
        return dir

    def __call__(self):

        camera = Picamera2()
        camera.configure(camera.create_preview_configuration(
            main={"format": 'RGB888', "size": (640, 480)}))
        camera.start()

        # warmup
        sleep(0.1)
        notThrow = True

        while notThrow:

            start_time = time()

            frame = camera.capture_array()
            results = self.predict(frame)

            # If there is object detected
            if len(results[0].boxes.xyxyn) > 0:
                # coordinate:[x1,y1,x2,y2]
                cor = [float(xyxy) for xyxy in results[0].boxes.xyxyn[0]]
                center_x, center_y = self.center_calculate(
                    cor)  # calculate the center coordinate
                area = self.area_calculate(cor)  # calculate the object area

                # decide if we will throw the ball or move the car, and return if the ball is throwed
                # if the ball is throwed, notThrow = False
                action = self.direction(center_x, center_y, area)
                if action == actions.THROW:
                    #     # self.ser.SerialWriteString('e')
                    notThrow = False
                # elif action == actions.FRONT:
                #     self.ser.SerialWriteString('f')
                # elif action == actions.LEFT:
                #     self.ser.SerialWriteString('l')
                # elif action == actions.RIGHT:
                #     self.ser.SerialWriteString('r')
                print(f'x:{center_x:.2f} y:{center_y:.2f} Area:{area:.4f}')

            # if there is no object been detected
            else:
                # self.ser.SerialWriteString('r')
                print('NOt found. Turn right')

            end_time = time()
            fps = 1/np.round(end_time - start_time, 2)
            print(f'FPS: {fps}')


if __name__ == '__main__':
    detection = ObjectDetection()
    detection()
