import sys
from PyQt6.QtGui import QIcon
from window import MainWindow
from PyQt6.QtWidgets import QApplication
from window import TrayIcon

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow(app.screens())
    tray_icon = TrayIcon(QIcon("monitor.png"), w)
    tray_icon.setVisible(True)
    tray_icon.show()
    app.exec()
    