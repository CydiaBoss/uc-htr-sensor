import ctypes
import sys

'''
This code is just for testing purposes. It serves no purpose in the application
'''

if __name__ == "__main__":
    # Update App ID if Windows
    myappid = 'medal.sensorfusion.h2'
    if sys.platform.startswith('win'):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Prep App Launch
    app = QtWidgets.QApplication(sys.argv)

    main_rc.qInitResources()

    win = Ui_MainWindow()
    win.setupUi(win)

    win.show()

    # End
    sys.exit(app.exec())