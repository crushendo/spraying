import cv2
import numpy as np

class blob_detector():
    def main(self):
        blobs = blob_detector()
        img, params = blobs.initialize()
        all_keypoints = blobs.all_drops(img, params)
        single_keypoints, diameter_list = blobs.single_drops(img,params)
        double_keypoints = blobs.double_drops(img,params)
        triple_keypoints = blobs.triple_drops(img,params)
        blobs.output(img, all_keypoints, single_keypoints, double_keypoints, triple_keypoints)

    def initialize(self):
        #img = cv2.imread("thresholded_paper_5.png")
        img = cv2.imread("spray_paper_large.tiff")
        params = cv2.SimpleBlobDetector_Params()
        return img, params

# ----------------
# Single Droplets
# ----------------
    def single_drops(self,img,params):
        # Minimum Area
        params.filterByArea = True
        params.minArea = 10

        # Circularity
        params.filterByCircularity = True
        params.minCircularity = 0

        #Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.2

        # Convexity Parameters
        params.filterByConvexity = True
        params.minConvexity = 0.93
        params.maxConvexity = 1

        #Set up detector
        detector = cv2.SimpleBlobDetector(params)
        # Detect blobs
        single_keypoints = detector.detect(img)
        single_drops = len(single_keypoints)

        i=0
        diameter_list = []

        #for keypoint in single_keypoints:
        #    keypoint = single_keypoints.size
        #    keypoint = keypoint / ppi
        #    keypoint = keypoint * keypoint * 3.14159 * 0.25
        #    drop_d = keypoint ** 0.455 * 1.06
        #    diameter_list[i] = drop_d
        #    i += 1

        print "Single drops: " + str(single_drops)
        return single_keypoints, diameter_list

# ----------------
# Double Droplets
# ----------------
    def double_drops(self,img,params):
        # Minimum Area
        params.filterByArea = True
        params.minArea = 10

        # Circularity
        params.filterByCircularity = True
        params.minCircularity = 0

        #Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.2

        # Convexity Parameters
        params.filterByConvexity = True
        params.minConvexity = 0.90
        params.maxConvexity = 0.92

        # Set up detector
        detector = cv2.SimpleBlobDetector(params)
        # Detect blobs
        double_keypoints = detector.detect(img)
        double_drops = len(double_keypoints)
        print "Double drops: " + str(double_drops)
        return double_keypoints

# ----------------
# Triple Droplets
# ----------------
    def triple_drops(self,img,params):
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
        params.minConvexity = 0.85
        params.maxConvexity = 0.89

        # Set up detector
        detector = cv2.SimpleBlobDetector(params)
        # Detect blobs
        triple_keypoints = detector.detect(img)
        triple_drops = len(triple_keypoints)
        print "Triple drops: " + str(triple_drops)
        return triple_keypoints

# -------------
# All Droplets
# -------------
    def all_drops(self,img,params):
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
        params.minConvexity = 0.85
        params.maxConvexity = 1

        # Set up detector
        detector = cv2.SimpleBlobDetector(params)
        # Detect blobs
        all_keypoints = detector.detect(img)
        size = all_keypoints[0].size
        print "Size: " + str(size)
        all_drops = len(all_keypoints)
        print "All drops: " + str(all_drops)
        return all_keypoints

    def stats(self, diameter_list):
        sorted_list = diameter_list.sort(key=float)
        list_length = len(sorted_list)
        index = (list_length - 1) // 2
        if list_length % 2:
            num_median = sorted_list[index]
        else:
            num_median = (sorted_list[index] + sorted_list[index + 1]) / 2
        for diameter in sorted_list:
            total_area = diameter * 3.14159 * 0.25
        current_area = 0
        i = 0
        while current_area <= total_area:
            current_area += sorted_list[i] * 3.14159 * 0.25
        vol_median = (sorted_list[i] + sorted_list[i - 1]) / 2
        


    def output(self, img, all_keypoints, single_keypoints, double_keypoints, triple_keypoints):
        # Draw detected blobs with circles around them
        im_with_keypoints = cv2.drawKeypoints(img, all_keypoints, np.array([]), (255,255,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #im_with_keypoints = cv2.drawKeypoints(im_with_keypoints, single_keypoints, np.array([]), (0, 0, 255))
        #im_with_keypoints = cv2.drawKeypoints(im_with_keypoints, double_keypoints, np.array([]), (0, 255, 0))
        #im_with_keypoints = cv2.drawKeypoints(im_with_keypoints, triple_keypoints, np.array([]), (255, 0, 0))
        cv2.imshow("im_with_keypoints", im_with_keypoints)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    blobs = blob_detector()
    blobs.main()
