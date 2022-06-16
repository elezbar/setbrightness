from time import sleep
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QSlider
from PyQt6.QtCore import QSize, Qt, QTimer
from random import randint


class BrightnessWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, list_monitors: list):
        super().__init__()
        self.list_monitors = list_monitors
        self.visible = 1
        self.updated = True
        self.ready_update = True
        self.setStyleSheet("background-color: #1A1A1A; color: white; ")
        self.setFixedSize(QSize(65, 140))
        self.setGeometry(50, 60, 0, 0)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.Tool)
        self.timer_hide = QTimer.singleShot(2000, self.start_animation)
        self.timer_animation = QTimer()
        self.timer_animation.timeout.connect(self.hide_animation)


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
        i = randint(0, 100)
        self.slider.setRange(0, 100)
        self.slider.setValue(i)
        self.slider.valueChanged.connect(self._slider_change)
        layout.addWidget(self.slider)
        self.label = QLabel(str(i))
        self.label.setStyleSheet("""font-family: "Segoe UI";
                                    font-size: 13px;
                                    margin-bottom:5px;
                                    font-weight:600""")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

    def _slider_change(self, value):
        self.label.setText(str(value))
        # monitor = self.list_monitors[1]
        # monitor.set_brightness(value)
        self.start_hide()

    def start_hide(self):
        self.timer_animation.stop()
        if self.timer_hide:
            self.timer_hide.stop()
            self.timer_hide.deleteLater()
        self.visible = 1
        self.setWindowOpacity(self.visible)
        
        self.timer_hide = QTimer.singleShot(2000, self.start_animation)

    def start_animation(self):
        self.timer_animation.start(10)

    def hide_animation(self):
        self.setWindowOpacity(self.visible)
        self.visible -=0.01
        if self.visible < 0:
            self.timer_animation.stop()

        