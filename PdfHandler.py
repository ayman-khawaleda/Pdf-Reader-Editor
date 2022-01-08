import random
import time
import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
from ShapeDetector import ShapeDetector
import pyautogui


class PDFHandler:
    def __init__(self):
        self.current_index = 0
        self.original_images = []
        self.mark_point_color = (255, 0, 0)
        self.last_point_center = (0, 0)
        self.old_page = []
        self.shape_detector = ShapeDetector()

    def Pdf2Image(self, path: str = None):
        if path is None:
            raise Exception('Path is None')
        elif path[-3:] != 'pdf':
            raise Exception('Not PDF File')
        try:
            """
                Return Images As PIL OBJECTS
            """
            __poppler_path = r'poppler-21.11.0\Library\bin'
            images = convert_from_path(path, poppler_path=__poppler_path)
            self.pdf_images = self.pdf_to_np(images)
            self.original_images = np.copy(self.pdf_images)
            return True
        except Exception as e:
            print(e)
            return False

    def pdf_to_np(self, images: list):
        return np.array([np.asarray(x) for x in images])

    def apply_eye_comfort_mode(self, val):
        for ind in range(len(self.pdf_images)):
            self.pdf_images[ind][:, :, 2] -= val

    def undo_eye_comfort_mode(self, val):
        for ind in range(len(self.pdf_images)):
            self.pdf_images[ind][:, :, 2] += val

    def apply_change_page_color(self, color):
        self.mark_point_color = color
        for image, ori_image in zip(self.pdf_images, self.original_images):
            grayimage = cv2.cvtColor(ori_image, cv2.COLOR_BGR2GRAY)
            mask2 = self.shape_detector.detect_shapes(grayimage, 3000)
            mask = self.binary_image(grayimage)
            mask = cv2.bitwise_and(mask, mask, mask=mask2)
            image[:, :, 0][mask[:, :] == 255] = color[0]
            image[:, :, 1][mask[:, :] == 255] = color[1]
            image[:, :, 2][mask[:, :] == 255] = color[2]
        self.old_page = self.pdf_images[self.current_index]

    def apply_change_font_color(self, color):
        for image, ori_image in zip(self.pdf_images, self.original_images):
            grayimage = cv2.cvtColor(ori_image, cv2.COLOR_BGR2GRAY)
            mask2 = self.shape_detector.detect_shapes(grayimage)
            mask = cv2.bitwise_not(self.binary_image(grayimage))
            mask = cv2.bitwise_or(mask, mask, mask=mask2)
            mask = cv2.bitwise_not(mask)
            image[:, :, 0][mask[:, :] == 0] = color[0]
            image[:, :, 1][mask[:, :] == 0] = color[1]
            image[:, :, 2][mask[:, :] == 0] = color[2]
        self.old_page = self.pdf_images[self.current_index]

    def binary_image(self, img):
        ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        zero_val = len(th2[th2[:, :] == 0])
        ones_val = len(th2[th2[:, :] == 255])
        if zero_val > ones_val:
            return cv2.bitwise_not(th2)
        return th2

    def set_point(self, pos):
        w, h = 720, 680
        iw, ih, _ = self.pdf_images[self.current_index].shape
        pos = (int((ih / h) * pos[0]), int((iw / w) * pos[1]))
        self.old_page = self.pdf_images[self.current_index].copy()
        self.old_ind = self.current_index
        cv2.circle(self.pdf_images[self.current_index], pos, 12,
                   (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5)

    def set_back_point(self):
        try:
            if len(self.old_page) != 0:
                self.pdf_images[self.old_ind] = self.old_page
        except Exception as e:
            pass

    def reset(self):
        self.pdf_images = self.original_images.copy()

    def save_pdf(self, name: str):
        try:
            first = Image.fromarray(self.pdf_images[0])
            img_lis = [Image.fromarray(x) for x in self.pdf_images[1:]]
            pdf_name = name + '.pdf'
            first.save(pdf_name, 'PDF', resolution=100.0, save_all=True, append_images=img_lis)
        except Exception as e:
            pass

    def take_screen_shoot(self, x, y):
        screenshot = pyautogui.screenshot()
        img = self.pdf_to_np([screenshot])[0]
        img2 = img[y + 10:750, x + 15:(x - 300) + 960, :]
        cv2.imwrite(str(time.time()) + '.png', img2)
