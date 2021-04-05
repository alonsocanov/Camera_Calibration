import unittest
import camera
import calibrate
import utils
import numpy as np
import os
import cv2


class TestCameraCalibration(unittest.TestCase):

    # def testVideoCapture(self):
    #     print('\nTesting video capture')

    #     dir_path = utils.create_dir('webcam')
    #     path = os.path.join(dir_path, 'video.avi')
    #     camera.captureVideo(0, path=path)

    # def testPhotoCapture(self):
    #     print('\nTesting capturing photos')
    #     dir_path = utils.create_dir('webcam')
    #     num_img = 1
    #     fps = 1
    #     camera.captureImage(0, num_img=num_img, fps=fps,
    #                         save_dir=save_dir)

    # def testCalibration(self):
    #     print('\nTesting camera calibration')
    #     photos_path = 'logi_720_v2'
    #     logi_720 = Calibrate(img_dir=photos_path)
    #     mtx, new_mtx, dist, roi = logi_720.calibrate()
    #     logi_720.save('camera_matrix.txt', mtx)
    #     logi_720.save('new_camera_matrix.txt', new_mtx)
    #     logi_720.save('camera_distortion.txt', dist)
    #     logi_720.save('region_of_interest.txt', roi)

    # def testFishEyeCalibration(self):
    #     print('\nTesting camera calibration for fish eye')
    #     fish_path = 'pi_fish_eye'
    #     fish = Calibrate(img_dir=fish_path)
    #     mtx, new_mtx, dist, roi = fish.calibrate_fish_eye()
    #     fish.save('camera_matrix.txt', mtx)
    #     fish.save('new_camera_matrix.txt', new_mtx)
    #     fish.save('camera_distortion.txt', dist)
    #     fish.save('region_of_interest.txt', roi)

    # def testUndisort(self):
    #     photos_path = 'rasp_pi'
    #     logi_720 = Calibrate(img_dir=photos_path)
    #     mtx, new_mtx, dist, roi = logi_720.calibrate()
    #     img_path = '/'.join([logi_720.directoy, 'img_1.jpg'])
    #     img = cv2.imread(img_path)
    #     img_undisort = logi_720.undisort(img, mtx, new_mtx, dist, roi)

    # def testFishEyeUndisort(self):
    #     fish_path = 'pi_fish_eye'
    #     fish = Calibrate(img_dir=fish_path)
    #     mtx, new_mtx, dist, roi = fish.calibrate_fish_eye()
    #     img_path = '/'.join([fish.directoy, 'img_1.jpg'])
    #     img = cv2.imread(img_path)
    #     img_undisort = fish.undisort_fish_eye(
    #         img, mtx, new_mtx, dist, roi)


if __name__ == '__main__':
    unittest.main()
