import cv2

img = cv2.imread("test_images\\20240221_192151.jpg")

cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL) 
cv2.resizeWindow("Resized_Window", 800, 600) 

cv2.imshow("Resized_Window", img)
cv2.waitKey(0)
cv2.destroyAllWindows()