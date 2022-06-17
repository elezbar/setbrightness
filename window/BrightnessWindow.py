from time import sleep
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QSlider
from PyQt6.QtCore import QSize, Qt, QTimer
from random import randint
from utils import Monitor


class BrightnessWindow(QWidget):
    
    def __init__(self, monitor: Monitor, n):
        super().__init__()
        self.monitor = monitor
        self.visible = 1
        self.updated = True
        self.ready_update = True
        self.setStyleSheet("background-color: #1A1A1A; color: white; ")
        self.setFixedSize(QSize(45, 140))
        self.setGeometry(50+n*45, 60, 0, 0)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.Tool)
        self._timer_hide = None
        self._timer_animation = QTimer()
        self._change_visible = False
        self._timer_animation.timeout.connect(self._hide_animation)
        layout = QVBoxLayout()
        self.slider = QSlider()
        self.slider.setGeometry(40, 0, 0, 0)
        self.slider.setStyleSheet("""
        QSlider::groove:vertical {
            background: white;
            position: absolute;
            left: 6px; right: 5px;
            top: 9px; bottom: 3px;
        }

        QSlider::handle:vertical {
            height: 11px;
            background: white;
            margin: 0 0px; /* expand outside the groove */
        }

        QSlider::add-page:vertical {
            background: black;
        }

        QSlider::sub-page:vertical {
            background: #6A6A6A;
        }
        """)
        self.slider.setRange(0, 100)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self._slider_change)
        layout.addWidget(self.slider)
        self.label = QLabel('0')
        self.label.setStyleSheet("""font-family: "Segoe UI";
                                    font-size: 13px;
                                    margin-bottom:5px;
                                    font-weight:600""")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)
        self._timer_animation.start(10)
        self.update()
        

    def update(self):
        bri = int(self.monitor.brightness)
        self.show()
        self.label.setText(str(bri))
        self.slider.setValue(bri)
        self._start_hide = True

    def _slider_change(self, value):
        self.monitor.set_brightness(value)
        self.label.setText(str(value))
        self._start_hide = True
        
    def _hide_animation(self):
        if self._start_hide:
            self.visible = 1
            self.setWindowOpacity(self.visible)
            self._start_hide = False
            self._change_visible = False
            if self._timer_hide:
                self._timer_hide.stop()
                self._timer_hide.deleteLater()
            self._timer_hide = QTimer.singleShot(4000, self._start_animation)
        if self._change_visible:
            if self.visible < 0:
                self._change_visible = False
                self.hide()
            else:
                self.setWindowOpacity(self.visible)
                self.visible -=0.01
            
    def _start_animation(self):
        self._change_visible = True
        

        