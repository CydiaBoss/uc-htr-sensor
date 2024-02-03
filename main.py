from io import TextIOWrapper
from threading import Thread
from typing import List

import numpy as np
from controller import SensorCtrl
from pathlib import Path
import sys, ctypes, time, re, atexit

from PyQt5.QtWidgets import QApplication, QAction
from PyQt5 import QtCore

from main_gui import Ui_MainWindow
from constants import *
from tools import active_ports, identical_list

# Run Data Collection
run_data_collect = True

# Data Storage
resistance = []
humidity = []
temperature = []

class Window(Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Show GUI
        self.show()

        # Main Logic
        # Connection to Sensors
        self.statusBar().showMessage("Looking for sensor controller...")

        # Start setup if sensor detected
        if len(self.ports) <= 0:
            self.statusBar().showMessage("No sensors found")
            return

        self.ctrl = SensorCtrl(baud=BAUD, timeout=SENSOR_TIMEOUT)
        self.statusBar().clearMessage()

        # Auto Start if connected
        if self.ctrl.connected:
            self.statusBar().showMessage(f"Connected to sensor at port {self.ctrl.sensor.port}!")
            self.ctrl.update_ref_resist(REF_RESIST, REF_RESIST_UNIT)
            self.ctrl.update_ref_volt(REF_VOLT)
            self.statusBar().clearMessage()
            self.statusBar().showMessage("Reference values configured.", 2500)

            # Auto Export Setup
            if AUTO_EXPORT:
                # Make data directory if not already
                Path("data/").mkdir(parents=True, exist_ok=True)

                # Look for export file
                filename = f"data-{int(time.time())}.csv"
                export = open(f"data/{filename}", "w", encoding="utf-8")
                atexit.register(lambda : export.close())
            
                # Grab latest data from sensors to make header in csv
                row = self.ctrl.read_from()

                # Parse Data row
                data = re.search(DATA_PARSE, row)
                print(f"{data.group(2)} {data.group(1)}Ω | {data.group(3)}%RH | {data.group(4)}°C")

                # Header
                export.write(f'"Time","Resistance ({data.group(1)}Ohm)","Humidity (%RH)","Temperature (degC)"\n"{time.strftime("%H:%M:%S", time.localtime())}","{data.group(2)}","{data.group(3)}","{data.group(4)}"\n')

                self.statusBar().clearMessage()
                self.statusBar().showMessage(f"Auto export enabled. Exporting to file {filename} in data folder.", 2500)
        
            # Initialize Data Collection
            data_collect = Thread(daemon=True, target=self.data_collection, args=(export,))
            data_collect.start()

        else:
            self.statusBar().showMessage("No sensors found, Please connect the sensor controller to this computer.")

    def data_collection(self, export : TextIOWrapper):
        '''
        Update the graphs on the GUI and handles auto export if needed
        '''
        # Counter
        x = 0

        # Loop
        while run_data_collect:
            # Grab next row
            row = self.ctrl.read_from()

            # Parse Data row
            data = re.search(DATA_PARSE, row)

            # Update Graph if not None
            if data is not None:
                # Ignore for inf
                if data.group(2) != "inf":
                    r_data = float(data.group(2))
                    self.resist_data.cb_append_data_point(r_data, x)
                    resistance.append(r_data)

                    # Calculate Resist AVG
                    resist_size = len(resistance)

                    self.resist_avg_sig.emit(str(round(sum(resistance)/resist_size, 2)) + f" {data.group(1)}Ω")

                    if resist_size > 15:
                        self.resist_avg_15_sig.emit(str(round(sum(resistance[-15:])/15, 2)) + f" {data.group(1)}Ω")
                    else:
                        self.resist_avg_15_sig.emit("N/A")

                    if resist_size > 50:
                        self.resist_avg_50_sig.emit(str(round(sum(resistance[-50:])/50, 2)) + f" {data.group(1)}Ω")
                    else:
                        self.resist_avg_50_sig.emit("N/A")

                h_data = float(data.group(3))
                t_data = float(data.group(4))

                self.humidity_data.cb_append_data_point(h_data, x)
                self.temperature_data.cb_append_data_point(t_data, x)

                humidity.append(h_data)
                temperature.append(t_data)

                # Calculate Humidity AVG
                humd_size = len(humidity)
                
                self.humd_avg_sig.emit(str(round(sum(humidity)/humd_size, 2)) + "%RH")

                if humd_size > 15:
                    self.humd_avg_15_sig.emit(str(round(sum(humidity[-15:])/15, 2)) + "%RH")
                else:
                    self.humd_avg_15_sig.emit("N/A")

                if humd_size > 50:
                    self.humd_avg_50_sig.emit(str(round(sum(humidity[-50:])/50, 2)) + "%RH")
                else:
                    self.humd_avg_50_sig.emit("N/A")

                # Calculate Temperature AVG
                temp_size = len(temperature)
                
                self.temp_avg_sig.emit(str(round(sum(temperature)/temp_size, 2)) + "°C")

                if temp_size > 15:
                    self.temp_avg_15_sig.emit(str(round(sum(temperature[-15:])/15, 2)) + "°C")
                else:
                    self.temp_avg_15_sig.emit("N/A")

                if temp_size > 50:
                    self.temp_avg_50_sig.emit(str(round(sum(temperature[-50:])/50, 2)) + "°C")
                else:
                    self.temp_avg_50_sig.emit("N/A")

            if AUTO_EXPORT and data is not None:
                # Write last row of data
                export.write(f'"{time.strftime("%H:%M:%S", time.localtime())}","{data.group(2)}","{data.group(3)}","{data.group(4)}"\n')

                # Output
                print(f"{data.group(2)} {data.group(1)}Ω | {data.group(3)}%RH | {data.group(4)}°C")

                # Auto Flush
                if x % AUTO_FLUSH == 0:
                    export.flush()

            # Delay a bit
            time.sleep(READ_DELAY)

            # Update x
            x += 1

    def updatePorts(self):
        """
        Update available ports to select
        """
        old_ports = self.ports
        self.ports = active_ports()
        if self.ctrl.sensor.is_open:
            self.ports.append(self.ctrl.sensor.port)

        # Ignore if nothing changed
        if identical_list(old_ports, self.ports):
            return
        
        # Remove all menu items
        for action_port in self.action_ports:
            self.menu_Connect.removeAction(action_port)

        # Add New COM Menu
        self.action_ports : List[QAction] = []
        _translate = QtCore.QCoreApplication.translate
        for port in self.ports:
            temp_port_action = QAction(self.mainWindow)
            temp_port_action.setObjectName(port)
            temp_port_action.setText(_translate("MainWindow", action_port.objectName().upper()))
            temp_port_action.setToolTip(_translate("MainWindow", "Switches to this port"))
            self.action_ports.append(temp_port_action)
            self.menu_Connect.addAction(temp_port_action)
    
    # Slots

    @QtCore.pyqtSlot()
    def on_action_Quit_triggered(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_action_Refresh_triggered(self):
        self.updatePorts()

if __name__ == "__main__":
    # Update App ID if Windows
    myappid = 'medal.sensorfusion.h2'
    if sys.platform.startswith('win'):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Prep App Launch
    app = QApplication(sys.argv)
    win = Window()

    # End
    sys.exit(app.exec())