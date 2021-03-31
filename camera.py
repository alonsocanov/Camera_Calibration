import os
import cv2
import sys
import glob
import numpy as np
import time
from utils import sys_exit


def check_webcam_avalability(webcam: cv2.VideoCapture) -> None:
    if not webcam.isOpened():
        webcam.release()
        sys_exit(message)


def check_key(char: str = 'q') -> bool:
    if cv2.waitKey(1) & 0xFF == ord(char):
        return True
    return False


def scale(dim: tuple, scale: float):
    if not isinstance(dim, tuple) or len(dim) != 2:
        message = ' '.join(['Dimension must be a tuple and of lenght 2:', dim])
        sys_exit(message)
    return(int(dim[0] * scale), int(dim[1] * scale))


def resize(img: np.ndarray, dim: tuple):
    if not isinstance(dim, tuple) or len(dim) != 2:
        message = ' '.join(['Dimension must be a tuple and of lenght 2:', dim])
        sys_exit(message)
    return cv2.resize(img, dim)


def save_video(file_path, fps=24, dim):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(file_path, fourcc, fps, (dim[0], dim[1]))
    return out


def captureVideo(fps=24, save_dir: str = '', video_name: str = 'video', show_frame: bool = False, time: float = None):
    if not self.api:
        webcam = cv2.VideoCapture(self.pipeline)
    else:
        webcam = cv2.VideoCapture(self.pipeline, self.api)
    check_webcam_avalability(webcam)

    width, height = scale((int(webcam.get(3)), int(webcam.get(4))))

    if save_dir:
        vid_name = ''.join([video_name, '.avi'])
        path = '/'.join([save_dir, vid_name])
        out = save_video(path, fps=24, (width, height))
    while True:
        try:
            # capture each frame
            ret, frame = webcam.read()
            if not ret:
                message = 'Could not get frame'
                sys_exit(message)
            frame = resize(frame, (width, height))
            # display frame
            if show_frame:
                cv2.imshow('Frame', frame)
            if save_dir:
                out.write(frame)
            if check_key():
                break
        except KeyboardInterrupt:
            print('Interrupted')
            break
    # After the loop release the video and out object
    webcam.release()
    if save_dir:
        out.release()
    # Destroy all windows
    cv2.destroyAllWindows()


def captureImage(pipeline, api=None, num_img: int = 1, fps: int = 1, save_dir='', img_name='img', file_type='.jpg', show_img=False):
    if not api:
        webcam = cv2.VideoCapture(pipeline)
    else:
        webcam = cv2.VideoCapture(pipeline, api)
    check_webcam_avalability(webcam)
    if show_img:
        time.sleep(fps)
    for i in range(num_img):
        try:
            ret, frame = webcam.read()
            if not ret:
                message = 'Unable to get image'
                sys_exit(message)

            if save_dir:
                image_name = ''.join([img_name, '_', str(i), file_type])
                path = '/'.join([save_dir, image_name])
                cv2.imwrite(filename=path, img=frame)
            if show_img:
                cv2.imshow("Captured Image", frame)
                cv2.waitKey(int(fps * 1000))
            if check_key():
                break
        except KeyboardInterrupt:
            print("Interrupted")
            break
    webcam.release()
    cv2.destroyAllWindows()
