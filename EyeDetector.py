import time

import cv2
import numpy as np


class EyeDetector:

    def __init__(self, main_window):
        self.eye_img1 = np.zeros((80, 50), np.uint8)
        self.face_cascade = cv2.CascadeClassifier()
        self.eye_cascade = cv2.CascadeClassifier()
        self.face_cascade.load(r'cascade\\haarcascade_frontalface_alt.xml')
        self.eye_cascade.load(r'cascade\\haarcascade_eye.xml')
        self.old_eye_gray = np.zeros((100, 80), np.uint8)
        self.old_iris_center = None
        self.frames_without_wink = 0
        self.main_window = main_window
        self.old_eye = None

    def screen_shoot_eye_detector(self, img):
        frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)
        # cv2.imshow('Gray', frame_gray)
        try:
            eye_img = self.get_eye_area(frame_gray, img)
            if eye_img is not None:
                ret, self.eye_img1 = cv2.threshold(cv2.cvtColor(eye_img, cv2.COLOR_BGR2GRAY), 70, 255,
                                                   cv2.THRESH_BINARY)
                cv2.imshow('Threshh', self.eye_img1)
            # faces = self.face_cascade.detectMultiScale(frame_gray)
            # for (x, y, w, h) in faces[:1]:
            #     faceROI = frame_gray[y + 80:y + h // 2, x:x + w // 2]
            #     cv2.imshow('Face', faceROI)
            #     eyes = self.eye_cascade.detectMultiScale(faceROI, 1.3, 2)
            #     for (x2, y2, w2, h2) in eyes[:1]:
            #         try:
            #             eye_img = img[y + y2 + 50:y + 80 + y2 + 50, x + x2:x + x2 + 50, :].copy()
            #             ret, self.eye_img1 = cv2.threshold(cv2.cvtColor(eye_img, cv2.COLOR_BGR2GRAY), 70, 255,
            #                                                cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            #             cv2.imshow('Eye', eye_img)
            #             cv2.imshow('Thresh123', self.eye_img1)
            #         except Exception as e:
            #             pass
            try:
                img_diff = cv2.absdiff(self.eye_img1, self.old_eye_gray)
                cv2.imshow('Deiff', img_diff)
                if len(img_diff[img_diff == 0]) == 8000:
                    self.frames_without_wink += 1
                else:
                    self.frames_without_wink = 0
                if self.frames_without_wink == 5:
                    self.frames_without_wink = 0
                    print('Wink')
                    self.main_window.take_screen_shoot()
                    self.main_window.start_detect_eyes = False
                self.old_eye_gray = self.eye_img1
            except Exception as e:
                pass
            # cv2.imshow('Capture - Face detection', img)
        except Exception as e:
            pass

    def get_eye_area(self, frame_gray, img):
        faces = self.face_cascade.detectMultiScale(frame_gray)
        for (x, y, w, h) in faces[:1]:
            faceROI = frame_gray[y + 80:y + h // 2, x:x + w // 2]
            cv2.imshow('Face', faceROI)
            eyes = self.eye_cascade.detectMultiScale(faceROI, 1.3, 2)
            for (x2, y2, w2, h2) in eyes[:1]:
                try:
                    eye_img = img[y + y2 + 50:y + y2 + 150, x + x2: x + x2 + 80, :]
                    self.old_eye = eye_img
                    return eye_img
                except Exception as e:
                    print(e)
            return None

    def start_screen_shoot_with_eye(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        try:
            while self.main_window.start_detect_eyes:
                opened, frame = cap.read()
                if frame is None:
                    break
                self.screen_shoot_eye_detector(frame)
                if cv2.waitKey(1) == 27:
                    break
            self.main_window.start_detect_eyes = True
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            cap.release()
            cv2.destroyAllWindows()

    def start_screen_scrolling(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        try:
            while self.main_window.start_detect_eyes:
                opened, frame = cap.read()
                if frame is None:
                    break
                self.screen_scrolling(frame)
                if cv2.waitKey(1) == 27:
                    break
            self.main_window.start_detect_eyes = True
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            cap.release()
            cv2.destroyAllWindows()

    def screen_scrolling(self, img):
        frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)
        # cv2.imshow('Gray', frame_gray)
        try:
            eye_img = self.get_eye_area(frame_gray, img)
            if eye_img is None:
                eye_img = self.old_eye
            cv2.imshow('Eye', eye_img)
            eye_img_blur = cv2.medianBlur(eye_img, 7)
            gray_eye = cv2.cvtColor(eye_img_blur, cv2.COLOR_BGR2GRAY)
            rows = gray_eye.shape[0]
            circles = cv2.HoughCircles(gray_eye, cv2.HOUGH_GRADIENT, 1, rows / 8,
                                       param1=60, param2=16,
                                       minRadius=8, maxRadius=12)

            if circles is not None:
                circles = np.int8(circles)
                for i in circles[0]:
                    center = (i[0], i[1])
                    if self.old_iris_center is not None:
                        cen = self.old_iris_center
                        x_diff = cen[0] - center[0]
                        y_diff = cen[1] - center[1]
                        if -1 > x_diff < 1:
                            val = self.main_window.ver_bar.value() - 500
                            self.main_window.ver_bar.setValue(val)
                            self.main_window.ver_bar.update()
                            print('Center Diff on X: ', x_diff)
                        if -1 > y_diff < 1:
                            val = self.main_window.ver_bar.value() + 500
                            self.main_window.ver_bar.setValue(val)
                            self.main_window.ver_bar.update()
                            print('Center Diff on Y: ', y_diff)
                    self.old_iris_center = center
                    radius = i[2]
                    cv2.circle(eye_img, center, radius + 1, (255, 0, 255), -1)

                ret, eye_img1 = cv2.threshold(gray_eye, 70, 255,
                                              cv2.THRESH_BINARY)
                eye_img1 = cv2.morphologyEx(eye_img1, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
                cv2.imshow('Eye', eye_img)
                cv2.imshow('Threshh', eye_img1)
                cv2.imshow('DIFF', cv2.absdiff(self.old_eye_gray, eye_img1))
                # self.old_eye_gray = eye_img1
        except KeyboardInterrupt:
            pass

        except Exception as e:
            pass

    def screen_scrolling1(self):
        feature_params = dict(maxCorners=5,
                              qualityLevel=0.3,
                              minDistance=7,
                              blockSize=7)

        lk_params = dict(winSize=(15, 15),
                         maxLevel=2,
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                                   10, 0.03))

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        old_frame = cap.read()[1]
        old_frame_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        old_eye = self.get_eye_area(old_frame_gray, old_frame)
        while old_eye is None:
            old_frame = cap.read()[1]
            old_frame_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
            old_eye = self.get_eye_area(old_frame_gray, old_frame)
            print('Still None')

        cv2.imshow('Eye', old_eye)
        cv2.waitKey(30)
        old_eye_gray = cv2.cvtColor(old_eye, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(old_eye_gray, mask=None,
                                     **feature_params)
        mask = np.zeros_like(old_eye)
        try:
            while True:
                eye = None
                while eye is None:
                    ret, frame = cap.read()
                    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    eye = self.get_eye_area(frame_gray, frame)
                    eye_gray = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
                p1, st, err = cv2.calcOpticalFlowPyrLK(old_eye_gray,
                                                       eye_gray,
                                                       p0, None,
                                                       **lk_params)
                # Select good points
                good_new = p1[st == 1]
                good_old = p0[st == 1]
                for i, (new, old) in enumerate(zip(good_new,
                                                   good_old)):
                    a, b = np.int8(new.ravel()).copy()
                    c, d = np.int8(old.ravel()).copy()
                    mask = cv2.line(mask, (a, b), (c, d),
                                    (255, 0, 0), 2)

                    eye = cv2.circle(eye, (a, b), 5,
                                     (0, 255, 0), -1)

                    img = cv2.add(eye, mask)
                    cv2.imshow('frame', eye)
                    cv2.imshow('Big-Frame', img)

                    k = cv2.waitKey(25)
                    if k == 27:
                        break

                    # Updating Previous frame and points
                    old_eye_gray = eye_gray.copy()
                    p0 = good_new.reshape(-1, 1, 2)
                    print('Here Good: ', good_new)

            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(e)
            # cap.release()
            # cv2.destroyAllWindows()
