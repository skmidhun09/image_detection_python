# import cv2
# import numpy as np
#
# frame = cv2.imread("real.jpg")
# cv2.imshow('frame', frame)
# lower_black = np.array([0,0,0], dtype = "uint16")
# upper_black = np.array([70,70,70], dtype = "uint16")
# black_mask = cv2.inRange(frame, lower_black, upper_black)
# cv2.imshow('mask0',black_mask)
# black_mask[np.where((black_mask == [0] ).all(axis = 1))] = [255]
# cv2.imshow('mask1',black_mask)
# cv2.waitKey(0)
