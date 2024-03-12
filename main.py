import os, re, time
from datetime import datetime
from typing import Union

from misc.controller import HTRSensorCtrl, HTRTester, QCMSensorCtrl, QCMTester, RSensorCtrl
from misc.constants import *
from misc.data import DataSaving
from misc.tools import active_ports, identical_list, noise_filtering

from PyQt5.QtWidgets import QMessageBox, QFileDialog, QInputDialog, QFrame
from PyQt5.QtGui import QPixmap, QCloseEvent
from PyQt5 import QtCore
from numpy import loadtxt

from main_gui import Ui_MainWindow

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget
from pglive.sources.live_axis import LiveAxis

from nidaqmx.system.system import System

import main_rc

# Translate Component
_translate = QtCore.QCoreApplication.translate

class Window(Ui_MainWindow):

    def __init__(self, parent=None):
        # Initiate resources
        main_rc.qInitResources()

        # Setup Basic Stuff
        super().__init__(parent)
        self.setupUi(self)

        # Disable All
        self.disable_all_ctrls()

        # Setup Graphs
        self.setup_plots()

        # Setup Variables
        self.setup_variable()

        # Setup Signals
        self.setup_signals()

        # Enable Ports
        self.update_ports()
        self.enable_ports()

        # Startup Memory Stuff
        self.setup_memory()

        # Set Size
        self.setMinimumSize(QtCore.QSize(MIN_WIDTH, MIN_HEIGHT))
        self.resize(MIN_WIDTH, MIN_HEIGHT)

    def setup_plots(self):
        '''
        Setups the graphs for live data collectrion
        '''
        # Setup Resistance Graph
        self.htr_layout.removeWidget(self.resist_plot)
        self.resist_plot.setParent(None)
        self.resist_plot.deleteLater()
        self.resist_axis = LiveAxis('left', text=_translate("MainWindow", "Resistance"), units="Ω", unitPrefix=SETTINGS.get_setting("ref_resist_unit").strip())
        self.resist_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Resistance"), axisItems={"left": self.resist_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Resistance") + f" ({SETTINGS.get_setting('ref_resist_unit').strip()}Ω)", "bottom": _translate("MainWindow", "Time") + " (s)"})
        self.resist_curve = LiveLinePlot(brush="red", pen="red")
        self.resist_plot.addItem(self.resist_curve)
        self.resist_plot.setBackground(background="w")
        self.resist_plot.show_crosshair()
        self.resist_data = DataConnector(self.resist_curve, update_rate=1.0)
        self.htr_layout.addWidget(self.resist_plot)
        
        # Setup Humidity Graph
        self.htr_layout.removeWidget(self.humd_plot)
        self.humd_plot.setParent(None)
        self.humd_plot.deleteLater()
        self.humd_axis = LiveAxis('left', text=_translate("MainWindow", "Humidity"), units="%RH")
        self.humd_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Humidity"), axisItems={"left": self.humd_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Humidity") + " (%RH)", "bottom": _translate("MainWindow", "Time") + " (s)"})
        self.humd_curve = LiveLinePlot(brush="green", pen="green")
        self.humd_plot.addItem(self.humd_curve)
        self.humd_plot.setBackground(background="w")
        self.humd_plot.show_crosshair()
        self.humd_data = DataConnector(self.humd_curve, update_rate=1.0)
        self.htr_layout.addWidget(self.humd_plot)
        
        # Setup Temperature Graph
        self.htr_layout.removeWidget(self.temp_plot)
        self.temp_plot.setParent(None)
        self.temp_plot.deleteLater()
        self.temp_axis = LiveAxis('left', text=_translate("MainWindow", "Temperature"), units="degC")
        self.temp_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Temperature"), axisItems={"left": self.temp_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Temperature") + " (degC)", "bottom": _translate("MainWindow", "Time") + " (s)"})
        self.temp_curve = LiveLinePlot(brush="blue", pen="blue")
        self.temp_plot.addItem(self.temp_curve)
        self.temp_plot.setBackground(background="w")
        self.temp_plot.show_crosshair()
        self.temp_data = DataConnector(self.temp_curve, update_rate=1.0)
        self.htr_layout.addWidget(self.temp_plot)
        
        # Setup Amplitude Graph
        self.qcm_layout.removeWidget(self.amp_plot)
        self.amp_plot.setParent(None)
        self.amp_plot.deleteLater()
        self.amp_axis = LiveAxis('left', text=_translate("MainWindow", "Amplitude"), units="dB", unitPrefix="m")
        self.amp_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Amplitude"), axisItems={"left": self.amp_axis, "bottom": LiveAxis(**FREQ_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Amplitude") + " (dB)", "bottom": _translate("MainWindow", "Frequency") + " (Hz)"})
        self.amp_curve = LiveLinePlot(brush="blue", pen="blue")
        self.amp_plot.addItem(self.amp_curve)
        self.amp_plot.setBackground(background="w")
        self.amp_data = DataConnector(self.amp_curve, update_rate=1.0)
        self.qcm_layout.addWidget(self.amp_plot, 0, 0, 1, 1)
        
        # Setup Phase Graph
        self.qcm_layout.removeWidget(self.phase_plot)
        self.phase_plot.setParent(None)
        self.phase_plot.deleteLater()
        self.phase_axis = LiveAxis('left', text=_translate("MainWindow", "Phase"), units="deg")
        self.phase_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Phase"), axisItems={"left": self.phase_axis, "bottom": LiveAxis(**FREQ_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Phase") + " (deg)", "bottom": _translate("MainWindow", "Frequency") + " (Hz)"})
        self.phase_curve = LiveLinePlot(brush="blue", pen="blue")
        self.phase_plot.addItem(self.phase_curve)
        self.phase_plot.setBackground(background="w")
        self.phase_data = DataConnector(self.phase_curve, update_rate=1.0)
        self.qcm_layout.addWidget(self.phase_plot, 0, 1, 1, 1)
        
        # Setup Frequency Graph
        self.qcm_layout.removeWidget(self.freq_plot)
        self.freq_plot.setParent(None)
        self.freq_plot.deleteLater()
        self.freq_axis = LiveAxis('left', text=_translate("MainWindow", "Frequency"), units="Hz")
        self.freq_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Resonance Frequency"), axisItems={"left": self.freq_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Frequency") + " (Hz)", "bottom": _translate("MainWindow", "Time") + " (s)"})
        self.freq_curve = LiveLinePlot(brush="blue", pen="blue")
        self.freq_plot.addItem(self.freq_curve)
        self.freq_plot.setBackground(background="w")
        self.freq_data = DataConnector(self.freq_curve, update_rate=1.0)
        self.qcm_layout.addWidget(self.freq_plot, 1, 0, 1, 1)
        
        # Setup Dissipation Graph
        self.qcm_layout.removeWidget(self.dissipate_plot)
        self.dissipate_plot.setParent(None)
        self.dissipate_plot.deleteLater()
        self.dissipate_axis = LiveAxis('left', text=_translate("MainWindow", "Dissipation"), units="ppm")
        self.dissipate_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Dissipation"), axisItems={"left": self.dissipate_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Dissipation") + " (ppm)", "bottom": _translate("MainWindow", "Time") + " (s)"})
        self.dissipate_curve = LiveLinePlot(brush="blue", pen="blue")
        self.dissipate_plot.addItem(self.dissipate_curve)
        self.dissipate_plot.setBackground(background="w")
        self.dissipate_data = DataConnector(self.dissipate_curve, update_rate=1.0)
        self.qcm_layout.addWidget(self.dissipate_plot, 1, 1, 1, 1)
        
        # Set Indicator Colours
        odd_num = [1, 3, 5, 7, 9]
        for c in ['f', 'd']:
            for i in range(5):
                colour_frame : QFrame = getattr(self, f"{c}{odd_num[i]}_colour")
                colour_frame.setStyleSheet(f"background-color:{Constants.plot_color_multi[i]};")

    def clear_qcm_plots_multi(self, rebuild=True):
        """
        Resets the plots for single measurements
        """
        # Reset current data if any
        # Plots
        while self.multi_amp_curves:
            curve = self.multi_amp_curves.pop()
            self.amp_plot.removeItem(curve)
            curve.deleteLater()
        while self.multi_phase_curves:
            curve = self.multi_phase_curves.pop()
            self.phase_plot.removeItem(curve)
            curve.deleteLater()
        while self.multi_freq_curves:
            curve = self.multi_freq_curves.pop()
            self.freq_plot.removeItem(curve)
            curve.deleteLater()
        while self.multi_dissipate_curves:
            curve = self.multi_dissipate_curves.pop()
            self.dissipate_plot.removeItem(curve)
            curve.deleteLater()

        # Data Connectors
        while self.multi_amp_datas:
            self.multi_amp_datas.pop().deleteLater()
        while self.multi_phase_datas:
            self.multi_phase_datas.pop().deleteLater()
        while self.multi_freq_datas:
            self.multi_freq_datas.pop().deleteLater()
        while self.multi_dissipate_datas:
            self.multi_dissipate_datas.pop().deleteLater()

        self.multi_mode = False

        # Reset Everything if wanted
        if rebuild:
            self.setup_plots()

    def setup_qcm_plots_multi(self):
        """
        Convert the single plots to support multi
        """
        # Reset old
        self.clear_qcm_plots_multi(rebuild=False)

        # Add new multi plots
        for i in range(self.peaks.size):
            # Update Amplitude
            temp_amp_curve = LiveLinePlot(brush=Constants.plot_color_multi[i], pen=Constants.plot_color_multi[i])
            self.amp_plot.addItem(temp_amp_curve)
            temp_amp_data = DataConnector(temp_amp_curve, update_rate=1.0)
            self.multi_amp_curves.append(temp_amp_curve)
            self.multi_amp_datas.append(temp_amp_data)

            # Update Phase
            temp_phase_curve = LiveLinePlot(brush=Constants.plot_color_multi[i], pen=Constants.plot_color_multi[i])
            self.phase_plot.addItem(temp_phase_curve)
            temp_phase_data = DataConnector(temp_phase_curve, update_rate=1.0)
            self.multi_phase_curves.append(temp_phase_curve)
            self.multi_phase_datas.append(temp_phase_data)
            
            # Update Frequency
            temp_freq_curve = LiveLinePlot(brush=Constants.plot_color_multi[i], pen=Constants.plot_color_multi[i])
            self.freq_plot.addItem(temp_freq_curve)
            temp_freq_data = DataConnector(temp_freq_curve, update_rate=1.0)
            self.multi_freq_curves.append(temp_freq_curve)
            self.multi_freq_datas.append(temp_freq_data)
            
            # Update Dissipation
            temp_dissipate_curve = LiveLinePlot(brush=Constants.plot_color_multi[i], pen=Constants.plot_color_multi[i])
            self.dissipate_plot.addItem(temp_dissipate_curve)
            temp_dissipate_data = DataConnector(temp_dissipate_curve, update_rate=1.0)
            self.multi_dissipate_curves.append(temp_dissipate_curve)
            self.multi_dissipate_datas.append(temp_dissipate_data)

        # Signal multi mode
        self.multi_mode = True

    def setup_variable(self):
        """
        Setup all the local variables
        """
        # Setup Ports
        self.htr_port : str = None
        self.qcm_port : str = None
        self.r_device : str = None

        # Setup Dropdowns
        self.ports = []

        # Setup Controllers
        self.htr_ctrl : HTRSensorCtrl = None
        self.qcm_ctrl : QCMSensorCtrl = None
        self.r_ctrl : RSensorCtrl = None

        # Setup Thread
        self.htr_thread : QtCore.QThread = None
        self.qcm_thread : QtCore.QThread = None
        self.r_thread : QtCore.QThread = None
        self.qcm_timer : QtCore.QTimer = None

        # Make Calibration Stuff
        self.qcm_calibrated = False
        self.peaks = np.array([])

        # Setup Multi Plot
        self.multi_mode = False
        self.multi_amp_curves : list[LiveLinePlot] = []
        self.multi_phase_curves : list[LiveLinePlot] = []
        self.multi_freq_curves : list[LiveLinePlot] = []
        self.multi_dissipate_curves : list[LiveLinePlot] = []
        self.multi_amp_datas : list[DataConnector] = []
        self.multi_phase_datas : list[DataConnector] = []
        self.multi_freq_datas : list[DataConnector] = []
        self.multi_dissipate_datas : list[DataConnector] = []

        # Data Storage
        # HTR
        self.raw_resistance = np.array([])
        self.resistance = np.array([])
        self.humidity = np.array([])
        self.htr_temperature = np.array([])
        self.resistance_time = np.array([])
        self.humidity_time = np.array([])
        self.htr_temperature_time = np.array([])
        self.htr_time = np.array([])
        self.r_time = np.array([])
        # QCM
        self.frequency = np.array([])
        self.dissipation = np.array([])
        self.qcm_temperature = np.array([])
        self.qcm_time = np.array([])

        # Read Noise Reduction value
        self.noise_reduce = int(SETTINGS.get_setting("noise_reduce"))

        # Data Saving Module
        self.data_saver : DataSaving = None
        self.data_saving_thread : QtCore.QThread = None
        self.data_saving_timer : QtCore.QTimer = None

        # Fill Frequency List
        self.fill_frequency_list()

        # Update Perm Status
        self.update_perm_status(_translate("MainWindow", "Not Ready"))

        # Setup Style
        # QProgressBar
        self.setStyleSheet(QPB_DEFAULT_STYLE)

        # Update Ohm SI Mult
        self.resist_label.setText(_translate("MainWindow", f'<html><head/><body><p><span style=" font-weight:600;">Resistance ({SETTINGS.get_setting("ref_resist_unit").strip()}Ω)</span></p></body></html>'))

    def setup_signals(self):
        """
        Setup all essential connections
        """
        # Port Detection singal
        self.htr_serial.currentIndexChanged.connect(self.port_conflict_detection)
        self.qcm_serial.currentIndexChanged.connect(self.port_conflict_detection)

        # Measurement Selection
        self.measure_type.currentIndexChanged.connect(lambda : self.freq_list.setEnabled(self.measure_type.currentIndex() == 0))

    def setup_memory(self):
        """
        Restore previous positions
        """
        # Restore COM selection
        htr_serial_memory = SETTINGS.get_setting("last_htr_port")
        qcm_serial_memory = SETTINGS.get_setting("last_qcm_port")

        if htr_serial_memory is not None and self.htr_serial.findText(htr_serial_memory) != -1:
            self.htr_serial.setCurrentText(htr_serial_memory)

        if qcm_serial_memory is not None and self.qcm_serial.findText(qcm_serial_memory) != -1:
            self.qcm_serial.setCurrentText(qcm_serial_memory)

        # Restore QC Chip Type selection
        qc_type = SETTINGS.get_setting("last_qc_chip")

        if qc_type is not None:
            self.qc_type.setCurrentText(qc_type)

        # Restore Measurement Selections
        measurement_type = SETTINGS.get_setting("measurement_mode")
        freq_select = SETTINGS.get_setting("freq_select")

        if measurement_type is not None:
            self.measure_type.setCurrentIndex(int(measurement_type))
        if freq_select is not None and len(self.freq_list) > int(freq_select):
            self.freq_list.setCurrentIndex(int(freq_select))

        # Restore File Management Selections
        auto_export_opt = SETTINGS.get_setting("auto_export")
        last_file_dest = SETTINGS.get_setting("last_file_dest")

        if auto_export_opt is not None:
            self.auto_export.setChecked(bool(auto_export_opt))
            self.file_dest.setEnabled(False)
            self.file_select.setEnabled(False)
        if last_file_dest is not None:
            self.file_dest.setText(last_file_dest)

    def disable_all_ctrls(self):
        """
        Disable all controls
        """
        # Ports
        self.htr_serial.setEnabled(False)
        self.qcm_serial.setEnabled(False)
        self.connect_btn.setEnabled(False)
        self.action_Scan_Connections.setEnabled(False)
        self.action_Disconnect.setEnabled(False)

        # Calibration
        self.qc_type.setEnabled(False)
        self.calibrate_btn.setEnabled(False)
        
        # Measurement
        self.measure_type.setEnabled(False)
        self.freq_list.setEnabled(False)

        # Exportation
        self.auto_export.setEnabled(False)
        self.file_dest.setEnabled(False)
        self.file_select.setEnabled(False)

        # Start
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.reset_btn.setEnabled(False)

    def reset_calibration_bar(self):
        """
        Reset Calibration Bar
        """
        self.calibration_bar.setValue(0)
        self.calibration_bar.setStyleSheet("")

    def reset_progress_bar(self):
        """
        Reset Progress Bar
        """
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("")

    def enable_ports(self):
        """
        Enable all port ctrls
        """
        self.htr_serial.setEnabled(True)
        if self.qcm_port is None or not self.qcm_calibrated:
            self.qcm_serial.setEnabled(True)

        if self.htr_serial.currentText() != self.qcm_serial.currentText():
            self.connect_btn.setEnabled(True)

        self.action_Scan_Connections.setEnabled(True)
        if self.r_device is not None:
            self.action_Disconnect.setEnabled(True)

    def enable_daq_indicator(self):
        """
        Control DAQ indicator
        """
        self.daq_label.setEnabled(True)
        self.daq_status.setEnabled(True)
        self.daq_device.setEnabled(True)

    def disable_daq_indicator(self):
        """
        Control DAQ indicator
        """
        self.daq_label.setEnabled(False)
        self.daq_status.setPixmap(QPixmap(":/main/mark.png"))
        self.daq_status.setEnabled(False)
        self.daq_device.setText("")
        self.daq_device.setEnabled(False)

    def enable_calibrate(self):
        """
        Enable all calibration ctrls
        """
        self.qc_type.setEnabled(True)
        self.calibrate_btn.setEnabled(True)

    def fill_frequency_list(self):
        """
        Fills the frequency list from the file
        """
        # Populate frequency list
        self.freq_list.clear()

        # Read list
        try:
            data  = loadtxt(Constants.cvs_peakfrequencies_path)
            self.peaks = data[:,0]

            for peak in self.peaks:
                self.freq_list.addItem(f"{peak} Hz")
        except FileNotFoundError:
            pass

    def enable_measurement(self):
        """
        Enable all measurement ctrls
        """
        self.measure_type.setEnabled(True)

        # Reread
        self.fill_frequency_list()

        if self.measure_type.currentIndex() == 0:
            self.freq_list.setEnabled(True)

    def enable_export(self):
        """
        Enable all export ctrls
        """
        self.auto_export.setEnabled(True)

        # Enable other stuff if also true
        if self.auto_export.isChecked():
            self.file_dest.setEnabled(True)
            self.file_select.setEnabled(True)

            # Trigger slot
            self.on_auto_export_clicked()

    def enable_start(self):
        """
        Enable all start ctrls
        """
        self.start_btn.setEnabled(True)

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
            # Update
            self.statusBar().showMessage("No New Ports Discovered", 5000)
            return
        
        # Remove all menu items
        self.htr_serial.clear()
        self.qcm_serial.clear()

        # Add empty placeholder
        self.htr_serial.addItem("---")
        self.qcm_serial.addItem("---")

        # Add New COM Menu
        for port in self.ports:
            self.htr_serial.addItem(port)
            self.qcm_serial.addItem(port)

        # Add Used Ports to list
        if self.htr_port is not None:
            self.htr_serial.setCurrentText(self.htr_port)
        if self.qcm_port is not None:
            self.qcm_serial.setCurrentText(self.qcm_port)

        # Update
        self.statusBar().showMessage("New Ports Discovered", 5000)

    def look_for_daq(self):
        """
        Detect the DAQ sensor
        """
        # Look for DAQs for resistance replacement
        if len(System.local().devices) > 0:
            r_daq = QInputDialog.getItem(self, _translate("MainWindow", "DAQ Detected"), _translate("MainWindow", "It seems that there are DAQs attached to the computer. Is one of them the resistor sensor?\nThe HTR's resistor sensor will be disabled if so."), [x.name for x in System.local().devices], editable=False)
            
            # Look for r_daq
            if r_daq[1]:
                self.r_device = r_daq[0]

                # Success
                self.statusBar().showMessage(f"DAQ {r_daq[0]} selected", 5000)

        else:
            self.statusBar().showMessage(f"No DAQ detected", 5000)

    def update_perm_status(self, msg : str):
        """
        Update the status info box
        """
        self.perm_status.setText("<font color=#0000ff > Status </font>" + msg)

    def port_conflict_detection(self):
        """
        Ensures valid port selection
        """
        # Cannot have matching ports
        if self.htr_serial.currentText() == self.qcm_serial.currentText():
            self.statusBar().showMessage("HTR and QCM cannot be on same port", 2500)
        # Does anything seem new?
        elif self.htr_serial.currentText() != self.htr_port or self.qcm_serial.currentText() != self.qcm_port:
            self.connect_btn.setEnabled(True)
            return
        
        # Keep disabled otherwise
        self.connect_btn.setEnabled(False)

    def test_htr_port(self):
        '''
        Test the HTR port for success
        '''
        # Reset Port String
        self.htr_port = None

        # Prepare QThread
        self.htr_thread = QtCore.QThread(self)

        # Reset Status Icon for Both 
        self.htr_status.setPixmap(QPixmap(":/main/mark.png"))

        # Start Worker
        self.htr_tester = HTRTester(port=self.htr_serial.currentText())
        self.htr_tester.moveToThread(self.htr_thread)

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
            self.statusBar().showMessage(f"Port {self.htr_serial.currentText()} is not the HTR", 5000)
        else:
            self.htr_status.setPixmap(QPixmap(":/main/check.png"))
            self.statusBar().showMessage(f"Port {self.htr_serial.currentText()} is the HTR", 5000)
            self.update_perm_status(_translate("MainWindow", "HTR Ready"))
            self.htr_port = self.htr_serial.currentText()
            SETTINGS.update_setting("last_htr_port", self.htr_port)
            self.enable_export()
            self.enable_start()

        # Unlock
        if self.qcm_serial.isEnabled() or self.qcm_serial.currentIndex() == 0:
            self.enable_ports()
        self.htr_serial.setEnabled(True)

        # Casually Look for DAQ also
        self.on_action_Scan_Connections_triggered()

    def test_qcm_port(self):
        '''
        Test the QCM port for success
        '''
        # Reset QCM port
        self.qcm_port = None

        # Prepare QThread
        self.qcm_thread = QtCore.QThread(self)

        # Reset Status Icon for Both 
        self.qcm_status.setPixmap(QPixmap(":/main/mark.png"))

        # Start Worker
        self.qcm_tester = QCMTester(port=self.qcm_serial.currentText())
        self.qcm_tester.moveToThread(self.qcm_thread)

        # Signal/Slots
        self.qcm_thread.started.connect(self.qcm_tester.run)
        self.qcm_tester.finished.connect(self.qcm_thread.quit)
        self.qcm_tester.finished.connect(self.qcm_tester.deleteLater)
        self.qcm_thread.finished.connect(self.qcm_thread.deleteLater)
        self.qcm_tester.results.connect(self._qcm_test_results)

        # Run
        self.qcm_thread.start()

    def _qcm_test_results(self, results : bool):
        '''
        Determine Success
        '''
        if not results:
            self.qcm_status.setPixmap(QPixmap(":/main/cross.png"))
            self.statusBar().showMessage(f"Port {self.qcm_serial.currentText()} is not the QCM", 5000)
        else:
            self.qcm_status.setPixmap(QPixmap(":/main/check.png"))
            self.statusBar().showMessage(f"Port {self.qcm_serial.currentText()} is the QCM", 5000)
            self.qcm_port = self.qcm_serial.currentText()
            SETTINGS.update_setting("last_qcm_port", self.qcm_port)
            self.enable_calibrate()

        # Unlock
        if self.htr_serial.isEnabled() or self.htr_serial.currentIndex() == 0:
            self.enable_ports()
        self.qcm_serial.setEnabled(True)

    def start_r(self):
        '''
        Start running R sampling
        '''
        # Make Data Thread
        self.r_thread = QtCore.QThread(self)
        
        # Create controller
        self.r_ctrl = RSensorCtrl(device=self.r_device, voltage=float(SETTINGS.get_setting("ref_volt")), reference_resist=float(SETTINGS.get_setting("ref_resist")))
        self.r_ctrl.moveToThread(self.r_thread)

        # Signal/Slots
        self.r_thread.started.connect(self.r_ctrl.run)
        self.r_ctrl.progress.connect(self.update_r_time)
        self.r_ctrl.resistance.connect(self.resistance_processing)
        self.r_ctrl.finished.connect(self.r_thread.quit)
        self.r_ctrl.finished.connect(self.r_ctrl.deleteLater)
        self.r_thread.finished.connect(self.r_thread.deleteLater)
    
        # Initialize Data Collection
        self.r_thread.start()

    def update_r_time(self):
        """
        Update the time array for r
        """
        temp_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.r_time = np.append(self.r_time, temp_time)

        # Queue for data saving if needed
        if self.data_saver is not None:
            self.data_saver.r_time.put(temp_time)

    def start_htr(self):
        '''
        Start running HTR sampling
        '''
        # Make Data Thread
        self.htr_thread = QtCore.QThread(self)
        
        # Create controller
        self.htr_ctrl = HTRSensorCtrl(port=self.htr_port, baud=BAUD, timeout=SENSOR_TIMEOUT)
        self.htr_ctrl.moveToThread(self.htr_thread)

        # Signal/Slots
        self.htr_thread.started.connect(self.htr_ctrl.run)
        self.htr_ctrl.progress.connect(self.update_htr_time)

        # Ignore if r_device is None
        if self.r_device is None:
            self.htr_ctrl.resistance.connect(self.resistance_processing)

        self.htr_ctrl.humidity.connect(self.humidity_processing)
        self.htr_ctrl.temperature.connect(self.htr_temperature_processing)
        self.htr_ctrl.finished.connect(self.htr_thread.quit)
        self.htr_ctrl.finished.connect(self.htr_ctrl.deleteLater)
        self.htr_thread.finished.connect(self.htr_thread.deleteLater)
    
        # Initialize Data Collection
        self.htr_thread.start()

    def update_htr_time(self):
        """
        Update the time array for htr
        """
        temp_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.htr_time = np.append(self.htr_time, temp_time)

        # Queue for data saving if needed
        if self.data_saver is not None:
            self.data_saver.htr_time.put(temp_time)

    def resistance_processing(self, time_at : float, r_data : float):
        """
        Processes the resistance data
        """
        # Queue for data saving if needed
        if self.data_saver is not None:
            if self.r_device is not None:
                self.data_saver.r_resist.put(r_data)
            else:
                self.data_saver.htr_resist.put(r_data)

        # Don't do anything for inf
        if r_data == np.inf:
            self.raw_resistance = np.append(self.raw_resistance, r_data)
            return
        
        # Add to list
        self.raw_resistance = np.append(self.raw_resistance, r_data)
        self.resistance = np.append(self.resistance, r_data)
        self.resistance_time = np.append(self.resistance_time, time_at)

        # Plot with noise filter
        self.resist_data.cb_set_data(noise_filtering(self.resistance, self.noise_reduce), self.resistance_time)

        # Calculate Resist AVGs
        resist_size = self.resistance.size

        self.resist_avg.setText(str(round(self.resistance.mean(), 2)) + f" {SETTINGS.get_setting('ref_resist_unit')}Ω")

        if resist_size > 15:
            self.avg_resist_15.setText(str(round(self.resistance[-15:].mean(), 2)) + f" {SETTINGS.get_setting('ref_resist_unit')}Ω")
        else:
            self.avg_resist_15.setText("N/A")

        if resist_size > 50:
            self.avg_resist_50.setText(str(round(self.resistance[-50:].mean(), 2)) + f" {SETTINGS.get_setting('ref_resist_unit')}Ω")
        else:
            self.avg_resist_50.setText("N/A")

    def humidity_processing(self, time_at : float, h_data : float):
        """
        Processes the humidity data
        """
        # Queue for data saving if needed
        if self.data_saver is not None:
            self.data_saver.htr_humid.put(h_data)

        # Add to list
        self.humidity = np.append(self.humidity, h_data)
        self.humidity_time = np.append(self.humidity_time, time_at)

        # Plot
        self.humd_data.cb_set_data(noise_filtering(self.humidity, self.noise_reduce), self.humidity_time)

        # Calculate Humidity AVGs
        humd_size = self.humidity.size
        
        self.humd_avg.setText(str(round(self.humidity.mean(), 2)) + "%RH")

        if humd_size > 15:
            self.humd_avg_15.setText(str(round(self.humidity[-15:].mean(), 2)) + "%RH")
        else:
            self.humd_avg_15.setText("N/A")

        if humd_size > 50:
            self.humd_avg_50.setText(str(round(self.humidity[-50:].mean(), 2)) + "%RH")
        else:
            self.humd_avg_50.setText("N/A")

    def htr_temperature_processing(self, time_at : float, t_data : float):
        """
        Processes the temperature data
        """
        # Queue for data saving if needed
        if self.data_saver is not None:
            self.data_saver.htr_temp.put(t_data)

        # Add to list
        self.htr_temperature = np.append(self.htr_temperature, t_data)
        self.htr_temperature_time = np.append(self.htr_temperature_time, time_at)

        # Plot
        self.temp_data.cb_set_data(noise_filtering(self.htr_temperature, self.noise_reduce), self.htr_temperature_time)

        # Calculate Temperature AVGs
        temp_size = self.htr_temperature.size
        
        self.temp_avg.setText(str(round(self.htr_temperature.mean(), 2)) + "°C")

        if temp_size > 15:
            self.temp_avg_15.setText(str(round(self.htr_temperature[-15:].mean(), 2)) + "°C")
        else:
            self.temp_avg_15.setText("N/A")

        if temp_size > 50:
            self.temp_avg_50.setText(str(round(self.htr_temperature[-50:].mean(), 2)) + "°C")
        else:
            self.temp_avg_50.setText("N/A")

    def start_qcm_calibrate(self):
        """
        Start calibration for the QCM sensor
        """
        # Make Data Thread
        self.qcm_thread = QtCore.QThread(self)

        # Create QCM controller
        self.qcm_ctrl = QCMSensorCtrl(port=self.qcm_port)
        self.qcm_ctrl.moveToThread(self.qcm_thread)

        # Reset
        self.calibration_bar.setStyleSheet("")

        # Setup Timer for Testing
        self.qcm_timer = QtCore.QTimer(self)
        self.qcm_timer.timeout.connect(self.calibration_processing)

        # Setup Signals
        self.qcm_thread.started.connect(lambda : self.qcm_ctrl.calibrate(self.qc_type.currentText()))
        self.qcm_thread.started.connect(lambda : self.qcm_timer.start(Constants.plot_update_ms))

        # Start
        self.qcm_thread.start()

        # Message
        self.statusBar().showMessage("Calibrating QCM...")
        
    def calibration_processing(self):
        """
        Process calibration data
        """
        try:
            # Consume
            self.qcm_ctrl.worker.consume_queue1()
            self.qcm_ctrl.worker.consume_queue2()
            self.qcm_ctrl.worker.consume_queue3()
            self.qcm_ctrl.worker.consume_queue4()
            self.qcm_ctrl.worker.consume_queue5()
            
            # general error queue
            self.qcm_ctrl.worker.consume_queue6()

            self.qcm_ctrl.worker.consume_queue_F_multi()
            self.qcm_ctrl.worker.consume_queue_D_multi()
            self.qcm_ctrl.worker.consume_queue_A_multi()
            self.qcm_ctrl.worker.consume_queue_P_multi()

            # flag for terminating calibration
            stop_flag = 0
            success = False

            # vector2[0] and vector3[0] flag error
            vector2 = self.qcm_ctrl.worker.get_t3_buffer()
            vector3 = self.qcm_ctrl.worker.get_d3_buffer()

            labelbar = 'The operation might take just over a minute to complete... please wait...'
            
            # progressbar
            error1, _, _, _ser_control, _ = self.qcm_ctrl.worker.get_ser_error()
            
            if _ser_control < (Constants.calib_sections):
                _completed = (_ser_control/(Constants.calib_sections))*100

            # calibration buffer empty
            if error1== 1 and vector3[0]==1:
                labelbar = 'Calibration Warning: empty buffer! Please, repeat the Calibration after disconnecting/reconnecting Device!'
                stop_flag=1

            # calibration buffer empty and ValueError from the serial port
            elif error1== 1 and vector2[0]==1:
                labelbar = 'Calibration Warning: empty buffer/ValueError! Please, repeat the Calibration after disconnecting/reconnecting Device!'
                stop_flag=1

            # calibration buffer not empty
            elif error1==0:
                labelbar = 'The operation might take just over a minute to complete... please wait...'

                # Success!
                if vector2[0]== 0 and vector3[0]== 0:
                    labelbar = 'Calibration Success for baseline correction!'
                    stop_flag=1
                    success = True
                
                # Error Message
                elif vector2[0]== 1 or vector3[0]== 1:
                    if vector2[0]== 1:
                        labelbar = 'Calibration Warning: ValueError or generic error during signal acquisition. Please, repeat the Calibration'
                        stop_flag=1 ##
                    elif vector3[0]== 1:
                        labelbar = 'Calibration Warning: unable to identify fundamental peak or apply peak detection algorithm. Please, repeat the Calibration!'
                        stop_flag=1 ##
                        
            # progressbar -------------
            self.calibration_bar.setValue(int(_completed + 10))
            self.statusBar().showMessage(f"{labelbar}", 5000)

            # terminate the  calibration (simulate clicked stop)
            if stop_flag == 1:
                self.qcm_timer.stop()
                self.qcm_ctrl.stop()
                self.enable_calibrate()

                # Enable measurement if successful
                if success:
                    self.calibration_bar.setStyleSheet(QPB_COMPLETED_STYLE)
                    self.update_perm_status(_translate("MainWindow", "QCM Ready"))
                    self.enable_measurement()
                    self.qcm_calibrated = True
                else:
                    self.calibration_bar.setStyleSheet(QPB_ERROR_STYLE)
                    self.statusBar().showMessage(_translate("MainWindow", "Calibration failed as the expected fundamental frequency could not be found."))

                # Enable this if success or htr is already on
                if success or self.htr_port is not None:
                    self.enable_export()
                    self.enable_start()

                # Open ports
                self.enable_ports()

                # Stop Thread
                self.stop_sensors()

            # Update Plot
            vector1 = self.qcm_ctrl.worker.get_value1_buffer()
            vector2 = self.qcm_ctrl.worker.get_value2_buffer()

            calibration_readFREQ  = np.arange(len(vector1)) * (Constants.calib_fStep) + Constants.calibration_frequency_start

            self.amp_data.cb_set_data(x=calibration_readFREQ, y=vector1, pen=Constants.plot_colors[0])
            self.phase_data.cb_set_data(x=calibration_readFREQ, y=vector2, pen=Constants.plot_colors[1])
        except AttributeError:
            # Error catch when qcm_ctrl destoryed
            pass

    def start_qcm(self):
        """
        Start measurements for the QCM sensor
        """
        # Make Data Thread
        self.qcm_thread = QtCore.QThread(self)

        # Create QCM controller
        self.qcm_ctrl = QCMSensorCtrl(port=self.qcm_port)
        self.qcm_ctrl.moveToThread(self.qcm_thread)

        # Setup Timer for Testing
        self.qcm_timer = QtCore.QTimer(self)

        # Setup Signals
        # Single
        if self.measure_type.currentIndex() == 0:
            # Clear Plots if needed
            if self.multi_mode:
                self.clear_qcm_plots_multi()
            self.qcm_timer.timeout.connect(self.single_processing)
            self.qcm_thread.started.connect(lambda : self.qcm_ctrl.single(self.peaks[self.freq_list.currentIndex()]))

            # Set the Data Saver
            if self.data_saver is not None:
                self.data_saver.set_freqs([self.peaks[self.freq_list.currentIndex()], ])
        # Multi
        elif self.measure_type.currentIndex() == 1:
            self.setup_qcm_plots_multi()
            self.qcm_timer.timeout.connect(self.multi_processing)
            self.qcm_thread.started.connect(lambda : self.qcm_ctrl.multi())

            # Set the Data Saver
            if self.data_saver is not None:
                self.data_saver.set_freqs(self.peaks)

        # Start Timer
        self.qcm_thread.started.connect(lambda : self.qcm_timer.start(Constants.plot_update_ms))

        # Save Data Signals if needed
        if self.auto_export:
            self.qcm_ctrl.progress.connect(self.update_qcm_time)
            self.qcm_ctrl.frequency.connect(self.frequency_processing)
            self.qcm_ctrl.dissipation.connect(self.dissipation_processing)
            self.qcm_ctrl.temperature.connect(self.qcm_temperature_processing)

        # Start
        self.qcm_thread.start()

        # Message
        self.statusBar().showMessage("Start measuring QCM...", 5000)
        
    def single_processing(self):
        """
        Process calibration data
        """
        # Consume
        self.qcm_ctrl.worker.consume_queue1()
        self.qcm_ctrl.worker.consume_queue2()
        self.qcm_ctrl.worker.consume_queue3()
        self.qcm_ctrl.worker.consume_queue4()
        # TODO note that data is logged here, when self.qcm_ctrl.worker.consume_queue5() is called
        self.qcm_ctrl.worker.consume_queue5()
        # general error queue
        self.qcm_ctrl.worker.consume_queue6()
        
        _ser_error1, _ser_error2, _ser_control, _, _ = self.qcm_ctrl.worker.get_ser_error()

        vector1 = self.qcm_ctrl.worker.get_d1_buffer()
        vector2 = self.qcm_ctrl.worker.get_d2_buffer()

        # Early Process
        prep_process = False
        
        if vector1.any():
            # progressbar
            if _ser_control<=Constants.environment:
                self.qcm_progress = _ser_control*2
                prep_process = True

            if str(vector1[0])=='nan' and not _ser_error1 and not _ser_error2:
                labelbar = 'Please wait, processing early data...'

                # Status
                self.update_perm_status(_translate("MainWindow", "Environment Reading..."))

            elif (str(vector1[0])=='nan' and (_ser_error1 or _ser_error2)):
                if _ser_error1 and _ser_error2:
                    labelbar = 'Warning: unable to apply half-power bandwidth method, lower and upper cut-off frequency not found'
                elif _ser_error1:
                    labelbar = 'Warning: unable to apply half-power bandwidth method, lower cut-off frequency (left side) not found'
                elif _ser_error2:
                    labelbar = 'Warning: unable to apply half-power bandwidth method, upper cut-off frequency (right side) not found'
    
                # Update QPB Style
                self.progress_bar.setStyleSheet(QPB_ERROR_STYLE)
            else:
                if not _ser_error1 and not _ser_error2:
                    labelbar = 'Monitoring!'
        
                    # Update QPB Style
                    self.progress_bar.setStyleSheet(QPB_COMPLETED_STYLE)

                    # Status
                    self.update_perm_status(_translate("MainWindow", labelbar))
                else:
                    if _ser_error1 and _ser_error2:
                        labelbar = 'Warning: unable to apply half-power bandwidth method, lower and upper cut-off frequency not found'
                    elif _ser_error1:
                        labelbar = 'Warning: unable to apply half-power bandwidth method, lower cut-off frequency (left side) not found'
                    elif _ser_error2:
                        labelbar = 'Warning: unable to apply half-power bandwidth method, upper cut-off frequency (right side) not found'
    
                    # Update QPB Style
                    self.progress_bar.setStyleSheet(QPB_ERROR_STYLE)
                    
        # progressbar 
        self.progress_bar.setValue(int(self.qcm_progress + 2))

        # Message
        self.statusBar().showMessage(labelbar, 5000)

        # Update Plot
        amp = self.qcm_ctrl.worker.get_value1_buffer()
        phase = self.qcm_ctrl.worker.get_value2_buffer()

        readFreq = self.qcm_ctrl.worker.get_frequency_range()

        self.amp_data.cb_set_data(x=readFreq, y=amp, pen=Constants.plot_colors[0])
        self.phase_data.cb_set_data(x=readFreq, y=phase, pen=Constants.plot_colors[1])

        # Continue to wait until process is done
        if prep_process:
            return

        # Freq Plot
        vector1 = np.array(vector1) - self.qcm_ctrl.reference_value_frequency
        self.freq_data.cb_set_data(x=self.qcm_ctrl.worker.get_t1_buffer(), y=vector1, pen=Constants.plot_colors[6])

        # Dissipationi Plot
        vector2 = np.array(vector2) - self.qcm_ctrl.reference_value_dissipation
        self.dissipate_data.cb_set_data(x=self.qcm_ctrl.worker.get_t2_buffer(), y=vector2, pen=Constants.plot_colors[7])

        # Update indicators
        for i in range(5):
            self.update_indicator_freq(i, None if self.freq_list.currentIndex() != i else vector1[0])
            self.update_indicator_dissipation(i, None if self.freq_list.currentIndex() != i else vector2[0] * 1e6)
        
    def multi_processing(self):
        """
        Process calibration data
        """
        # Consume
        self.qcm_ctrl.worker.consume_queue1()
        self.qcm_ctrl.worker.consume_queue2()
        self.qcm_ctrl.worker.consume_queue3()
        self.qcm_ctrl.worker.consume_queue4()
        # TODO note that data is logged here, when self.qcm_ctrl.worker.consume_queue5() is called
        self.qcm_ctrl.worker.consume_queue5()
        # general error queue
        self.qcm_ctrl.worker.consume_queue6()

        self.qcm_ctrl.worker.consume_queue_F_multi()
        self.qcm_ctrl.worker.consume_queue_D_multi()
        self.qcm_ctrl.worker.consume_queue_A_multi()
        self.qcm_ctrl.worker.consume_queue_P_multi()

        # Early Process
        prep_process = False

        # Data
        vector1 = self.qcm_ctrl.worker.get_d1_buffer()

        # TODO update plot
        self._ser_error1, self._ser_error2, self._ser_control, self._ser_err_usb, self._overtone_number = self.qcm_ctrl.worker.get_ser_error()

        if vector1.any():
            # progressbar
            if self._ser_control <= Constants.environment:
                prep_process = True

                # VER 0.1.2 just a little thing  
                self._completed = self._ser_control * 100 / Constants.environment
                
                # VER 0.1.2
                # Optimize and update infobar and infostatus in multiscan mode
                labelbar = 'Please wait, processing early data...'

                # Status
                self.update_perm_status(_translate("MainWindow", "Environment Reading..."))

            else:
                # Continue to monitor
                labelbar = "Monitoring!"
        
                # Update QPB Style
                self.progress_bar.setStyleSheet(QPB_COMPLETED_STYLE)

                # Status
                self.update_perm_status(_translate("MainWindow", labelbar))
                    
        # progressbar -------------
        self.progress_bar.setValue(int(self._completed + 2))

        # Message
        self.statusBar().showMessage(labelbar, 5000)

        # Continue to wait until process is done
        if prep_process:
            return
        
        # Update Plot
        for idx in range(self.peaks.size):
            # AMPLITUDE
            # get and scale frequency axis
            x_sweep_axis = self.qcm_ctrl.worker.get_F_Sweep_values_buffer(idx) - self.peaks[idx]
            # get amplitude axis
            y_sweep_axis_amp = self.qcm_ctrl.worker.get_A_values_buffer(idx)
            y_sweep_axis_phase = self.qcm_ctrl.worker.get_P_values_buffer(idx)
            # plot sweep
            if isinstance(x_sweep_axis, np.ndarray):
                self.multi_amp_datas[idx].cb_set_data( x = x_sweep_axis, y = y_sweep_axis_amp, pen = Constants.plot_color_multi[idx], name = Constants.name_legend[idx] )
                self.multi_phase_datas[idx].cb_set_data( x = x_sweep_axis, y = y_sweep_axis_phase, pen = Constants.plot_color_multi[idx], name = Constants.name_legend[idx] )

            # FREQ & DISSIPATE
            # get time axis
            time_axis_new = self.qcm_ctrl.worker.get_time_values_buffer(idx)
            
            # get y frequency and dissipation axis
            y_freq = np.array( self.qcm_ctrl.worker.get_F_values_buffer(idx) )
            y_diss = np.array( self.qcm_ctrl.worker.get_D_values_buffer(idx) )

            # plot frequency and dissipation data
            self.multi_freq_datas[idx].cb_set_data(x = time_axis_new, y = y_freq, pen = Constants.plot_color_multi[idx], name = Constants.name_legend[idx] )
            self.multi_dissipate_datas[idx].cb_set_data(x = time_axis_new, y = y_diss, pen = Constants.plot_color_multi[idx], name = Constants.name_legend[idx] )

            # Update Indicators
            self.update_indicator_freq(idx, y_freq[0])
            self.update_indicator_dissipation(idx, y_diss[0] * 1e6)

        # Hide additional indicators if needed
        for i in range(self.peaks.size, 5):
            self.update_indicator_freq(i, "")
            self.update_indicator_dissipation(i, "")

    def update_indicator_freq(self, index : int, value : Union[float, None]):
        """
        Update the indicator fields for frequencies
        """
        if type(value) == str:
            label = value
        elif value is not None:
            label = round(value, 2)
        else:
            label = "N/A"

        if (index == 0):
            self.freq_f1.setText(str(label))
        elif (index == 1):
            self.freq_f3.setText(str(label))
        elif (index == 2):
            self.freq_f5.setText(str(label))
        elif (index == 3):
            self.freq_f7.setText(str(label))
        elif (index == 4):
            self.freq_f9.setText(str(label))

    def update_indicator_dissipation(self, index : int, value : Union[float, None]):
        """
        Update the indicator fields for dissipation
        """
        if type(value) == str:
            label = value
        elif value is not None:
            label = round(value, 2)
        else:
            label = "N/A"

        if (index == 0):
            self.diss_d1.setText(str(label))
        elif (index == 1):
            self.diss_d3.setText(str(label))
        elif (index == 2):
            self.diss_d5.setText(str(label))
        elif (index == 3):
            self.diss_d7.setText(str(label))
        elif (index == 4):
            self.diss_d9.setText(str(label))

    def update_qcm_time(self):
        """
        Update the time array for qcm
        """
        temp_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.qcm_time = np.append(self.qcm_time, temp_time)

        # Queue for data saving if needed
        if self.data_saver is not None:
            self.data_saver.qcm_time.put(temp_time)


    def frequency_processing(self, data : float, idx : int=0):
        """
        Processes the frequency values from qcm
        """
        self.frequency = np.append(self.frequency, data)

        # Queue for data saving if needed
        if self.data_saver is not None:
            self.data_saver.qcm_freq[idx].put(data)

    def dissipation_processing(self, data : float, idx : int=0):
        """
        Processes the dissipation values from qcm
        """
        self.dissipation = np.append(self.dissipation, data)

        # Queue for data saving if needed
        if self.data_saver is not None:
            self.data_saver.qcm_diss[idx].put(data)

    def qcm_temperature_processing(self, data : float):
        """
        Processes the temperature values from qcm
        """
        self.qcm_temperature = np.append(self.qcm_temperature, data)

        # Queue for data saving if needed
        if self.data_saver is not None:
            self.data_saver.qcm_temp.put(data)

    def clear_plots(self):
        """
        Clear the graphs
        """
        # Set Override Plot
        self.resist_data.cb_set_data([0,], [0,])
        self.humd_data.cb_set_data([0,], [0,])
        self.temp_data.cb_set_data([0,], [0,])

        # Override other plots with empty data
        self.amp_data.cb_set_data([0,], [0,])
        self.phase_data.cb_set_data([0,], [0,])
        self.freq_data.cb_set_data([0,], [0,])
        self.dissipate_data.cb_set_data([0,], [0,])

        # If Multi, also clear
        for i in range(len(self.multi_amp_datas)):
            self.multi_amp_datas[i].cb_set_data([0,], [0,])
            self.multi_freq_datas[i].cb_set_data([0,], [0,])
            self.multi_dissipate_datas[i].cb_set_data([0,], [0,])

    def clear_data(self):
        """
        Clear the graphs
        """
        # Clear Data
        self.raw_resistance = np.array([])
        self.resistance = np.array([])
        self.humidity = np.array([])
        self.htr_temperature = np.array([])
        self.resistance_time = np.array([])
        self.humidity_time = np.array([])
        self.htr_temperature_time = np.array([])
        self.htr_time = np.array([])
        self.r_time = np.array([])

        # Clear Progress
        self.progress_bar.setValue(0)

        # Clear Data Values
        self.resist_avg.clear()
        self.avg_resist_15.clear()
        self.avg_resist_50.clear()
        self.humd_avg.clear()
        self.humd_avg_15.clear()
        self.humd_avg_50.clear()
        self.temp_avg.clear()
        self.temp_avg_15.clear()
        self.temp_avg_50.clear()

        # Clear Indicators
        for i in range(5):
            self.update_indicator_freq(i, "")
            self.update_indicator_dissipation(i, "")

    def start_data_saving(self):
        """
        Starts the data saving process
        """
        # Setup
        self.data_saving_thread = QtCore.QThread(self)
        self.data_saving_timer = QtCore.QTimer(self)

        # Connect Signals
        self.data_saving_timer.timeout.connect(self.data_saver.write)
        self.data_saving_thread.started.connect(lambda : self.data_saving_timer.start(Constants.data_timeout_ms))

        # Start File Writing
        self.data_saver.open()

        # Start
        self.data_saving_thread.start()

    def stop_sensors(self):
        """
        Stops all the processes in process
        """
        # Close HTR stuff
        if self.htr_ctrl is not None:
            self.htr_ctrl.stop()
            self.htr_ctrl = None
        if self.htr_thread is not None:
            self.htr_thread.quit()
            self.htr_thread = None

        # Close QCM stuff
        if self.qcm_ctrl is not None:
            self.qcm_ctrl.stop()
            self.qcm_ctrl = None
            if self.qcm_timer is not None:
                self.qcm_timer.stop()
                self.qcm_timer.deleteLater()
                self.qcm_timer = None
        if self.qcm_thread is not None:
            self.qcm_thread.quit()
            self.qcm_thread = None

        # Close R stuff
        if self.r_ctrl is not None:
            self.r_ctrl.stop()
            self.r_ctrl = None
        if self.r_thread is not None:
            self.r_thread.quit()
            self.r_thread = None

        # Stop Data Saving
        if self.data_saving_thread is not None:
            self.data_saving_timer.stop()
            self.data_saving_thread.quit()
            self.data_saving_timer.deleteLater()
            self.data_saving_timer = None
            self.data_saving_thread = None
            self.data_saver.close()
            self.data_saver = None
    
    # Slots
    @QtCore.pyqtSlot()
    def on_action_Refresh_Ports_triggered(self):
        self.update_ports()

    @QtCore.pyqtSlot()
    def on_action_Scan_Connections_triggered(self):
        self.look_for_daq()

        # Unlock stuff if connected
        if self.r_device is not None:
            self.action_Disconnect.setEnabled(True)
            self.enable_daq_indicator()
            self.daq_status.setPixmap(QPixmap(":/main/check.png"))
            self.daq_device.setText(self.r_device)
            self.enable_export()
            self.enable_start()

            self.update_perm_status(_translate("MainWindow", "R Ready"))

    @QtCore.pyqtSlot()
    def on_action_Disconnect_triggered(self):
        # Ask for confirmation before disconnecting
        confirmation = QMessageBox.question(self, _translate("MainWindow", "Confirmation"), _translate("MainWindow", "Are you sure you want to disconnect the DAQ? The HTR's resistor sensor will be re-enabled."), QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.No:
            # ignore
            return
        
        # Disable and remove
        self.action_Disconnect.setEnabled(False)
        self.disable_daq_indicator()
        self.r_device = None

        # Disable stuff if needed
        if self.htr_port is None and (self.qcm_port is None or not self.qcm_calibrated):
            self.disable_all_ctrls()
            self.reset_progress_bar()
            self.enable_ports()

            self.update_perm_status(_translate("MainWindow", "Not Ready"))

    @QtCore.pyqtSlot()
    def on_action_Quit_triggered(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_action_Resistor_triggered(self):
        # Prompt user for new voltage
        raw_resist = QInputDialog.getText(self, _translate("MainWindow", "Reference Resistor"), _translate("MainWindow", "Enter the new reference resistance from the controller with SI multipler."), text=f"{float(SETTINGS.get_setting('ref_resist'))}{SETTINGS.get_setting('ref_resist_unit')}")

        # Update
        if raw_resist[1]:
            # Parse string
            resist = re.search(REF_RESIST_PARSE, raw_resist[0])

            # Fail if not found
            if resist is None or len(resist.groups()) < 3:
                self.statusBar().showMessage(f"Reference resistance could not be updated, formatting is not correct. Must be (\\d+(\\.\\d+)?)([a-zA-Z ])", 5000)
                return

            SETTINGS.update_setting("ref_resist", resist.group(1))
            SETTINGS.update_setting("ref_resist_unit", resist.group(3))

            self.statusBar().showMessage(f"Reference resistance updated to {resist.group(1)} {resist.group(3)}Ω", 5000)

            # Update R Sensor if needed
            if self.r_ctrl is not None:
                self.r_ctrl.set_ref_resist(float(resist.group(1)))
            elif self.htr_ctrl is not None:
                self.htr_ctrl.update_ref_resist(float(resist.group(1)))

    @QtCore.pyqtSlot()
    def on_action_Voltage_triggered(self):
        # Prompt user for new voltage
        volt = QInputDialog.getDouble(self, _translate("MainWindow", "Reference Voltage"), _translate("MainWindow", "Enter the new reference voltage from the controller."), float(SETTINGS.get_setting("ref_volt")), 0.0, decimals=4)

        # Update
        if volt[1]:
            SETTINGS.update_setting("ref_volt", str(volt[0]))
            self.statusBar().showMessage(f"Reference voltage updated to {volt[0]}V", 5000)

            # Update R Sensor if needed
            if self.r_ctrl is not None:
                self.r_ctrl.set_voltage(volt[0])
            elif self.htr_ctrl is not None:
                self.htr_ctrl.update_ref_volt(volt[0])

    @QtCore.pyqtSlot()
    def on_action_Noise_Reduction_triggered(self):
        # Prompt user for new voltage
        noise = QInputDialog.getInt(self, _translate("MainWindow", "Noise Reduction"), _translate("MainWindow", "Enter the number of times to apply the noise filter."), self.noise_reduce, 1)

        # Update
        if noise[1]:
            SETTINGS.update_setting("noise_reduce", str(noise[0]))
            self.noise_reduce = noise[0]
            self.statusBar().showMessage(f"Noise reduction filter will now iterate {noise[0]} times", 5000)

    @QtCore.pyqtSlot()
    def on_action_Reset_Software_triggered(self):
        # Ask for confirmation before resetting
        confirmation = QMessageBox.question(self, _translate("MainWindow", "Confirmation"), _translate("MainWindow", "Are you sure you want to reset everything? All data not saved will be lost."), QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.No:
            # ignore
            return

        # Disable All
        self.disable_all_ctrls()
        self.reset_calibration_bar()
        self.reset_progress_bar()

        # Setup Graphs
        self.setup_plots()

        # Setup Variables
        self.setup_variable()

        # Setup Signals
        self.setup_signals()

        # Enable Ports
        self.update_ports()
        self.enable_ports()

        # Startup Memory Stuff
        self.setup_memory()

    @QtCore.pyqtSlot(int)
    def on_htr_serial_currentIndexChanged(self, _ : int):
        if self.htr_serial.currentText() != self.htr_port:
            self.htr_status.setPixmap(QPixmap(":/main/mark.png"))
        else:
            self.htr_status.setPixmap(QPixmap(":/main/check.png"))

    @QtCore.pyqtSlot(int)
    def on_qcm_serial_currentIndexChanged(self, _ : int):
        if self.qcm_serial.currentText() != self.qcm_port:
            self.qcm_status.setPixmap(QPixmap(":/main/mark.png"))
        else:
            self.qcm_status.setPixmap(QPixmap(":/main/check.png"))

    @QtCore.pyqtSlot()
    def on_connect_btn_clicked(self):
        # Ensure something is selected
        if self.htr_serial.currentIndex() == -1 or self.qcm_serial.currentIndex() == -1:
            self.statusBar().showMessage("Nothing to connect to...", 5000)
            return
        
        running = False
        
        # Test HTR (Ignore if ---)
        if self.htr_serial.currentIndex() != 0 and self.htr_port != self.htr_serial.currentText():
            running = True
            self.test_htr_port()
                
        # Test QCM (Ignore if ---)
        if self.qcm_serial.currentIndex() != 0 and self.qcm_port != self.qcm_serial.currentText():
            running = True
            self.test_qcm_port()

        # If nothing is running, do nothing
        if not running:
            return
        
        # Signal Launch
        self.statusBar().showMessage("Attempting to communicate with the sensors...", 5000)

        # Disable
        self.disable_all_ctrls()
        self.reset_calibration_bar()
        self.reset_progress_bar()

    @QtCore.pyqtSlot()
    def on_calibrate_btn_clicked(self):
        # Disable
        self.disable_all_ctrls()
        self.reset_calibration_bar()
        self.qcm_calibrated = False

        # Start
        self.start_qcm_calibrate()

        # Save QC Selection
        SETTINGS.update_setting("last_qc_chip", self.qc_type.currentText())

    @QtCore.pyqtSlot()
    def on_auto_export_clicked(self):
        # If Check and Empty, set default
        if self.auto_export.isChecked() and self.file_dest.text().strip() == "":
            self.file_dest.setText(f"{DATA_FOLDER}/data-{int(time.time())}.csv")
        elif not self.auto_export.isChecked() and self.file_dest.text().startswith(f"{DATA_FOLDER}/data-"):
            self.file_dest.clear()

    @QtCore.pyqtSlot()
    def on_file_select_clicked(self):
        # Get File
        self.file_dialog = QFileDialog.getSaveFileName(self, _translate("MainWindow", 'Exportation'), f"{DATA_FOLDER}/", _translate("MainWindow", "CSV (*.csv)"))

        # Save
        self.file_dest.setText(self.file_dialog[0])

    @QtCore.pyqtSlot()
    def on_start_btn_clicked(self):
        # Warn if saving is off
        if not self.auto_export.isChecked():
            confirmation = QMessageBox.question(self, _translate("MainWindow", "Warning: Saving Disabled"), _translate("MainWindow", "Are you sure you want to start without saving any data?"), QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.No:
                return
            
        # Warn if QCM is not connected
        if self.qcm_port is None:
            confirmation = QMessageBox.question(self, _translate("MainWindow", "Warning: Missing QCM Sensor"), _translate("MainWindow", f"You are missing the QCM sensor! Are you sure you want to start without it?"), QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.No:
                return
            
        # Warn if HTR is not connected
        if self.htr_port is None:
            confirmation = QMessageBox.question(self, _translate("MainWindow", "Warning: Missing HTR Sensor"), _translate("MainWindow", f"You are missing the HTR sensor! Are you sure you want to start without it?"), QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.No:
                return
            
        # Warn if not calibrated
        if self.qcm_port is not None and not self.qcm_calibrated:
            confirmation = QMessageBox.question(self, _translate("MainWindow", "Warning: No Calibration"), _translate("MainWindow", "You have not calibrated the QCM sensor. It will not start without it. Are you sure you want to start without it?"), QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.No:
                return

        # Disable
        self.disable_all_ctrls()
        self.reset_progress_bar()

        # Save selection
        SETTINGS.update_setting("measurement_mode", f"{self.measure_type.currentIndex()}")
        SETTINGS.update_setting("freq_select", f"{self.freq_list.currentIndex()}")
        SETTINGS.update_setting("auto_export", f"{self.auto_export.isChecked()}")
        if self.file_dest.text() != "" and not self.file_dest.text().startswith(f"{DATA_FOLDER}/data-"):
            SETTINGS.update_setting("last_file_dest", self.file_dest.text())
        else:
            SETTINGS.update_setting("last_file_dest", " ")
        
        # Clear
        self.clear_plots()
        self.clear_data()

        # Enable buttons
        self.stop_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)

        # Update save status
        if self.auto_export.isChecked():
            self.data_saver = DataSaving(file_name=self.file_dest.text())

        # Start HTR
        if self.htr_port is not None:
            self.start_htr()
        elif self.auto_export.isChecked():
            self.data_saver.set_htr(False)

        # Start R
        if self.r_device is not None:
            self.start_r()
        elif self.auto_export.isChecked():
            self.data_saver.set_r(False)

        # Start QCM
        if self.qcm_port is not None and self.qcm_calibrated:
            self.start_qcm()
        elif self.auto_export.isChecked():
            self.data_saver.set_qcm(False)

        # Data Saving Thread
        if self.auto_export.isChecked():
            self.start_data_saving()

    @QtCore.pyqtSlot()
    def on_stop_btn_clicked(self):
        # Disable button
        self.stop_btn.setEnabled(False)

        # Stop Sensors
        self.stop_sensors()

        # Enable button
        self.start_btn.setEnabled(True)

        # Update Status
        self.update_perm_status("Monitoring Stopped; Ready")

    @QtCore.pyqtSlot()
    def on_reset_btn_clicked(self):
        # Disable button
        self.reset_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.clear_plots()
        self.clear_data()
        self.stop_sensors()

        # Enable stuff
        self.enable_measurement()
        self.enable_export()
        self.enable_start()

        # Update Status
        self.update_perm_status("Reset Configuration; Ready")

    # Events
    def closeEvent(self, a0: QCloseEvent) -> None:
        # Ask for confirmation before closing
        confirmation = QMessageBox.question(self, _translate("MainWindow", "Confirmation"), _translate("MainWindow", "Are you sure you want to close the application?"), QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            # Close Controllers
            self.stop_sensors()

            # Close
            a0.accept()
        else:
            a0.ignore() 
            
