import ctypes, sys
from misc.constants import APPID

from misc.logger import Logger

from PyQt5.QtWidgets import QApplication

from main import Window

if __name__ == "__main__":
    # Update App ID if Windows
    if sys.platform.startswith("win"):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APPID)

    # Start Logger
    Logger()

    # Prep App Launch
    app = QApplication(sys.argv)
    win = Window()

    # Show
    win.show()

    # End
    sys.exit(app.exec())
