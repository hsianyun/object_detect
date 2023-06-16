from picamera2 import Picamera2
from time import time, sleep
import torch
import numpy as np
from ultralytics import YOLO


class ObjectDetection:

    def __init__(self):

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)

        self.model = self.load_model()

        self.CLASS_NAMES_DICT = self.model.model.names

    def load_model(self):

        model = YOLO("can_detect_n.pt")  # load a pretrained YOLOv8n model
        model.fuse()

        return model

    def predict(self, frame):

        results = self.model(frame)

        return results

    def __call__(self):

        camera = Picamera2()
        camera.configure(camera.create_preview_configuration(
            main={"format": 'RGB888', "size": (640, 480)}))
        camera.start()

        # warmup
        sleep(0.1)
        count = 0

        while True:

            start_time = time()

            frame = camera.capture_array()
            results = self.predict(frame)
            if len(results[0].boxes.xyxyn) > 0:
                cor = [float(xyxy) for xyxy in results[0].boxes.xyxyn[0]]
                print(cor)

            end_time = time()
            fps = 1/np.round(end_time - start_time, 2)
            print(f'FPS: {fps}')

            count += 1
            if count > 50:
                break


if __name__ == '__main__':
    detection = ObjectDetection()
    detection()
