from threading import Thread
from controller import SensorCtrl

from PyQt5.QtWidgets import QApplication

from pglive.sources.data_connector import DataConnector

from main_gui import Ui_MainWindow
import sys, ctypes, os, time, re, atexit
from pathlib import Path

class Window(Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

def data_collection(ctrl : SensorCtrl, resist_data : DataConnector, humidity_data : DataConnector, temperature_data : DataConnector):
    '''
    Update the graphs on the GUI
    '''
    # Counter
    x = 0
    while True:
        # Grab next row
        row = ctrl.read_from()

        # Parse Data row
        data = re.search(r"([a-zA-Z ])Ω:(inf|\d+\.\d{2}),%RH:(inf|\d+\.\d{2}),°C:(inf|\d+\.\d{2})", row)

        # Update Graph if not None
        if data is not None:
            # Ignore for inf
            if data.group(2) != "inf":
                resist_data.cb_append_data_point(float(data.group(2)), x)
            humidity_data.cb_append_data_point(float(data.group(3)), x)
            temperature_data.cb_append_data_point(float(data.group(4)), x)

        # Delay a bit
        time.sleep(1)

        # Update x
        x += 1

if __name__ == "__main__":
    # Update App ID if Windows
    myappid = 'medal.sensorfusion.h2'
    if os.name == "nt":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Prep App Launch
    app = QApplication(sys.argv)
    win = Window()

    # Main Logic
    # Connection to Sensors
    ctrl = SensorCtrl(port="COM5", baud=9600, timeout=.1)

    win.show()
    
    Thread(target=data_collection, args=(ctrl, win.resist_data, win.humidity_data, win.temperature_data)).start()

    # End
    sys.exit(app.exec())

    # Make data directory if not already
    Path("data/").mkdir(parents=True, exist_ok=True)

    # Look for export file
    export = open(f"data/data-{int(time.time())}.csv", "w", encoding="utf-8")
    atexit.register(lambda : export.close())
    
    # Grab latest data from sensors to make header in csv
    row = ctrl.read_from()

    # Parse Data row
    data = re.search(r"([a-zA-Z ])Ω:(inf|\d+\.\d{2}),%RH:(inf|\d+\.\d{2}),°C:(inf|\d+\.\d{2})", row)
    print(f"{data.group(2)} {data.group(1)}Ω | {data.group(3)}%RH | {data.group(4)}°C")

    # Header
    export.write(f'"Resistance ({data.group(1)}Ohm)","Humidity (%RH)","Temperature (degC)"\n')

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