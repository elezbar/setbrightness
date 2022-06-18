from time import sleep
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QSlider, QGraphicsOpacityEffect, QMainWindow 
from PyQt6.QtCore import QSize, Qt, QTimer, QPropertyAnimation, QAbstractAnimation

from random import randint
from utils import Monitor


class BrightnessWindow(QMainWindow):
    
    def __init__(self, monitor: Monitor, n):
        super().__init__()
        self.monitor = monitor
        self.visible = 1
        self.background = QWidget(self)

        self.updated = True
        self.ready_update = True
        self.background.setStyleSheet("background-color: #1A1A1A; color: white ")
        self.setFixedSize(QSize(45, 140))
        self.setGeometry(50+n*45, 60, 0, 0)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.Tool)
        self._timer_hide = None
        self._timer_animation = QTimer()
        self._change_visible = False
        # self._timer_animation.timeout.connect(self._hide_animation)
        layout = QVBoxLayout()
        self.slider = QSlider()
        self.slider.setGeometry(100, 0, 0, 0)
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
                                    font-weight:600;""")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.background.setLayout(layout)
        self.setCentralWidget(self.background)  
        effect = QGraphicsOpacityEffect(self, opacity=1.0)
        self.setGraphicsEffect(effect)
        self._animation = QPropertyAnimation(
            self,
            propertyName=b"opacity",
            targetObject=effect,
        )
        self._animation.setDuration(4000)
        self._animation.setKeyValueAt(0.0,1.0)
        self._animation.setKeyValueAt(0.75,1.0)
        self._animation.setKeyValueAt(1,0.0)
        self._animation.setDirection(QAbstractAnimation.Direction.Forward)
        # self._animation.finished.connect(lambda: self.hide())
        self.update()
       
        

    def update(self):
        # self.setWindowOpacity(self.visible)
        self.show()
        bri = int(self.monitor.brightness)
        self.label.setText(str(bri))
        self.slider.setValue(bri)
        self._animation.stop()
        self._animation.setCurrentTime(0)
        self._animation.start()

    def _slider_change(self, value):
        self.monitor.set_brightness(value)
        self.label.setText(str(value))
        self._start_hide = True
        self.update()
    