import os
import ctypes, sys

from multiprocessing import freeze_support 

from misc.constants import APPID
from misc.logger import Logger

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo

from main import Window

if __name__ == "__main__":
    # Freeze Support
    freeze_support()
    
    # Update App ID if Windows
    if sys.platform.startswith("win"):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APPID)

    # Start Logger
    # Logger()

    # Prep App Launch
    app = QApplication(sys.argv)

    # Look for Language Pack
    if os.path.isfile("lang.qm"):
        tran = QTranslator()

        # Attempts to load file
        if tran.load("lang"):
            print(tran.language(), "loaded")
            curr_lang = tran.language()

            # Install
            app.installTranslator(tran)

            # Attempt to update qtbase
            base_tran = QTranslator()
            if base_tran.load(f"qtbase_{curr_lang}", QLibraryInfo.location(QLibraryInfo.LibraryLocation.TranslationsPath)):
                print("Correct qtbase loaded")

                # Install new qtbase language
                app.installTranslator(base_tran)

    win = Window()

    # Show
    win.show()

    # End
    sys.exit(app.exec())
