from PyQt6.QtWidgets import QMainWindow, QMessageBox, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QAction, QPixmap, QGuiApplication
from PyQt6.QtCore import QSize, Qt, QTimer
import keyboard
from queue import LifoQueue


from utils import WindowKeyBoardWorker, Monitor, FlowLayout
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
        self.setMinimumSize(QSize(150, 400))
        layout = FlowLayout()
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
        self.setCentralWidget(self.window)
        self.stack_keys = LifoQueue()
        worker = WindowKeyBoardWorker(self)
        worker.start()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        keyboard.add_hotkey('alt+2', lambda: self.stack_keys.put(1), suppress= True)
        keyboard.add_hotkey('alt+8', lambda: self.stack_keys.put(0), suppress = True)


    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def brightness_up(self):
        for slider in self.child_windows['BrightnessWindow']:
            slider.monitor.up_brightness()
        for slider in self.child_windows['BrightnessWindow']:
            slider.update()

    def brightness_down(self):
        for slider in self.child_windows['BrightnessWindow']:
            slider.monitor.down_brightness()
        for slider in self.child_windows['BrightnessWindow']:
            slider.update()
