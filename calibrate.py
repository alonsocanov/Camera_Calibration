import os
import cv2
import sys
import glob
import numpy as np
import undisort_images as ui
from camera import Camera

class Calibrate:
    def __init__(self, save: bool=False, path: str='', file_name: str='') -> None:
        
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
    
    def calibrate(self, num_rows:int=9, num_cols:int=6, dimension:int=30, extension:str='jpg', show_img:bool=False) -> None:
        path = ''.join([self._dir_path, '/*.', extension])
        images = glob.glob(path)
        # chessboard grid
        grid = (num_cols, num_rows)
        # filter size
        filt = (5, 5)
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, dimension, .1)
        # prepare object points
        objp = np.zeros((1, num_cols * num_rows, 3), np.float32)
        objp[0, :, :2] = np.mgrid[0:num_cols, 0:num_rows].T.reshape(-1, 2)
        # Arrays to store object points and image points from all the images.
        # 3d point in real world space
        objpoints = []
        # 2d points in image plane.
        imgpoints = []
        # save the name of the image with bad chess bord detection
        img_bad = None
        # number of imges
        print ('Provided images: ', len(images))
        if len(images) < 9:
            print ('Not enough images, at least 9 images must be given')
            sys.exit()
        
        for image in images:
            # Read Image
            img = cv2.imread(image)
            # convert to gray scale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, grid, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
            # If found, add object points, image points (after refining them)
            if ret:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, filt, (-1, -1), criteria)
                imgpoints.append(corners2)
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
        print('Useful images: ', len(objpoints))
        print('Image dimensions: ', img.shape)
        # undisort images usin finctions from undisort images
        mtx, dist, undistoted_img = ui.udisort_normal(objpoints, imgpoints, img)
        # save resuts in a .txt file
        camera_matrix = ''.join([self._dir_path,'/','camera_matrix','.txt'])
        np.savetxt(camera_matrix, mtx, delimiter=',')
        camera_distortion = ''.join([self._dir_path,'/','camera_distortion','.txt'])
        np.savetxt(camera_distortion, np.transpose(dist), delimiter=',')
        
        cv2.imshow('Undisorted Image', undistoted_img)
        while not self.check_Q:
            pass
        cv2.destroyAllWindows()