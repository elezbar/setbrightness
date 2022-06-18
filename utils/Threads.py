from PyQt6.QtCore import QThread


class WindowKeyBoardWorker(QThread):
    def __init__(self, window):
        QThread.__init__(self)
        self.window = window
    def run(self):
        while True:
            key = self.window.stack_keys.get()
            if key == 0:
                self.window.brightness_up()
            elif key == 1:
                self.window.brightness_down()

