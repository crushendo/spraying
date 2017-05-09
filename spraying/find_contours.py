import cv2
import numpy as np
from matplotlib import path

class find_contours():
    def main(self):
        img = cv2.imread('png_spray_paper_large.png')
        imgrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgrey,160,255,0)
        image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        im_with_contours = cv2.drawContours(img, contours, -1, (0,0,255), 1)
        #cv2.imshow("im_with_contours", im_with_contours)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        print hierarchy.shape
        print contours[2]
        print type(contours[2])
        clist = contours[2].tolist()
        print clist
        print contours[2].shape[1]
        contours[2].shape = (int(contours[2].shape[0]), int(contours[2].shape[2]))
        p = path.Path(contours[2])
        print clist[1]
        print 'size' + str(cv2.contourArea(contours[2]))

        if p.contains_points([(1162,1845)]):
            print 'yes its in'
        print type(hierarchy[0])
        print len(hierarchy)
        print hierarchy.shape[1]
        hierarchy.shape = (4924, 4)
        print hierarchy[2]
        hlist = hierarchy.tolist()
        print len(hlist[2])
        hlist2 = hlist[2]
        print hlist2[2]
        print hlist[2][2]



if __name__ == "__main__":
    finder = find_contours()
    finder.main()
