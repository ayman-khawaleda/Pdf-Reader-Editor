# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OpencvProjectUIfIzpsF.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import threading
import time
from PIL import Image
from PySide6 import QtGui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import PdfHandler
import ImageView
import EyeDetector


class Ui_MainWindow(object):
    def __init__(self):
        self.start_detect_eyes = True
        self.thread_eye_detector = None
        self.pdf_handler = PdfHandler.PDFHandler()
        self.has_file = False
        self.apply_ecm = False
        self.mark_point = False
        self.last_MIVI = 0
        self.image_views = []
        self.page_size = 740

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"PDF-Reader")
        MainWindow.setGeometry(300, 30, 860, 750)
        MainWindow.setFixedWidth(860)
        MainWindow.setFixedHeight(750)
        self.main_window = MainWindow
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setAcceptDrops(True)
        self.centralwidget.dropEvent = self.drop_event
        self.centralwidget.dragEnterEvent = self.drag_event

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 10, 700, 700))
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setAcceptDrops(True)
        self.ver_bar = QScrollBar()
        self.scrollArea.setVerticalScrollBar(self.ver_bar)

        self.vertical_images_widget = QWidget(self.scrollArea)
        self.vertical_images_widget.setObjectName(u"vertical_images_widget")
        self.vertical_images_widget.setAcceptDrops(True)
        self.vertical_images_widget.setFixedWidth(680)

        self.vertical_images_layout = QVBoxLayout()

        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(720, 20, 131, 201))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.eye_com_button = QPushButton(self.verticalLayoutWidget)
        self.eye_com_button.setObjectName(u"eye_com_button")
        self.eye_com_button.clicked.connect(self.eye_comfort_event)
        self.verticalLayout.addWidget(self.eye_com_button)

        self.change_page_color_button = QPushButton(self.verticalLayoutWidget)
        self.change_page_color_button.setObjectName(u"change_page_color_button")
        self.change_page_color_button.clicked.connect(self.change_page_color_event)

        self.verticalLayout.addWidget(self.change_page_color_button)

        self.change_font_color_button = QPushButton(self.verticalLayoutWidget)
        self.change_font_color_button.setObjectName(u"change_font_color_button")
        self.change_font_color_button.clicked.connect(self.change_font_color_event)

        self.verticalLayout.addWidget(self.change_font_color_button)

        self.mark_point_button = QPushButton(self.verticalLayoutWidget)
        self.mark_point_button.setObjectName(u"mark_point_button")
        self.mark_point_button.clicked.connect(self.mark_point_event)

        self.verticalLayout.addWidget(self.mark_point_button)

        self.eye_scroling_button = QPushButton(self.verticalLayoutWidget)
        self.eye_scroling_button.setObjectName(u"eye_scroling_button")
        self.eye_scroling_button.clicked.connect(self.scroll_with_eye_event)

        self.verticalLayout.addWidget(self.eye_scroling_button)

        self.eye_screenshoot_button = QPushButton(self.verticalLayoutWidget)
        self.eye_screenshoot_button.setObjectName(u"eye_screenshoot_button")
        self.eye_screenshoot_button.clicked.connect(self.take_screen_shoot_event)

        self.verticalLayout.addWidget(self.eye_screenshoot_button)

        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(780, 240, 41, 21))
        self.spinBox.valueChanged.connect(self.spin_box_event)

        self.reset_button = QPushButton(self.verticalLayoutWidget)
        self.reset_button.setObjectName(u"Reset")
        self.reset_button.setGeometry(QRect(740, 280, 40, 20))
        self.reset_button.clicked.connect(self.reset_event)
        self.verticalLayout.addWidget(self.reset_button)

        self.save_button = QPushButton(self.verticalLayoutWidget)
        self.save_button.setObjectName(u"Save")
        self.save_button.setGeometry(QRect(740, 320, 40, 20))
        self.save_button.clicked.connect(self.save_event)
        self.verticalLayout.addWidget(self.save_button)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(720, 240, 51, 21))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 861, 21))
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.ver_bar.sliderChange = self.slider_change_event

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PDF-REDER", None))
        self.eye_com_button.setText(QCoreApplication.translate("MainWindow", u"Eye Comfort", None))
        self.change_page_color_button.setText(QCoreApplication.translate("MainWindow", u"Change Page Color", None))
        self.change_font_color_button.setText(QCoreApplication.translate("MainWindow", u"Change Font Color", None))
        self.mark_point_button.setText(QCoreApplication.translate("MainWindow", u"Mark Point", None))
        self.eye_scroling_button.setText(QCoreApplication.translate("MainWindow", u"Eye Scroling", None))
        self.eye_screenshoot_button.setText(QCoreApplication.translate("MainWindow", u"Eye ScreenShoot", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Page Num:", None))
        self.reset_button.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.save_button.setText(QCoreApplication.translate("MainWindow", u"Save", None))

    def add_image_view(self, index):
        image_view = ImageView.ImageView(self.vertical_images_widget)
        image_view.setObjectName(f"{index}")
        image_view.setFixedSize(680, 720)
        image_view.setScaledContents(True)
        image_view.setWordWrap(False)
        image_view.setPixmap(self.convertCvImage2QtImage(self.pdf_handler.pdf_images[index]))
        image_view.set_upper_widegt(self)
        self.image_views.append(image_view)
        self.vertical_images_layout.addWidget(image_view)

    def reset_images_ui(self):
        self.image_views = []
        self.vertical_images_widget = QWidget(self.scrollArea)
        self.vertical_images_widget.setObjectName(u"vertical_images_widget")
        self.vertical_images_widget.setAcceptDrops(True)
        self.vertical_images_widget.setFixedWidth(680)
        self.vertical_images_layout = QVBoxLayout()

    def drop_event(self, e):
        try:
            self.path = e.mimeData().text()
            self.pdf_handler = PdfHandler.PDFHandler()
            isloaded = self.pdf_handler.Pdf2Image(self.path[8:])
            self.reset_images_ui()
            self.vertical_images_widget.setFixedHeight(len(self.pdf_handler.pdf_images) * self.page_size)
            for i, img in enumerate(self.pdf_handler.pdf_images):
                self.add_image_view(i)
            self.vertical_images_widget.setLayout(self.vertical_images_layout)
            self.scrollArea.setWidget(self.vertical_images_widget)
            self.spinBox.setMaximum(len(self.pdf_handler.pdf_images) - 1)
            self.has_file = True if isloaded else False
            self.apply_ecm = False
        except Exception as e:
            print(e)

    def drag_event(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def spin_box_event(self, val):
        pass

    def slider_change_event(self, val):
        self.spinBox.setValue((self.ver_bar.sliderPosition() + 300) // self.page_size)
        self.ver_bar.update()

    def change_page_color_event(self):
        if self.has_file:
            color = QColorDialog.getColor()
            self.pdf_handler.apply_change_page_color(color.getRgb())
            self.update_images()

    def change_font_color_event(self):
        if self.has_file:
            color = QColorDialog.getColor()
            self.pdf_handler.apply_change_font_color(color.getRgb())
            self.update_images()

    def eye_comfort_event(self):
        if self.has_file:
            if not self.apply_ecm:
                self.pdf_handler.apply_eye_comfort_mode(70)
                self.update_images()
                self.apply_ecm = True
            else:
                self.pdf_handler.undo_eye_comfort_mode(70)
                self.apply_ecm = False
                self.update_images()

    def convertCvImage2QtImage(self, cv_img):
        PIL_image = Image.fromarray(cv_img).toqimage()
        return QPixmap().fromImage(PIL_image)

    def update_images(self):
        for i, _ in enumerate(self.pdf_handler.pdf_images):
            self.set_image(i)

    def set_image(self, ind):
        img = self.pdf_handler.pdf_images[ind]
        self.image_views[ind].setPixmap(self.convertCvImage2QtImage(img))

    def mark_point_event(self, event):
        if self.has_file:
            try:
                if not self.mark_point:
                    self.pdf_handler.set_back_point()
                self.mark_point = not self.mark_point
            except Exception as e:
                return

    def reset_event(self, event):
        if self.has_file:
            self.pdf_handler.reset()
            self.update_images()

    def save_event(self, event):
        if self.has_file:
            self.pdf_handler.save_pdf(time.time().__str__())
            self.update_images()

    def take_screen_shoot_event(self, event):
        if self.has_file:
            if self.start_detect_eyes:
                self.find_eyes()
            else:
                self.start_detect_eyes = not self.start_detect_eyes

    def take_screen_shoot(self):
        qrect = self.main_window.geometry()
        self.pdf_handler.take_screen_shoot(qrect.x(), qrect.y())

    def find_eyes(self):
        if self.has_file:
            eye_detector = EyeDetector.EyeDetector(self)
            self.thread_eye_detector = threading.Thread(target=eye_detector.start_screen_shoot_with_eye, args=())
            self.thread_eye_detector.start()

    def scroll_with_eye_event(self, event):
        if self.has_file:
            if self.start_detect_eyes:
                try:
                    eye_detector = EyeDetector.EyeDetector(self)
                    self.thread_eye_detector = threading.Thread(target=eye_detector.start_screen_scrolling, args=())
                    self.thread_eye_detector.start()
                except KeyboardInterrupt:
                    pass
            else:
                self.start_detect_eyes = not self.start_detect_eyes
