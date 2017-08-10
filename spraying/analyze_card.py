import cv2
import numpy as np
from matplotlib import path

class blob_detector():
    def main(self):
        blobs = blob_detector()
        img, params = blobs.initialize()
        single_keypoints, xlist, ylist = blobs.single_drops(img,params)
        total_area, singles_list, total_drops = blobs.find_contours(img, xlist, ylist)
        psi, ppi, totalpix = blobs.scale(img)
        something = blobs.analysis(total_area, singles_list, totalpix, psi, total_drops, ppi)

    def initialize(self):
        #img = cv2.imread("thresholded_paper_5.png")
        img = cv2.imread('png_spray_paper_large.png')
        params = cv2.SimpleBlobDetector_Params()
        return img, params

    # Needs serious optimization
    def scale(self, img):
        card_length = input("What is the length of the card in inches?")
        card_height = input("What is the width of the card in inches?")
        sqin = float(card_height) * float(card_length)
        img_copy = img
        height, width, channels = img_copy.shape
        # Black out the white background
        for i in range(height):
            for j in range(width):
                blue = img_copy[i, j, 0]
                green = img_copy[i, j, 1]
                red = img_copy[i, j, 2]
                if blue > 200:
                    if green > 230:
                        if red > 230:
                            img_copy[i, j] = [0, 0, 0]
                            continue
                if img_copy[i - 1, j, 0] == 0 or img_copy[i, j - 1, 0] == 0 or img_copy[i - 1, j - 1, 0] == 0:
                    if blue > 150:
                        if green > 150:
                            if red > 130:
                                img_copy[i, j] = [0, 0, 0]
        for i in range(height - 1, -1, -1):
            for j in range(width - 1, -1, -1):
                blue = img_copy[i, j, 0]
                green = img_copy[i, j, 1]
                red = img_copy[i, j, 2]
                if i == height - 1:
                    continue
                if img_copy[i + 1, j, 0] == 0 or img_copy[i, j + 1, 0] == 0 or img_copy[i + 1, j + 1, 0] == 0:
                    if blue > 150:
                        if green > 150:
                            if red > 130:
                                img_copy[i, j] = [0, 0, 0]
        totalcount = 0
        for i in range(height):
            for j in range(width):
                blue = img_copy[i, j, 0]
                green = img_copy[i, j, 1]
                red = img_copy[i, j, 2]
                if red == 0 and green == 0 and blue == 0:
                    continue
                else:
                    totalcount += 1

        psi = float(totalcount) / sqin
        ppi = psi ** (0.5)
        totalpix = totalcount
        return psi, ppi, totalpix

    # ----------------
    # Single Droplets
    # ----------------
    def single_drops(self, img, params):
        # Minimum Area
        params.filterByArea = True
        params.minArea = 10

        # Circularity
        params.filterByCircularity = True
        params.minCircularity = 0

        # Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.2

        # Convexity Parameters
        params.filterByConvexity = True
        params.minConvexity = 0.93
        params.maxConvexity = 1

        # Set up detector
        detector = cv2.SimpleBlobDetector(params)
        # Detect blobs
        single_keypoints = detector.detect(img)
        single_drops = len(single_keypoints)

        # Create list of xy coordinates of all single blob centers
        i = 0
        xlist = []
        ylist = []

        print int(len(single_keypoints))
        while i < int(len(single_keypoints)):
            x = int(single_keypoints[i].pt[0])
            y = int(single_keypoints[i].pt[1])
            print x
            print y
            xlist.append(x)
            ylist.append(y)
            i += 1

        return single_keypoints, xlist, ylist

    def find_contours(self, img, xlist, ylist):
        img = cv2.imread('png_spray_paper_large.png')
        imgrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgrey, 160, 255, 0)
        image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        total_drops = len(contours)
        im_with_contours = cv2.drawContours(img, contours, -1, (0, 0, 255), 1)
        hlength = len(contours)
        hierarchy.shape = (hlength, 4)
        hlist = hierarchy.tolist()
        i = 0
        singles_list = []
        total_area = 0
        # check length of heirarchy and contours

        while i < len(contours):
            # Determine if contour is in appropriate hierarchy
            # Needs foolproofing: what if some images have blobs at a different hierarchy level?
            print hlist[i][3]
            if hlist[i][3] != 0:
                i += 1
                continue
            cnt = contours[i]
            # Convert contour to path
            contours[i].shape = (int(contours[i].shape[0]), int(contours[i].shape[2]))
            p = path.Path(contours[i])
            j = 0
            while j < len(xlist):
                x = xlist[j]
                y = ylist[j]
                # If the current contour is a single blob, add it to the singles_list
                # for size distribution analysis, and to the total area for coverage %
                if p.contains_points([(x,y)]):
                    singles_count = len(singles_list)
                    singles_list.append(cv2.contourArea(cnt))
                    del xlist[j]
                    del ylist[j]
                    break
                j += 1
            total_area += cv2.contourArea(cnt)
            i += 1
            print "i = " + str(i)
        print 'length of singles list: ' + str(len(singles_list))
        return total_area, singles_list, total_drops

    def analysis(self, total_area, singles_list, totalpix, psi, total_drops, ppi):
        print total_area
        print totalpix
        coverage_per = float(total_area / totalpix)
        print "Coverage percentage: " + str(coverage_per)
        print 'length of singles list: ' + str(len(singles_list))
        print type(singles_list[3])
        sorted_list_pix = sorted(singles_list)
        print type(sorted_list_pix)
        # Convert to a list of blob areas sorted by size (in square micrometres)
        sorted_list = [x / psi * 6.4516 * (10 ** 8) for x in sorted_list_pix]
        # Convert list of blob areas to blob diameters
        diameters_list = [x ** 0.455 * 1.06 for x in sorted_list]

        # Numerical Mean, Median, and Standard Deviation
        num_median = np.median(diameters_list)
        num_average = np.mean(diameters_list)
        num_stdev = np.std(diameters_list)
        list_length = len(sorted_list)

        # Volume Median Diameter
        vol_total = 0
        h = 0
        while h < len(sorted_list):
            vol_total = vol_total + (sorted_list[h] ** 0.455 * 1.06) ** 3 * 3.14159 / 6
            h += 1

        vol_counter = 0
        i = 0
        # VMD: convert to volume from pix and count until reach median volumetrically
        while vol_counter < ( vol_total / 2 ):
            vol_counter = vol_counter + (sorted_list[i] ** 0.455 * 1.06) ** 3 * 3.14159 / 6
            i += 1
        if vol_counter != (vol_total / 2):
            i -= 1
            vol_median_dia = ( sorted_list[i] ** 0.455 * 1.06 + sorted_list[i+1] ** 0.455 * 1.06 ) / 2
        else:
            i -= 1
            vol_median_dia = sorted_list[i] ** 0.455 * 1.06

        # Volume Mean Diameter
        j = 0
        numerator = 0
        denominator = 0
        while j < len(sorted_list):
            numerator = numerator + (sorted_list[j] ** 0.455 * 1.06) ** 4
            denominator = denominator + (sorted_list[j] ** 0.455 * 1.06) ** 3
            j += 1
        vol_mean_dia = numerator / denominator

        # Blob density in droplets per square inch
        drop_density = total_drops / (totalpix / psi)

        print num_median
        print num_average
        print num_stdev
        print vol_median_dia
        print vol_mean_dia
        print drop_density

        num_median_in = num_median / ppi
        num_average_in = num_average / ppi
        num_stdev_in = num_stdev / ppi
        vol_median_dia_in = vol_median_dia / ppi
        vol_mean_dia_in = vol_mean_dia / ppi

        print num_median_in
        print num_average_in
        print num_stdev_in
        print vol_mean_dia_in
        print vol_median_dia_in










if __name__ == "__main__":
    blobs = blob_detector()
    blobs.main()