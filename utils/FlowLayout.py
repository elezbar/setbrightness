from tkinter import SEL_FIRST
from typing import Optional
from PyQt6.QtCore import QSize, QRect, QPoint, Qt
from PyQt6.QtWidgets import QLayout, QLayoutItem
from numpy import rec

class FlowLayout(QLayout):
    
    def __init__(self, margin: int=0, spacing: int=0, paren=None) -> None:
        super().__init__()
        if paren is not None:
            self.setMarging(margin)
        self.setSpacing(spacing)
        self.item_list = []

    def __del__(self) -> None:
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, a0: QLayoutItem) -> None:
        self.item_list.append(a0)

    def count(self) -> int:
        return len(self.item_list)

    def itemAt(self, index: int) -> QLayoutItem:
        if 0 <= index < len(self.item_list):
            return self.item_list[index]
    
    def takeAt(self, index: int) -> QLayoutItem:
        if 0 <= index < len(self.item_list):
            return self.item_list.pop(index)

    def expandingDirections(self) -> Qt.Orientation:
        return Qt.Orientation(Qt.Orientation(0))

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, a0: int) -> int:
        return self.processing(QRect(0, 0, a0, 0))

    def setGeometry(self, a0: QRect) -> None:
        super().setGeometry(a0)
        self.processing(a0)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        size = QSize()
        for item in self.item_list:
            size = size.expandedTo(item.minimumSize())
        size += QSize(2 * self.contentsMargins().top(),
                      2 * self.contentsMargins().top())
        return size

    def processing(self, rect: QRect) -> int:
        x = rect.x()
        y = rect.y()
        line_height = 0

        for item in self.item_list:
            space_x = self.spacing()
            space_y = self.spacing()
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x

            item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height + rect.y()