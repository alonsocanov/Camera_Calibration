import unittest
from camera import Camera
from calibrate import Calibrate

class TestCameraCalibration(unittest.TestCase):
    def testVideoCapture(self):
        camera = Camera(save=False, save_path='', file_name='')
        fps = 24
        camera.captureVideo(fps=fps)

    def testPhotoCapture(self):
        camera = Camera(save=False, save_path='', file_name='')
        num_img = 1
        fps = 1
        camera.captureImage(num_img=num_img, fps=fps)

    def testCalibration(self):
        photos_path = 'logi_720'
        camera = Calibrate(save=False, path=photos_path, file_name='')
        camera.calibrate()

    # def testUndisort(self):
    #     photos_path = 'logi_720'
    #     camera = Calibrate(save=False, path=photos_path, file_name='')
    #     camera.undisort()


if __name__ == '__main__':
    unittest.main()
