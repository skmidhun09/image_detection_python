import cv2
import numpy as np
import matplotlib.pyplot as plt

frame = cv2.imread("real.jpg")
cv2.imshow('frame', frame)
lower_black = np.array([0,0,0], dtype = "uint16")
upper_black = np.array([70,70,70], dtype = "uint16")
black_mask = cv2.inRange(frame, lower_black, upper_black)
cv2.imshow('mask0',black_mask)
black_mask[np.where((black_mask == [0] ).all(axis = 1))] = [255]
cv2.imshow('mask1',black_mask)
_, thrash = cv2.threshold(black_mask, 150, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
count = 0
biggest_contour = max(contours, key=cv2.contourArea)
cv2.drawContours(black_mask, biggest_contour, -1, (0, 255, 0), 4)

for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
    #cv2.drawContours(black_mask, [approx], 0, (0, 255, 0), 3)
cv2.imshow("Final", black_mask)
cv2.waitKey(0)