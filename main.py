import cv2
import cvzone
import requests 
import numpy as np 
import imutils 

# Replace the below URL with your own. Make sure to add "/shot.jpg" at last. 
url = "http://192.168.1.5:8080//shot.jpg"

totalMoney = 0

# def empty(a):
#     pass
# cv2.namedWindow("Settings")
# cv2.resizeWindow("Settings", 640,240)
# cv2.createTrackbar("Threshold1", "Settings", 111, 255, empty)
# cv2.createTrackbar("Threshold2", "Settings", 255, 255, empty)

def preProcessing(img):

    imgPre = cv2.addWeighted(img, 1.2, np.zeros(img.shape, img.dtype), 0, 45) 
    imgPre = cv2.GaussianBlur(imgPre, (5,5), 5)
    # threshold1 = cv2.getTrackbarPos("Threshold1", "Settings")
    # threshold2 = cv2.getTrackbarPos("Threshold2", "Settings")
    imgPre = cv2.Canny(imgPre, 60,130)
    kernel = np.ones((4,4), np.uint8)
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

    totalMoney = 0
    if conFound:
        for contour in conFound:
            peri = cv2.arcLength(contour['cnt'], True)
            approx = cv2.approxPolyDP(contour['cnt'], 0.02*peri, True)

            if len(approx) > 6:
                area = contour['area']

                # print(area)

                if area < 9000:
                    totalMoney += 1
                elif 10700 < area < 10800:
                    totalMoney += 1
                elif 10500 < area < 10850:
                    totalMoney += 1
                elif 10600 < area < 10900:
                    totalMoney += 2
                elif 9000 < area < 10800:
                    totalMoney += 5
                elif 11000 < area < 12000:
                    totalMoney += 5
                elif area > 12000:
                    totalMoney += 10
        # print(totalMoney)

    stackedImage = cvzone.stackImages([img, imgPre, imgContours],2,0.5)
    cvzone.putTextRect(stackedImage, f'Rs. {totalMoney}', (50,50))
    cv2.imshow("Image", stackedImage)

    # Press Esc key to exit 
    if cv2.waitKey(1) == 27: 
        break
cv2.destroyAllWindows()




