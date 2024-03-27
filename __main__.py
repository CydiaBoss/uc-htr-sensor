import os
import ctypes, sys

from multiprocessing import freeze_support 

from misc import lang
from misc.constants import APPID, SETTINGS
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

    # Grab System Language
    curr_lang_code = ""
    sys_trans = QTranslator()
    if sys_trans.load(QLocale.system(), "qtbase", "_", QLibraryInfo.location(QLibraryInfo.LibraryLocation.TranslationsPath)):
        print("TRANS: system language loaded")
        curr_lang_code = sys_trans.language()
        app.installTranslator(sys_trans)

    # Look for Language Pack
    if os.path.isfile("lang.qm"):
        tran = QTranslator()

        # Attempts to load file
        if tran.load("lang"):
            print('TRANS:', tran.language(), "loaded")
            curr_lang = tran.language()

            # Attempt to update qtbase
            base_tran = QTranslator()
            if base_tran.load(f"qtbase_{curr_lang}", QLibraryInfo.location(QLibraryInfo.LibraryLocation.TranslationsPath)):
                print("TRANS: Correlating qtbase loaded")

                # Install new qtbase language
                app.installTranslator(base_tran)

            # Install Pack
            curr_lang_code = curr_lang
            app.installTranslator(tran)

    # Otherwise, look at settings
    else:
        code = SETTINGS.get_setting("lang")

        if code is not None:
            tran = QTranslator()

            # Attempts to load file
            if tran.load(code, "lang"):
                print('TRANS:', tran.language(), "loaded")
                curr_lang = tran.language()

                # Attempt to update qtbase
                base_tran = QTranslator()
                if base_tran.load(f"qtbase_{curr_lang}", QLibraryInfo.location(QLibraryInfo.LibraryLocation.TranslationsPath)):
                    print("TRANS: Correlating qtbase loaded")

                    # Install new qtbase language
                    app.installTranslator(base_tran)

                # Install Pack
                curr_lang_code = curr_lang
                app.installTranslator(tran)

    # Update language dictionary
    SETTINGS.update_setting("lang", curr_lang_code)
    lang.retranslate_lang()

    win = Window()

    # Show
    win.show()

    # End
    sys.exit(app.exec())
