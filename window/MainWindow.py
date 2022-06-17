from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap, QGuiApplication
from PyQt6.QtCore import QSize, Qt, QTimer
import keyboard
from queue import LifoQueue

from utils import VisibleThread, Monitor
from . import BrightnessWindow

class MonitorWidget(QWidget):
    def __init__(self, monitor: Monitor) -> None:
        super().__init__()
        self.setFixedSize(QSize(150, 150))
        layout = QVBoxLayout()
        self.monitor = monitor
        label_pixmap = QLabel()
        pixmap = QPixmap('monitor.png')
        pixmap = pixmap.scaled(QSize(120, 120))
        label_pixmap.setPixmap(pixmap)
        label_pixmap.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_pixmap)

        self.label_name = QLabel(monitor.name)
        self.label_name.setStyleSheet("""
            color:white;
        """)
        self.label_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_name)
        self.setLayout(layout)

class MainWindow(QMainWindow):

    def __init__(self, screens) -> None:
        super().__init__()
        self.visible = 0
        self.child_windows = {}
        self.screens = screens
        self.setMinimumSize(QSize(600, 400))
        layout = QHBoxLayout()
        self._list_monitors = Monitor.get_list_monitors()
        for mon in self._list_monitors:
            layout.addWidget(MonitorWidget(mon))
        self.setLayout(layout)
        self.window = QWidget()
        self.window.setStyleSheet("""
            background-color:black;
        """)
        self.window.setLayout(layout)
        self.alt_on_pressed = False
        self.child_windows['BrightnessWindow'] = [BrightnessWindow(elem,i) for i, elem in enumerate(self._list_monitors)]
        #
        self.setCentralWidget(self.window)
        self._stack_keys = LifoQueue()
        self._timer_stack = QTimer()
        self._timer_stack.timeout.connect(self._stack_to_func)
        self._timer_stack.start(10)
        keyboard.add_hotkey('alt+8', lambda: self._stack_keys.put(0), suppress = True)
        keyboard.add_hotkey('alt+2', lambda: self._stack_keys.put(1), suppress= True)


    def _stack_to_func(self):
        if not self._stack_keys.empty():
            if self._stack_keys.get() == 0:
                self._brightness_up()
            else:
                self._brightness_down()


    def _brightness_up(self):
        for slider in self.child_windows['BrightnessWindow']:
            slider.monitor.up_brightness()
        for slider in self.child_windows['BrightnessWindow']:
            slider.update()

    def _brightness_down(self):
        for slider in self.child_windows['BrightnessWindow']:
            slider.monitor.down_brightness()
        for slider in self.child_windows['BrightnessWindow']:
            slider.update()
