import os
import cv2
import sys
import glob
import numpy as np
import undisort_images as ui
from camera import Camera


class Calibrate:
    def __init__(self, save: bool = False, path: str = '', file_name: str = '') -> None:

        self._save = save
        self._file_name = file_name
        self._path = path
        self._cur_dir = os.path.abspath(os.path.dirname(__file__))
        if path:
            path = [self._cur_dir, self._path, self._file_name]
            self._file_path = '/'.join(path)
            path = [self._cur_dir, self._path]
            self._dir_path = '/'.join(path)
        else:
            path = [self._cur_dir, self._file_name]
            self._file_path = '/'.join(path)
            path = [self._cur_dir]
            self._dir_path = '/'.join(path)

    @property
    def check_Q(self) -> bool:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        return False

    def crop(self, img, h_dim, w_dim):
        w, h, _ = img.shape
        img = img[h_dim[0]:h_dim[1], w_dim[0]:w_dim[1], :]
        # Resize the image
        img = cv2.resize(img, (h, w))

    def calibrate(self, num_rows: int = 9, num_cols: int = 6, dimension: int = 30, extension: str = 'jpg', show_img: bool = False) -> None:
        path = ''.join([self._dir_path, '/*.', extension])
        images = glob.glob(path)
        # chessboard grid
        grid = (num_cols, num_rows)
        # filter size
        filt = (5, 5)
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, dimension, .1)
        # prepare object points
        objp = np.zeros((1, num_cols * num_rows, 3), np.float32)
        objp[0, :, :2] = np.mgrid[0:num_cols, 0:num_rows].T.reshape(-1, 2)
        # Arrays to store object points and image points from all the images.
        # 3d point in real world space
        obj_pts = []
        # 2d points in image plane.
        img_pts = []
        # save the name of the image with bad chess bord detection
        img_bad = None
        # number of imges
        print('Provided images: ', len(images))
        if len(images) < 9:
            print('Not enough images, at least 9 images must be given')
            sys.exit()

        for image in images:
            # Read Image
            img = cv2.imread(image)
            # convert to gray scale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(
                gray, grid, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
            # If found, add object points, image points (after refining them)
            if ret:
                obj_pts.append(objp)
                corners2 = cv2.cornerSubPix(
                    gray, corners, filt, (-1, -1), criteria)
                img_pts.append(corners2)
                # Draw and display the corners
                if show_img:
                    img = cv2.drawChessboardCorners(img, grid, corners2, ret)
                    cv2.imshow('img', img)
                    cv2.waitKey(500)
                if img_bad is None:
                    img_bad = image
            else:
                img_bad = image
        cv2.destroyAllWindows()

        # read image
        img = cv2.imread(img_bad)
        print('Useful images: ', len(obj_pts))
        print('Image dimensions: ', img.shape)
        # undisort images usin finctions from undisort images
        mtx, dist, undistoted_img = self.undisort(
            obj_pts, img_pts, img)
        # save resuts in a .txt file
        camera_matrix = ''.join([self._dir_path, '/', 'camera_matrix', '.txt'])
        np.savetxt(camera_matrix, mtx, delimiter=',')
        camera_distortion = ''.join(
            [self._dir_path, '/', 'camera_distortion', '.txt'])
        np.savetxt(camera_distortion, np.transpose(dist), delimiter=',')

        cv2.imshow('Undisorted Image', undistoted_img)
        while not self.check_Q:
            pass
        cv2.destroyAllWindows()

    def undisort(self, obj_pts, img_pts, img):
        if len(obj_pts) > 1:
            h, w, _ = img.shape
            # Undistort an image
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
                obj_pts, img_pts, (w, h), None, None)
            #cv2.imshow('Disorted Image', img)
            # cv2.waitKey(500)

            new_mtx, roi = cv2.getOptimalNewCameraMatrix(
                mtx, dist, (w, h), 1, (w, h))
            undisorted_img = cv2.undistort(img, mtx, dist, None, new_mtx)
            # Crop image
            if roi[0]:
                x, y, w, h = roi
                undisorted_img = undisorted_img[y:y + h, x:x + w]

            print('ROI: ', roi)
            print('Calibration Matrix: ')
            print(mtx)
            print('New Camera Martrix:')
            print(new_mtx)
            print('Disortion: ')
            print(dist)

            # Distortion Error
            mean_error = 0
            for i in range(len(obj_pts)):
                img_pts2, _ = cv2.projectPoints(
                    obj_pts[i], rvecs[i], tvecs[i], mtx, dist)
                error = cv2.norm(img_pts[i], img_pts2,
                                cv2.NORM_L2) / len(img_pts2)
                mean_error += error

            print('Total error: ', mean_error / len(obj_pts))
        else:
            print('Not enough images')
            mtx, dist, rvecs, tvecs, undisorted_img = 0, 0, 0, 0, 0

        return mtx, dist, undisorted_img


    def undisort_fish_eye_v1(self, obj_pts, img_pts, img):
        calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND + cv2.fisheye.CALIB_FIX_SKEW
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)

        nb_img = len(obj_pts)
        h, w = img.shape[:2]
        mtx = np.zeros((3, 3))
        dist = np.zeros((4, 1))
        rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(nb_img)]
        tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(nb_img)]
        rms, _, _, _, _ = cv2.fisheye.calibrate(obj_pts, img_pts, (w, h), mtx, dist, rvecs, tvecs, calibration_flags, criteria)

        map1, map2 = cv2.fisheye.initUndistortRectifyMap(mtx, dist, np.eye(3), mtx, (w, h), cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

        print('Calibration Matrix: ')
        print(mtx)
        print('Disortion: ')
        print(np.transpose(dist))

        return mtx, dist, undistorted_img



    def undisort_fish_eye_v2(self, obj_pts, img_pts, img):
        calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND + cv2.fisheye.CALIB_FIX_SKEW
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)

        h, w = img.shape[:2]
        nb_img = len(obj_pts)
        mtx = np.zeros((3, 3))
        dist = np.zeros((4, 1))
        rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(nb_img)]
        tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(nb_img)]
        rms, _, _, _, _ = cv2.fisheye.calibrate(obj_pts, img_pts, (w, h), mtx, dist, rvecs, tvecs, calibration_flags, criteria)

        # Undistort an image
        balance = 1
        dim1 = img.shape[:2][::-1]
        dim2 = (int(dim1[0] / 1.1), int(dim1[1] / 1.1))
        dim3 = (int(dim1[0] / 1), int(dim1[1] / 1))

        if dim2 == None:
            dim2 = dim1
        if dim3 == None:
            dim3 = dim1

        scaled_mtx = mtx * dim1[0] / w
        scaled_mtx[2][2] = 1

        new_mtx = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_mtx, dist, dim2, np.eye(3), balance=balance)
        mapx, mapy = cv2.fisheye.initUndistortRectifyMap(scaled_mtx, dist, np.eye(3), new_mtx, dim3, cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, mapx, mapy, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

        print('Calibration Matrix: ')
        print(mtx)
        print('Disortion: ')
        print(np.transpose(dist))

        return mtx, dist, undistorted_img
