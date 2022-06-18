import json
import sys
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon

class TrayIcon(QSystemTrayIcon):

    def __init__(self, icon, win, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip("Test SystemTray")
        self.win = win  # <----- name it whatever you want ie self.abc will also work

        menu = QMenu(parent)
        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())

        self.setContextMenu(menu)
        self.activated.connect(self.trayiconclicked)

    def trayiconclicked(self, reason):
        print("SysTrayIcon left clicked")
        if reason == self.ActivationReason.Trigger:
            
            self.win.show()  # <--- if you named you attribute self.abc call self.abc here instead of self.win