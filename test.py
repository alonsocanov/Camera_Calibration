from camera import Camera
from calibrate import Calibrate


def main():
    # camera = Camera(save=False, save_path='logi_720', file_name='')
    # camera.captureVideo(fps=24)
    # camera.captureImage(1, 1)
    camera = Calibrate(save=False, path='logi_720', file_name='')
    camera.calibrate()

if __name__ == '__main__':
    main()
