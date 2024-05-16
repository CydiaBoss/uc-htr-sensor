import ctypes, sys

from multiprocessing import freeze_support 

from misc.constants import APPID
from misc.logger import Logger

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen

from main import Window

import main_rc as _

if __name__ == "__main__":
    # Freeze Support
    freeze_support()
    
    # Update App ID if Windows
    if sys.platform.startswith("win"):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APPID)

    # Prep App Launch
    app = QApplication(sys.argv)

    # Show Splash
    pixmap = QPixmap(":/main/biomed.png")
    splash = QSplashScreen(pixmap)
    splash.show()

    # Process
    app.processEvents()

    # Start Logger
    Logger()

    # Setup Window
    win = Window()

    # Show
    win.show()
    splash.finish(win)

    # End
    sys.exit(app.exec())
