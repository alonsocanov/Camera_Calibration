import cv2
# if we want to save photos set to true
save_photos = False
# value of pressed key
key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
# number of photos to take
nb_imgs = 25
# save path
cam_folder = "logi_720/"
key = cv2.waitKey(3000)
try:
    for i in range(nb_imgs):
        key = cv2.waitKey(1)
        check, frame = webcam.read()
        cv2.imshow("Captured Image", frame)
        if save_photos:
            nb_imgs = "img_" + str(i) + ".jpg"
            cv2.imwrite(filename=cam_folder + nb_imgs, img=frame)
        # see image for 2 seconds
        key = cv2.waitKey(2000)
        if key == ord('q'):
            print("Photos interrupted")
            break

except(KeyboardInterrupt):
    print("Photos interrupted")

print("Turning off camera...")
webcam.release()
print("Camera off.")
print("Program ended.")
cv2.destroyAllWindows()
