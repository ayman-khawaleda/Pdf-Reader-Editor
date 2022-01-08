import PySide6
from PySide6 import QtGui
from PySide6.QtWidgets import *


class ImageView(QLabel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setAcceptDrops(True)

    def set_upper_widegt(self, ref):
        self.ref = ref

    def mousePressEvent(self, ev: PySide6.QtGui.QMouseEvent):
        if self.ref.mark_point:
            self.last_x = ev.x()
            self.last_y = ev.y()
            self.ref.last_MIVI = int(self.objectName())
            if self.ref.pdf_handler.current_index != self.ref.last_MIVI:
                self.ref.set_image(self.ref.pdf_handler.current_index)
            self.ref.pdf_handler.current_index = self.ref.last_MIVI
            self.ref.pdf_handler.set_point((self.last_x, self.last_y))
            self.ref.set_image(self.ref.last_MIVI)
            self.ref.mark_point = False
