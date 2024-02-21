import cv2
import cvzone
import requests 
import numpy as np 
import imutils 

# Replace the below URL with your own. Make sure to add "/shot.jpg" at last. 
url = "http://192.168.1.8:8080/shot.jpg"

totalMoney = 0

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
    imgPre = cv2.Canny(imgPre, 60,150)
    kernel = np.ones((3,3), np.uint8)
    imgPre = cv2.dilate(imgPre, kernel, iterations=1)
    imgPre = cv2.morphologyEx(imgPre, cv2.MORPH_CLOSE, kernel)

    return imgPre

# While loop to continuously fetching data from the Url 
while True: 
    img_resp = requests.get(url) 
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
    img = cv2.imdecode(img_arr, -1) 

    img = imutils.resize(img, width=800, height=600) 
    imgPre = preProcessing(img)
    imgContours, conFound = cvzone.findContours(img, imgPre, minArea=20)

    if conFound:
        for contour in conFound:
            peri = cv2.arcLength(contour['cnt'], True)
            approx = cv2.approxPolyDP(contour['cnt'], 0.02*peri, True)

            if len(approx) > 6:
                area = contour['area']
                print(area)
                
                # if area

    stackedImage = cvzone.stackImages([img, imgPre, imgContours],2,0.5)
    cv2.imshow("Image", stackedImage)

    # Press Esc key to exit 
    if cv2.waitKey(1) == 27: 
        break
cv2.destroyAllWindows()




