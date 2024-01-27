from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

import sys

class MainWindow(QMainWindow):
    '''
    Main Window
    '''

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("MEDAL Sensor Fusion")
 
        # setting  the geometry of window
        self.setGeometry(100, 100, 1000, 1000)

        # show all the widgets
        self.show()

# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = MainWindow()

# Start the Application
sys.exit(App.exec())