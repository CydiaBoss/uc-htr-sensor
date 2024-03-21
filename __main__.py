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

    # tran = QTranslator()
    # sys_lang = QLocale.system().name()
    # Try looking for base if not already
    # if tran.load("qt_ko", QLibraryInfo.location(QLibraryInfo.LibraryLocation.TranslationsPath)):
    #     app.installTranslator(tran)
    # if tran.load("qtbase_ko", QLibraryInfo.location(QLibraryInfo.LibraryLocation.TranslationsPath)):
    #     app.installTranslator(tran)
    # if tran.load(QLocale.system(), "qt", "_", QLibraryInfo.location(QLibraryInfo.LibraryLocation.TranslationsPath)):
    #     app.installTranslator(tran)
    # tran.load(QLocale.system(), "qt", "_", QLibraryInfo.location(QLibraryInfo.LibraryLocation.TranslationsPath))
    # print(tran.language())
    # tran.load("fr", "lang")
    # print(tran.language())
    # app.installTranslator(tran)

    win = Window()

    # Show
    win.show()

    # End
    sys.exit(app.exec())
