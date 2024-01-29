# from controller import SensorCtrl
# import time

# # Connection to Snesors
# ctrl = SensorCtrl(port="COM5", baud=9600, timeout=.1)

# # Serial Monitor
# while True:
#     print(ctrl.read_from(), end="")
#     time.sleep(1.5)

from PyQt5.QtWidgets import QApplication

from main_gui import Ui_MainWindow
import sys

class Window(Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())