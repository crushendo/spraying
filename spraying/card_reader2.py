import cv2
import numpy as np
import matplotlib.pyplot as plt

card_length = input("What is the length of the card in inches?")
card_height = input("What is the width of the card in inches?")
img = cv2.imread("spray_paper_large.tiff")
height, width, channels = img.shape
print height, width, channels

card_upper = np.array([255,240,100])
card_lower = np.array([240, 200, 3])
white_upper = np.array([255,255,255])
white_lower = np.array([240,240,240])

# Black out the white background
for i in range(height):
    for j in range(width):
        blue = img[i,j,0]
        green = img[i,j,1]
        red = img[i,j,2]
        if blue > 200:
            if green > 230:
                if red > 230:
                    img[i,j] = [0,0,0]
                    continue
        if img[i-1,j,0] == 0 or img[i,j-1,0] == 0 or img[i-1,j-1,0] == 0:
            if blue > 150:
                if green > 150:
                    if red > 130:
                        img[i, j] = [0, 0, 0]
for i in range(height-1, -1, -1):
    for j in range(width-1, -1, -1):
        blue = img[i, j, 0]
        green = img[i, j, 1]
        red = img[i, j, 2]
        if i == height - 1:
            continue
        if img[i + 1, j, 0] == 0 or img[i, j + 1, 0] == 0 or img[i + 1, j + 1, 0] == 0:
            if blue > 150:
                if green > 150:
                    if red > 130:
                        img[i, j] = [0, 0, 0]

# Determine scale of image (pixels per inch) and percent coverage
bluecount = 0
yellowcount = 0
totalcount = 0
interstitial = 0
sqin = float(card_height) * float(card_length)
for i in range(height):
    for j in range(width):
        blue = img[i, j, 0]
        green = img[i, j, 1]
        red = img[i, j, 2]
        if red == 0 and green == 0 and blue == 0:
            continue
        # Card Threshold
        elif red > 210:
            yellowcount += 1
            img[i, j] = [0, 255, 255]
        elif green > 200:
            yellowcount += 1
            img[i, j] = [0, 255, 255]
            interstitial += 1
        elif red > 150 and green > 140 and blue > 100:
            yellowcount += 1
            img[i, j] = [0, 255, 255]
            interstitial += 1
        elif blue > 170:
            bluecount += 1
            img[i, j] = [255, 0, 0]
        else:
            # Large blob threshold
            if red > 110 and green > 115:
                # Interstitial Threshold
                if blue > 100 and red > 200 and green > 200:
                    # Medium blob threshold
                    if red > 150 and blue > 150 and green > 150:
                        yellowcount += 1
                        img[i, j] = [0, 255, 255]
                        interstitial += 1
                    else:
                        bluecount += 1
                        img[i, j] = [255, 0, 0]
                # Small blob threshold
                else:
                    bluecount += 1
                    img[i, j] = [255, 0, 0]
            # Large blob threshold
            else:
                bluecount += 1
                img[i, j] = [255, 0, 0]
        totalcount += 1





psi = float(totalcount) / sqin
ppi = psi**(0.5)
print psi
print ppi

coverage = float(bluecount) / float(totalcount)
print("Total pixels counted: " + str(totalcount))
print("Blue pixels counted: " + str(bluecount))
print("Yellow pixels counted: " + str(yellowcount))
print("Interstitial pixels counted: " + str(interstitial))
print("Percent coverage: " + str(coverage))



# Detect blobs
#detector = cv2.SimpleBlobDetector()
#keypoints = detector.detect(img)


cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()




