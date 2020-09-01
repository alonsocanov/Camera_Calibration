import unittest
from camera import Camera
from calibrate import Calibrate
import numpy as np
import cv2


class TestCameraCalibration(unittest.TestCase):

    def testVideoCapture(self):
        print('\nTesting video capture')
        camera = Camera(save=False, save_path='', file_name='')
        fps = 24
        camera.captureVideo(fps=fps)

    def testPhotoCapture(self):
        print('\nTesting capturing photos')
        camera = Camera(save=False, save_path='', file_name='')
        num_img = 1
        fps = 1
        camera.captureImage(num_img=num_img, fps=fps)

    def testCalibration(self):
        print('\nTesting camera calibration')
        photos_path = 'rasp_pi'
        camera = Calibrate(save=False, path=photos_path, file_name='')
        camera.calibrate(fish_eye=False)

    def testFishEyeCalibration(self):
        print('\nTesting camera calibration for fish eye')
        fish_path = 'pi_fish_eye'
        camera = Calibrate(save=False, path=fish_path, file_name='')
        camera.calibrate(fish_eye=True)

    def testUndisort(self):
        photos_path = 'rasp_pi'
        camera = Calibrate(save=False, path=photos_path, file_name='')
        img_path = '/'.join([camera.directoy_path, 'img_1.jpg'])
        img = cv2.imread(img_path)
        mtx = camera.mtx
        new_mtx = camera.new_mtx
        dist = camera.dist
        roi = camera.roi
        img = camera.undisort(img, mtx, new_mtx, dist, roi, fish_eye=False)

    def testFishEyeUndisort(self):
        fish_path = 'pi_fish_eye'
        camera = Calibrate(save=False, path=fish_path, file_name='')
        img_path = '/'.join([camera.directoy_path, 'img_1.jpg'])
        mtx = camera.mtx
        new_mtx = camera.new_mtx
        dist = camera.dist
        roi = camera.roi
        img = cv2.imread(img_path)
        img = camera.undisort(img, mtx, new_mtx, dist, roi, fish_eye=True)


if __name__ == '__main__':
    unittest.main()
