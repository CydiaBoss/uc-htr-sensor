from io import TextIOWrapper
from threading import Thread
from controller import SensorCtrl
from pathlib import Path
import sys, ctypes, time, re, atexit

from PyQt5.QtWidgets import QApplication
from pglive.sources.data_connector import DataConnector

from main_gui import Ui_MainWindow
from constants import *

class Window(Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

def data_collection(ctrl : SensorCtrl, export : TextIOWrapper, resist_data : DataConnector, humidity_data : DataConnector, temperature_data : DataConnector):
    '''
    Update the graphs on the GUI and handles auto export if needed
    '''
    # Counter
    x = 0

    # Loop
    while True:
        # Grab next row
        row = ctrl.read_from()

        # Parse Data row
        data = re.search(DATA_PARSE, row)

        # Update Graph if not None
        if data is not None:
            # Ignore for inf
            if data.group(2) != "inf":
                resist_data.cb_append_data_point(float(data.group(2)), x)
            humidity_data.cb_append_data_point(float(data.group(3)), x)
            temperature_data.cb_append_data_point(float(data.group(4)), x)

        if AUTO_EXPORT and data is not None:
            # Write last row of data
            export.write(f'"{data.group(2)}","{data.group(3)}","{data.group(4)}"\n')

            # Output
            print(f"{data.group(2)} {data.group(1)}Ω | {data.group(3)}%RH | {data.group(4)}°C")

            # Auto Flush
            if x % AUTO_FLUSH == 0:
                export.flush()

        # Delay a bit
        time.sleep(READ_DELAY)

        # Update x
        x += 1

if __name__ == "__main__":
    # Update App ID if Windows
    myappid = 'medal.sensorfusion.h2'
    if sys.platform.startswith('win'):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Prep App Launch
    app = QApplication(sys.argv)
    win = Window()

    # Main Logic
    # Connection to Sensors
    ctrl = SensorCtrl(port="COM5", baud=BAUD, timeout=SENSOR_TIMEOUT)
    ctrl.update_ref_resist(REF_RESIST, REF_RESIST_UNIT)
    ctrl.update_ref_volt(REF_VOLT)

    # Auto Export Setup
    if AUTO_EXPORT:
        # Make data directory if not already
        Path("data/").mkdir(parents=True, exist_ok=True)

        # Look for export file
        export = open(f"data/data-{int(time.time())}.csv", "w", encoding="utf-8")
        atexit.register(lambda : export.close())
    
        # Grab latest data from sensors to make header in csv
        row = ctrl.read_from()

        # Parse Data row
        data = re.search(DATA_PARSE, row)
        print(f"{data.group(2)} {data.group(1)}Ω | {data.group(3)}%RH | {data.group(4)}°C")

        # Header
        export.write(f'"Resistance ({data.group(1)}Ohm)","Humidity (%RH)","Temperature (degC)"\n"{data.group(2)}","{data.group(3)}","{data.group(4)}"\n')

    win.show()
    
    # Initialize Data Collection
    Thread(target=data_collection, args=(ctrl, export, win.resist_data, win.humidity_data, win.temperature_data)).start()

    # End
    sys.exit(app.exec())