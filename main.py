import sys
from window import MainWindow
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow(app.screens())
    w.show()
    app.exec()