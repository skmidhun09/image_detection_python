from typing import Counter
import cv2
import numpy as np
import Cordinate
import excelWrite
import glob

def processImage(imageName , totalImageCount):
    img_rgb = cv2.imread(imageName)
    template = cv2.imread('SAMPLE/test_new.png')
    height, width, channels = template.shape
    radius = int((height + width)/ 4)
    print("sample height:",height," width:",width," radius:",radius)
    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(res >= threshold)
    prev_pt1=0
    prev_pt2=0
    mod_pt1=10000
    mod_pt2=10000

    x = []
    y = []
    for pt in zip(*loc[::-1]):  # Switch columns and rows
        cv2.circle(img_rgb, (pt[0] +radius , pt[1] + radius ), radius, (0, 255, 0), 1)
        if prev_pt1 != 0 and prev_pt2 != 0 : 
            #if prev_pt1 != pt[0] and prev_pt2 != pt[1] :
                if (pt[0] - mod_pt1) > radius or (pt[0] - mod_pt1) < -radius or (pt[1] - mod_pt2) > radius or (pt[1] - mod_pt2) < -radius:
                    mod_pt1 = pt[0] - (pt[0] % 10)
                    mod_pt2 = pt[1] - (pt[1] % 10)
                    #print(pt[0],pt[1])
                    x.append(pt[0])
                    y.append(pt[1])
        prev_pt1 = pt[0]
        prev_pt2 = pt[1]
    # >>Remove Noise
    i=0
    while i < len(x):
        j=i+1
        while j < len(x):
            if x[i] < (x[j] + radius) and x[i] > (x[j] - radius):
                if y[i] < (y[j] + radius) and y[i] > (y[j] - radius):
                    x.remove(x[j])
                    y.remove(y[j])
                else:
                    j = j + 1   
            else:
                j = j + 1    
        i = i + 1
    #print(x)
    #print(y)
    # >>Print numbers in detected Image
    i=0
    count=0
    while i < len(x):
        count = count + 1
        cv2.putText(img_rgb, str(count), (x[i],y[i]), 5, 0.5, (0, 0, 128),1)
        i=i+1
    # >>Finding the chain length
    i=0
    chains = []
    while i < len(x):
        l = x[i]
        m = y[i]
        x.remove(l)
        y.remove(m)
        chain = [Cordinate.Axis(l,m)]   
        for ch in chain:
            j=0
            while j < len(x):
                if ch.x < (x[j] + 35) and ch.x > (x[j] - 35):
                    if ch.y < (y[j] + 35) and ch.y > (y[j] - 35):
                        chain.append(Cordinate.Axis(x[j],y[j]))
                        x.remove(x[j])
                        y.remove(y[j])
                    else:
                        j = j + 1   
                else:
                    j = j + 1
        chains.append(chain)
    ########
    chainCount = []
    for z in chains:
        #print(z)
        chainCount.append(len(z))
    # >>print count in chain
    chainCounter = Counter(chainCount)
    # >>print final list chain and count
    excelWrite.addtoExcel(chainCounter,imageName,totalImageCount)
    print ("######################################### OUTPUT #############################################")
    for chain in chainCounter.items():
        print("chain length :"+str(chain[0]) + ", chain count :"+str(chain[1]))
    cv2.imwrite('result.png', img_rgb)

    
def bulkImageProcess(imgPath):
    images = glob.glob(imgPath)
    for image in images:
        processImage(image,len(images))


# >> Single Image Process
    #processImage("test1.jpg" , 1)
# >> Buld folder process
bulkImageProcess("INPUT/*.jpg")