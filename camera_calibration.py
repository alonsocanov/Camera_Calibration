import numpy as np
import cv2
# import glob
import sys
import undisort_images as ui
import os


def main(img_names):
    # ---------------------- SET THE PARAMETERS
    # show detected chess corners
    show_fig = False
    # number of rows on ches board
    nRows = 9
    # number of columns on ches board
    nCols = 6
    #  dimension oc squares on chess bord - mm
    dimension = 30
    # ------------------------------------------
    print('Camera Calibration')
    # filter size
    filt = (5, 5)
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, dimension, .1)
    # prepare object points
    objp = np.zeros((1, nCols * nRows, 3), np.float32)
    objp[0, :, :2] = np.mgrid[0:nCols, 0:nRows].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    # 3d point in real world space
    objpoints = []
    # 2d points in image plane.
    imgpoints = []
    # save the name of the image with bad chess bord detection
    img_bad = None
    # number of imges
    print ('Provided images: ', len(img_names))
    if len(img_names) < 9:
        print ('Not enough images, at least 9 images must be given')
        sys.exit()

    for img_name in img_names:
        # Read Image
        img = cv2.imread(img_name)
        # convert to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (nCols, nRows), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, filt, (-1, -1), criteria)
            imgpoints.append(corners2)
            # Draw and display the corners
            if show_fig:
                img = cv2.drawChessboardCorners(img, (nCols, nRows), corners2, ret)
                cv2.imshow('img', img)
                cv2.waitKey(500)
            if img_bad is None:
                img_bad = fname
        else:
            img_bad = img_name

    cv2.destroyAllWindows()

    # read image
    img = cv2.imread(img_bad)
    print('Useful images: ', len(objpoints))
    print('Image dimension: ', img.shape[:2])
    # undisort images usin finctions from undisort images
    mtx, dist, undistoted_img = ui.udisort_normal(objpoints, imgpoints, img)
    path_cam_data = 'logi_720/'

    # save resuts in a .txt file
    filename = 'camera_matrix' + '.txt'
    np.savetxt(filename, mtx, delimiter=',')
    filename = 'camera_distortion' + '.txt'
    np.savetxt(filename, np.transpose(dist), delimiter=',')

    cv2.imshow('Undisorted Image', undistoted_img)
    # stop program by typing 'q'
    key = cv2.waitKey(1) & 0xFF
    while key != ord('q'):
        key = cv2.waitKey(1) & 0xFF

    print('End of Camera Calibration')


if __name__ == '__main__':
    # path to images
    img_path = 'logi_720/'
    img_type = '.jpg'
    # obtain images names from data where name terminates with .jpg
    img_names = [img_path + x for x in os.listdir(img_path) if img_type in x]
    main(img_names)
