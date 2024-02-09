from io import TextIOWrapper
from threading import Thread

from pathlib import Path
import sys, ctypes, time, re, atexit

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPixmap, QCloseEvent
from PyQt5 import QtCore
from controller import HTRSensorCtrl, HTRTester

from main_gui_new import Ui_MainWindow
from constants import *
from tools import active_ports, identical_list

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget
from pglive.sources.live_axis import LiveAxis

import main_rc

# Translate Component
_translate = QtCore.QCoreApplication.translate

# Run Data Collection
run_data_collect = True

# Data Storage
resistance = []
humidity = []
temperature = []

class Window(Ui_MainWindow):

    def __init__(self, parent=None):
        # Setup Basic Stuff
        main_rc.qInitResources()
        super().__init__(parent)
        self.setupUi(self)

        # Setup Graphs
        self.setup_plots()

        # Setup Ports
        self.htr_port : str = None
        self.qcm_port : str = None

        # Setup Dropdowns
        self.ports = []
        self.update_ports()

        # Main Logic
        # Connection to Sensors
        # self.statusBar().showMessage("Looking for sensor controller...")
        # self.ctrl = HTRSensorCtrl(baud=BAUD, timeout=SENSOR_TIMEOUT)
        # self.statusBar().clearMessage()
        # self.htr_thread = None

        # # Auto Start if connected
        # if self.ctrl.connected:
        #     self.statusBar().showMessage(f"Connected to sensor at port {self.ctrl.sensor.port}!")
        #     self.ctrl.update_ref_resist(REF_RESIST, REF_RESIST_UNIT)
        #     self.ctrl.update_ref_volt(REF_VOLT)
        #     self.statusBar().clearMessage()
        #     self.statusBar().showMessage("Reference values configured.", 2500)
        #     self.start_btn.setEnabled(True)

        # else:
        #     self.statusBar().showMessage("No sensors found, Please connect the sensor controller to this computer.")

    def setup_plots(self):
        '''
        Setups the graphs for live data collectrion
        '''
        # Setup Resistance Graph
        self.htr_layout.removeWidget(self.resist_plot)
        self.resist_plot.setParent(None)
        self.resist_plot.deleteLater()
        self.resist_axis = LiveAxis('left', text=_translate("MainWindow", "Resistance"), units="Ohm", unitPrefix=REF_RESIST_UNIT.strip())
        self.resist_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Resistance"), axisItems={"left": self.resist_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Resistance") + f" ({REF_RESIST_UNIT}Ohm)", "bottom": _translate("MainWindow", "Time")})
        self.resist_curve = LiveLinePlot(brush="red", pen="red")
        self.resist_plot.addItem(self.resist_curve)
        self.resist_plot.setBackground(background="w")
        self.resist_plot.show_crosshair()
        self.resist_data = DataConnector(self.resist_curve, max_points=300, update_rate=1.0)
        self.htr_layout.addWidget(self.resist_plot)
        
        # Setup Humidity Graph
        self.htr_layout.removeWidget(self.humd_plot)
        self.humd_plot.setParent(None)
        self.humd_plot.deleteLater()
        self.humd_axis = LiveAxis('left', text=_translate("MainWindow", "Humidity"), units="%RH")
        self.humd_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Humidity"), axisItems={"left": self.humd_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Humidity") + " (%RH)", "bottom": _translate("MainWindow", "Time")})
        self.humd_curve = LiveLinePlot(brush="green", pen="green")
        self.humd_plot.addItem(self.humd_curve)
        self.humd_plot.setBackground(background="w")
        self.humd_plot.show_crosshair()
        self.humd_data = DataConnector(self.humd_curve, max_points=300, update_rate=1.0)
        self.htr_layout.addWidget(self.humd_plot)
        
        # Setup Temperature Graph
        self.htr_layout.removeWidget(self.temp_plot)
        self.temp_plot.setParent(None)
        self.temp_plot.deleteLater()
        self.temp_axis = LiveAxis('left', text=_translate("MainWindow", "Temperature"), units="degC")
        self.temp_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Temperature"), axisItems={"left": self.temp_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Temperature") + " (degC)", "bottom": _translate("MainWindow", "Time")})
        self.temp_curve = LiveLinePlot(brush="blue", pen="blue")
        self.temp_plot.addItem(self.temp_curve)
        self.temp_plot.setBackground(background="w")
        self.temp_plot.show_crosshair()
        self.temp_data = DataConnector(self.temp_curve, max_points=300, update_rate=1.0)
        self.htr_layout.addWidget(self.temp_plot)
        
        # Setup Amplitude Graph
        self.qcm_layout.removeWidget(self.amp_plot)
        self.amp_plot.setParent(None)
        self.amp_plot.deleteLater()
        self.amp_axis = LiveAxis('left', text=_translate("MainWindow", "Amplitude"), units="dB")
        self.amp_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Amplitude"), axisItems={"left": self.amp_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Amplitude") + " (dB)", "bottom": _translate("MainWindow", "Time")})
        self.amp_curve = LiveLinePlot(brush="blue", pen="blue")
        self.amp_plot.addItem(self.amp_curve)
        self.amp_plot.setBackground(background="w")
        self.amp_data = DataConnector(self.amp_curve, max_points=300, update_rate=1.0)
        self.qcm_layout.addWidget(self.amp_plot, 0, 0, 1, 1)
        
        # Setup Phase Graph
        self.qcm_layout.removeWidget(self.phase_plot)
        self.phase_plot.setParent(None)
        self.phase_plot.deleteLater()
        self.phase_axis = LiveAxis('left', text=_translate("MainWindow", "Phase"), units="deg")
        self.phase_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Phase"), axisItems={"left": self.phase_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Phase") + " (deg)", "bottom": _translate("MainWindow", "Time")})
        self.phase_curve = LiveLinePlot(brush="blue", pen="blue")
        self.phase_plot.addItem(self.phase_curve)
        self.phase_plot.setBackground(background="w")
        self.phase_data = DataConnector(self.phase_curve, max_points=300, update_rate=1.0)
        self.qcm_layout.addWidget(self.phase_plot, 0, 1, 1, 1)
        
        # Setup Frequency Graph
        self.qcm_layout.removeWidget(self.freq_plot)
        self.freq_plot.setParent(None)
        self.freq_plot.deleteLater()
        self.freq_axis = LiveAxis('left', text=_translate("MainWindow", "Frequency"), units="Hz")
        self.freq_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Frequency"), axisItems={"left": self.freq_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Frequency") + " (dB)", "bottom": _translate("MainWindow", "Time")})
        self.freq_curve = LiveLinePlot(brush="blue", pen="blue")
        self.freq_plot.addItem(self.freq_curve)
        self.freq_plot.setBackground(background="w")
        self.freq_data = DataConnector(self.freq_curve, max_points=300, update_rate=1.0)
        self.qcm_layout.addWidget(self.freq_plot, 1, 0, 1, 1)
        
        # Setup Dissipation Graph
        self.qcm_layout.removeWidget(self.dissipate_plot)
        self.dissipate_plot.setParent(None)
        self.dissipate_plot.deleteLater()
        self.dissipate_axis = LiveAxis('left', text=_translate("MainWindow", "Dissipation"), units="ppm")
        self.dissipate_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Dissipation"), axisItems={"left": self.dissipate_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Dissipation") + " (ppm)", "bottom": _translate("MainWindow", "Time")})
        self.dissipate_curve = LiveLinePlot(brush="blue", pen="blue")
        self.dissipate_plot.addItem(self.dissipate_curve)
        self.dissipate_plot.setBackground(background="w")
        self.dissipate_data = DataConnector(self.dissipate_curve, max_points=300, update_rate=1.0)
        self.qcm_layout.addWidget(self.dissipate_plot, 1, 1, 1, 1)

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

    def update_ports(self):
        """
        Update available ports to select
        """
        # Ping for
        old_ports = self.ports
        self.ports = active_ports()

        # Add Used Ports to list
        if self.htr_port is not None:
            self.ports.append(self.htr_port)
        if self.qcm_port is not None:
            self.ports.append(self.qcm_port)

        # Ignore if nothing changed
        if identical_list(old_ports, self.ports):
            return
        
        # Remove all menu items
        self.htr_serial.clear()
        self.qcm_serial.clear()

        # Add New COM Menu
        for port in self.ports:
            self.htr_serial.addItem(port)
            self.qcm_serial.addItem(port)

        # Add Used Ports to list
        if self.htr_port is not None:
            self.htr_serial.setCurrentText(self.htr_port)
        if self.qcm_port is not None:
            self.qcm_serial.setCurrentText(self.qcm_port)

    def test_htr_port(self):
        '''
        Test the HTR port for success
        '''
        # Lock Connect Button for now
        self.connect_btn.setEnabled(False)
        self.htr_serial.setEnabled(False)

        # Prepare QThread
        self.htr_thread = QtCore.QThread()

        # Reset Status Icon for Both 
        self.htr_status.setPixmap(QPixmap(":/main/mark.png"))

        # Connection to HTR Sensor
        self.statusBar().showMessage(f"Validating port {self.htr_serial.currentText()} for HTR...")

        # Start Worker
        self.htr_tester = HTRTester(self.htr_serial.currentText())
        self.htr_thread.moveToThread(self.htr_tester)

        # Signal/Slots
        self.htr_thread.started.connect(self.htr_tester.run)
        self.htr_tester.finished.connect(self.htr_thread.quit)
        self.htr_tester.finished.connect(self.htr_tester.deleteLater)
        self.htr_thread.finished.connect(self.htr_thread.deleteLater)
        self.htr_tester.results.connect(self._htr_test_results)

        # Run
        self.htr_thread.start()

    def _htr_test_results(self, results : bool):
        '''
        Determine Success
        '''
        if not results:
            self.htr_status.setPixmap(QPixmap(":/main/cross.png"))
            self.statusBar().showMessage(f"Port {self.htr_serial.currentText()} is not the HTR")
        else:
            self.htr_status.setPixmap(QPixmap(":/main/check.png"))
            self.statusBar().showMessage(f"Port {self.htr_serial.currentText()} is the HTR")

        # Unlock
        self.connect_btn.setEnabled(True)
        self.htr_serial.setEnabled(True)

    def start_htr(self):
        '''
        Start running HTR sampling
        '''
        # Ensure connected
        if not self.ctrl.connected:
            self.statusBar().showMessage("No sensor connected to start HTR")
            return
        
        # Ensure not already running
        if self.htr_thread is not None:
            self.statusBar().showMessage("Already running HTR data collection")
            return
        
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
        self.htr_thread = Thread(daemon=True, target=self.data_collection, args=(export,))
        self.htr_thread.start()
        
        # Disable start button
        self.start.setEnabled(False)
    
    # Slots
    @QtCore.pyqtSlot()
    def on_action_Quit_triggered(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_action_Refresh_triggered(self):
        self.update_ports()

    @QtCore.pyqtSlot()
    def on_connect_btn_clicked(self):
        # Ensure something is selected
        if self.htr_serial.currentIndex() == -1 or self.qcm_serial.currentIndex() == -1:
            self.statusBar().showMessage("Nothing to connect to...", 5000)
            return
        
        # Test HTR
        self.test_htr_port()

    @QtCore.pyqtSlot()
    def on_startButton_clicked(self):
        self.start_htr()

    # Events
    def closeEvent(self, a0: QCloseEvent) -> None:
        # Ask for confirmation before closing
        confirmation = QMessageBox.question(self, "Confirmation", "Are you sure you want to close the application?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            a0.accept()
        else:
            a0.ignore() 

if __name__ == "__main__":
    # Update App ID if Windows
    myappid = 'medal.sensorfusion.h2'
    if sys.platform.startswith('win'):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Prep App Launch
    app = QApplication(sys.argv)
    win = Window()

    # Show
    win.show()

    # End
    sys.exit(app.exec())