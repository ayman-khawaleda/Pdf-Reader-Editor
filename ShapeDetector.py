import cv2
import imutils
import numpy as np


class ShapeDetector:
    def detect_shapes(self, img, area_size=4000):
        """
        :param img In Gray Space:
        :return mask of Shapes(Images In our Case):
        """
        blurred = cv2.GaussianBlur(img, (3, 3), 0)
        thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=2)

        cnts = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        mask = np.zeros_like(img)
        for c in cnts:
            area = cv2.contourArea(c)
            if 300000 > area > area_size:
                newc = c.copy().reshape(-1)
                if newc[0] == 0 and newc[1] == 0:
                    continue
                cv2.drawContours(mask, [c], -1, (255, 255, 255), -1)
        return cv2.bitwise_not(mask)
