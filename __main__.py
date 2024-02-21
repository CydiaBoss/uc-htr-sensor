import ctypes, sys
from logger import Logger

from main import Window

from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    # Update App ID if Windows
    myappid = 'medal.sensorfusion.h2'
    if sys.platform.startswith('win'):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Start Logger
    Logger()

    # Prep App Launch
    app = QApplication(sys.argv)
    win = Window()

    # Show
    win.show()

    # End
    sys.exit(app.exec())