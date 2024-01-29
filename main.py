from controller import SensorCtrl

from PyQt5.QtWidgets import QApplication

from main_gui import Ui_MainWindow
import sys, ctypes, os, time, re, atexit
from pathlib import Path

class Window(Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    # # Update App ID if Windows
    # myappid = 'medal.sensorfusion.h2'
    # if os.name == "nt":
    #     ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # # Prep App Launch
    # app = QApplication(sys.argv)
    # win = Window()
    # win.show()
    # sys.exit(app.exec())

    # Make data directory if not already
    Path("data/").mkdir(parents=True, exist_ok=True)

    # Connection to Snesors
    ctrl = SensorCtrl(port="COM5", baud=9600, timeout=.1)

    # Look for export file
    export = open(f"data/data-{int(time.time())}.csv", "w", encoding="utf-8")
    atexit.register(lambda : export.close())
    
    # Grab latest data from sensors to make header in csv
    row = ctrl.read_from()

    # Parse Data row
    data = re.search(r"([a-zA-Z ])Ω:(inf|\d+\.\d{2}),%RH:(inf|\d+\.\d{2}),°C:(inf|\d+\.\d{2})", row)
    print(f"{data.group(2)} {data.group(1)}Ω | {data.group(3)}%RH | {data.group(4)}°C")

    # Header
    export.write(f'"Resistance ({data.group(1)}Ω)","Humidity (%RH)","Temperature (°C)"\n')

    # Flush counter
    f_counter = 1

    # Serial Monitor
    while True:
        # Write last row of data
        export.write(f'"{data.group(2)}","{data.group(3)}","{data.group(4)}"\n')
        f_counter += 1

        # Grab latest data from sensors
        row = ctrl.read_from()

        # Parse Data row
        data = re.search(r"([a-zA-Z ])Ω:(inf|\d+\.\d{2}),%RH:(inf|\d+\.\d{2}),°C:(inf|\d+\.\d{2})", row)
        print(f"{data.group(2)} {data.group(1)}Ω | {data.group(3)}%RH | {data.group(4)}°C")

        # Flush every 50 rows
        if f_counter >= 50:
            export.flush()
            f_counter = 0

        # Delay a bit
        time.sleep(1.5)