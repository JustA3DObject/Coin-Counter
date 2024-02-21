import cv2
import cvzone
import numpy as np

img = cv2.imread("test_images\\20240221_202713.jpg")
img = cv2.resize(img, (800,600))

# def empty(a):
#     pass
# cv2.namedWindow("Settings")
# cv2.resizeWindow("Settings", 640,240)
# cv2.createTrackbar("Threshold1", "Settings", 111, 255, empty)
# cv2.createTrackbar("Threshold2", "Settings", 255, 255, empty)

def preProcessing(img):

    imgPre = cv2.addWeighted(img, 1.1, np.zeros(img.shape, img.dtype), 0, 50) 
    imgPre = cv2.GaussianBlur(imgPre, (5,5), 5)
    # threshold1 = cv2.getTrackbarPos("Threshold1", "Settings")
    # threshold2 = cv2.getTrackbarPos("Threshold2", "Settings")
    imgPre = cv2.Canny(imgPre, 75,175)
    kernel = np.ones((3,3), np.uint8)
    imgPre = cv2.dilate(imgPre, kernel, iterations=2)
    imgPre = cv2.morphologyEx(imgPre, cv2.MORPH_CLOSE, kernel)

    return imgPre

imgPre = preProcessing(img)
imgContours, conFound = cvzone.findContours(img, imgPre, minArea=20)

if conFound:
    for contour in conFound:
        peri = cv2.arcLength(contour['cnt'], True)
        approx = cv2.approxPolyDP(contour['cnt'], 0.02*peri, True)

        if len(approx) > 6:
            print(contour['area'])

stackedImage = cvzone.stackImages([img, imgPre, imgContours],2,0.5)
cv2.imshow("Image", stackedImage)

cv2.waitKey(0)
cv2.destroyAllWindows()