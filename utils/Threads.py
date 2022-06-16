from PyQt6.QtCore import QThread


class VisibleThread(QThread):
    def __init__(self, key_window: str, dict_window: dict):
        QThread.__init__(self)
        self.key_window = key_window
        self.dict_window = dict_window

    def run(self):
        while self.dict_window[self.key_window].visible > 0:
            if self.dict_window[self.key_window].updated:
                self.sleep(2)
                self.dict_window[self.key_window].updated = False
            self.msleep(10)
            _vis = self.dict_window[self.key_window].visible
            self.dict_window[self.key_window].setWindowOpacity(_vis)
            self.dict_window[self.key_window].visible -= 0.01
        del self.dict_window[self.key_window]
