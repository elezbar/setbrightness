from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize, Qt

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

    def __init__(self) -> None:
        super().__init__()
        self.visible = 0
        self.child_windows = {}
        
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


        # self.button = QPushButton("Push for Window")
        # self.button.clicked.connect(self.show_new_window)
       
        self.setCentralWidget(self.window)

    def show_new_window(self, checked) -> None:
        self.threads = []
        if 'BrightnessWindow' not in self.child_windows:
            self.child_windows['BrightnessWindow'] = BrightnessWindow(self._list_monitors)
            # visible_thread = VisibleThread('BrightnessWindow', self.child_windows)
            # self.threads.append(visible_thread)
            # visible_thread.start()
            self.child_windows['BrightnessWindow'].show()
        else:
            self.child_windows['BrightnessWindow'].start_hide()

    def keyPressEvent(self, e):
        
        print(e.key)