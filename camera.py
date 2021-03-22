import os
import cv2
import sys
import glob
import numpy as np
import time


class Camera:
    def __init__(self, pipeline=0, api=None) -> None:

        self.pipeline = pipeline
        self.api = api

    def check_webcam_avalability(self, webcam: cv2.VideoCapture) -> None:
        if not webcam.isOpened():
            print("Error opening webcam")
            webcam.release()
            sys.exit(1)

    def check(self, char: str = 'q') -> bool:
        if cv2.waitKey(1) & 0xFF == ord(char):
            return True
        return False

    def captureVideo(self, fps) -> None:
        webcam = cv2.VideoCapture(0)
        width = int(webcam.get(3))
        height = int(webcam.get(4))

        self.check_webcam_avalability(webcam)
        if self._save:
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            save_path = ''.join([self._file_path, '.avi'])
            out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
        while True:
            try:
                # capture each frame
                ret, frame = webcam.read()
                if ret:
                    # display frame
                    cv2.imshow('Frame', frame)
                    if self._save:
                        out.write(frame)
                    if self.check:
                        break
                else:
                    break
            except KeyboardInterrupt:
                print('Interrupted')
                break
        # After the loop release the video and out object
        webcam.release()
        if self._save:
            out.release()
        # Destroy all windows
        cv2.destroyAllWindows()

    def captureImage(self, num_img: int = 1, fps: int = 1, save_dir='', img_name='img', file_type='.jpg', show_img=False) -> None:
        if not self.api:
            webcam = cv2.VideoCapture(self.pipeline)
        else:
            webcam = cv2.VideoCapture(self.pipeline, self.api)
        self.check_webcam_avalability(webcam)
        if show_img:
            time.sleep(fps)
        for i in range(num_img):
            try:
                ret, frame = webcam.read()
                if not ret:
                    print('Unable to get image')
                    sys.exit(1)
                if save_dir:
                    image_name = ''.join([img_name, '_', str(i), file_type])
                    path = '/'.join([save_dir, image_name])
                    cv2.imwrite(filename=path, img=frame)
                if show_img:
                    cv2.imshow("Captured Image", frame)
                    cv2.waitKey(int(fps * 1000))
                if self.check:
                    break
            except KeyboardInterrupt:
                print("Interrupted")
                break
        webcam.release()
        cv2.destroyAllWindows()
