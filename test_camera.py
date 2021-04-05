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
    #                         save_dir=dir_path)

    # def testCalibration(self):
    #     print('\nTesting camera calibration')
    #     dir_path = utils.get_file_dir()
    #     photos_path = utils.join_path(dir_path, 'logi_720_v2')
    #     files = utils.files_in_dir(photos_path, '.jpg')

    #     mtx, new_mtx, dist, roi = calibrate.calibrate(files)
    #     cam_mtx = utils.join_path(photos_path, 'camera_matrix.txt')
    #     calibrate.save(cam_mtx, mtx)
    #     new_cam_mtx = utils.join_path(photos_path, 'new_camera_matrix.txt')
    #     calibrate.save(new_cam_mtx, new_mtx)
    #     cam_dist = utils.join_path(photos_path, 'camera_distortion.txt')
    #     calibrate.save(cam_dist, dist)
    #     cam_roi = utils.join_path(photos_path, 'region_of_interest.txt')
    #     calibrate.save(cam_roi, roi)

    # def testFishEyeCalibration(self):
    #     print('\nTesting camera calibration for fish eye')
    #     dir_path = utils.get_file_dir()
    #     fish_path = utils.join_path(dir_path, 'pi_fish_eye_v2')
    #     files = utils.files_in_dir(fish_path, '.jpg')
    #     mtx, new_mtx, dist, roi = calibrate.calibrate_fish_eye(files)

    #     cam_mtx = utils.join_path(fish_path, 'camera_matrix.txt')
    #     calibrate.save(cam_mtx, mtx)
    #     new_cam_mtx = utils.join_path(fish_path, 'new_camera_matrix.txt')
    #     calibrate.save(new_cam_mtx, new_mtx)
    #     cam_dist = utils.join_path(fish_path, 'camera_distortion.txt')
    #     calibrate.save(cam_dist, dist)
    #     cam_roi = utils.join_path(fish_path, 'region_of_interest.txt')
    #     calibrate.save(cam_roi, roi)

    # def testUndisort(self):
    #     photos_path = 'logi_720_v2'
    #     dir_path = utils.get_file_dir()
    #     photos_path = utils.join_path(dir_path, photos_path)
    #     files = utils.files_in_dir(photos_path, '.jpg')
    #     mtx, new_mtx, dist, roi = calibrate.calibrate(files)
    #     img_path = utils.join_path(photos_path, 'img_1.jpg')
    #     img = cv2.imread(img_path)
    #     img_undisort = calibrate.undisort(img, mtx, new_mtx, dist, roi)

    # def testFishEyeUndisort(self):
    #     fish_path = 'pi_fish_eye_v2'
    #     dir_path = utils.get_file_dir()
    #     fish_path = utils.join_path(dir_path, fish_path)
    #     files = utils.files_in_dir(fish_path, '.jpg')
    #     mtx, new_mtx, dist, roi = calibrate.calibrate_fish_eye(files)
    #     img_path = utils.join_path(fish_path, 'img_1.jpg')
    #     img = cv2.imread(img_path)
    #     img_undisort = calibrate.undisort_fish_eye(
    #         img, mtx, new_mtx, dist, roi)


if __name__ == '__main__':
    unittest.main()
