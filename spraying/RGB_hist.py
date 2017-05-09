import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("small_blob_composite.tiff")
imgrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
color = ('g')
#color = ('b', 'g', 'r')
for channel,col in enumerate(color):
    histr = cv2.calcHist([imgrey],[channel],None,[255],[1,255])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.title('RGB Histogram')
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()