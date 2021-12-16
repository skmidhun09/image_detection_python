import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

img = cv2.imread('img2.jpg')
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(imgGrey, (11,11), 0)
plt.imshow(blur, cmap='gray')
_, thrash = cv2.threshold(imgGrey, 65, 255, cv2.THRESH_BINARY)
# >>Get contour and Hierarchy in image
contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# cv2.imshow("img", img)
count = 0
i=0
beadCount = 0
parentList = []
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
    if (cv2.contourArea(contour) < 400):
        if (hierarchy[-1][i][3] != -1):
            # cv2.putText(img, str(hierarchy[-1][i][3]), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
            parentList.append(hierarchy[-1][i][3])
# >>Get parent contour list from contours
    if(cv2.contourArea(contour) > 400 and cv2.contourArea(contour) < 30000):
        # >>Get Green contours
        cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)
        # >>Print polygon shape
        if len(approx) > 10:
            # cv2.putText(img, "circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            count = count + 1
    x = approx.ravel()[0]
    # print(cv2.contourArea(contour))
    y = approx.ravel()[1] - 5
    i = i + 1
# >> Count the entries of list
counter = Counter(parentList)
chainList = []
filteredCountList = []
j = 0

# >> Filter the list based on contour area
for contour in contours:
    for data in counter.most_common():
        if j == data[0]:
            print(str(data[0])+", "+str(data[1])+", "+str(cv2.contourArea(contour)))
            print("")
            if cv2.contourArea(contour) > (data[1] * 250) and cv2.contourArea(contour) < (data[1] * 400):
                print("**"+str(data[0])+", "+str(data[1]) )
                filteredCountList.append(j)
    j = j + 1
print(Counter(filteredCountList))

# >> Draw filtered contours
for ct in counter.items():
    if(ct[1] < 100):
        chainList.append(ct[1])
    m = 0
    for c in contours:
        if(ct[0] == hierarchy[-1][m][3]):
            newContours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE,None,hierarchy[-1][m])
            aprox = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            cv2.drawContours(img, aprox, 0, (0, 0, 255), 10)
            print("#########################")
        m=m+1

chainCounter = Counter(chainList)
# >>print final list chain and count
for chain in chainCounter.items():
    print("chain length :"+str(chain[0]) + ", count :"+str(chain[1]))
# biggest_contour = max(contours, key=cv2.contourArea)
# cv2.drawContours(img, biggest_contour, -1, (0, 255, 0), 4)
# print("number circles : "+ str(count))

cv2.namedWindow("output", cv2.WINDOW_NORMAL)    # Create window with freedom of dimensions                 # Read image
imS = cv2.resize(img, (2000, 2000))                # Resize image
cv2.imshow("output", imS)
cv2.waitKey(0)
cv2.destroyAllWindows()