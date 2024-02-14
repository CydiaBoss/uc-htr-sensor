import sys, ctypes

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPixmap, QCloseEvent
from PyQt5 import QtCore
from controller import HTRSensorCtrl, HTRTester, QCMSensorCtrl, QCMTester

from main_gui import Ui_MainWindow
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

    # Signal
    connected = QtCore.pyqtSignal()

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

        # Setup Ports
        self.htr_port : str = None
        self.qcm_port : str = None

        # Setup Dropdowns
        self.ports = []
        self.update_ports()

        # Setup Signals
        self.setup_signals()

        # Setup Controllers
        self.htr_ctrl : HTRSensorCtrl = None
        self.qcm_ctrl : QCMSensorCtrl = None

        # Enable Ports
        self.enable_ports()

    def setup_plots(self):
        '''
        Setups the graphs for live data collectrion
        '''
        # Setup Resistance Graph
        self.htr_layout.removeWidget(self.resist_plot)
        self.resist_plot.setParent(None)
        self.resist_plot.deleteLater()
        self.resist_axis = LiveAxis('left', text=_translate("MainWindow", "Resistance"), units="Ohm", unitPrefix=REF_RESIST_UNIT.strip())
        self.resist_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Resistance"), axisItems={"left": self.resist_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Resistance") + f" ({REF_RESIST_UNIT}Ohm)", "bottom": _translate("MainWindow", "Time") + " (s)"})
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
        self.humd_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Humidity"), axisItems={"left": self.humd_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Humidity") + " (%RH)", "bottom": _translate("MainWindow", "Time") + " (s)"})
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
        self.temp_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Temperature"), axisItems={"left": self.temp_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Temperature") + " (degC)", "bottom": _translate("MainWindow", "Time") + " (s)"})
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
        self.freq_plot = LivePlotWidget(self.layoutWidget1, title=_translate("MainWindow", "Real-time Frequency"), axisItems={"left": self.freq_axis, "bottom": LiveAxis(**TIME_AXIS_CONFIG)}, labels={"left": _translate("MainWindow", "Frequency") + " (dB)", "bottom": _translate("MainWindow", "Time") + " (s)"})
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

    def setup_signals(self):
        """
        Setup all essential connections
        """
        # Connection signal
        self.connected.connect(self.is_connected)

    def disable_all_ctrls(self):
        """
        Disable all controls
        """
        # Ports
        self.htr_serial.setEnabled(False)
        self.qcm_serial.setEnabled(False)
        self.connect_btn.setEnabled(False)

        # Calibration
        self.qc_type.setEnabled(False)
        self.calibrate_btn.setEnabled(False)
        self.calibration_bar.setValue(0)
        
        # Measurement
        self.measure_type.setEnabled(False)
        self.freq_list.setEnabled(False)
        self.qcm_temp_ctrl.setChecked(False)
        self.qcm_temp_ctrl.setEnabled(False)

        # Exportation
        self.auto_export.setChecked(False)
        self.auto_export.setEnabled(False)
        self.file_dest.setEnabled(False)
        self.file_select.setEnabled(False)

        # Start
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.reset_btn.setEnabled(False)
        self.progress_bar.setValue(0)

    def enable_ports(self):
        """
        Enable all port ctrls
        """
        self.htr_serial.setEnabled(True)
        self.qcm_serial.setEnabled(True)
        self.connect_btn.setEnabled(True)

    def enable_calibrate(self):
        """
        Enable all calibration ctrls
        """
        self.qc_type.setEnabled(True)
        self.calibrate_btn.setEnabled(True)

    def enable_measurement(self):
        """
        Enable all measurement ctrls
        """
        self.measure_type.setEnabled(True)
        self.freq_list.setEnabled(True)
        # self.qcm_temp_ctrl.setEnabled(True)

    def enable_export(self):
        """
        Enable all export ctrls
        """
        self.auto_export.setEnabled(True)

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
            self.statusBar().showMessage("No New Ports Discovered")
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

        # Update
        self.statusBar().showMessage("New Ports Discovered")

    def test_htr_port(self):
        '''
        Test the HTR port for success
        '''
        # Reset Port String
        self.htr_port = None

        # Prepare QThread
        self.htr_thread = QtCore.QThread()

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
            self.statusBar().showMessage(f"Port {self.htr_serial.currentText()} is not the HTR")
        else:
            self.htr_status.setPixmap(QPixmap(":/main/check.png"))
            self.statusBar().showMessage(f"Port {self.htr_serial.currentText()} is the HTR")
            self.htr_port = self.htr_serial.currentText()
            self.connected.emit()

        # Unlock
        if self.qcm_serial.isEnabled():
            self.connect_btn.setEnabled(True)
        self.htr_serial.setEnabled(True)

    def test_qcm_port(self):
        '''
        Test the QCM port for success
        '''
        # Reset QCM port
        self.qcm_port = None

        # Prepare QThread
        self.qcm_thread = QtCore.QThread()

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
            self.statusBar().showMessage(f"Port {self.qcm_serial.currentText()} is not the QCM")
        else:
            self.qcm_status.setPixmap(QPixmap(":/main/check.png"))
            self.statusBar().showMessage(f"Port {self.qcm_serial.currentText()} is the QCM")
            self.qcm_port = self.qcm_serial.currentText()
            self.connected.emit()

        # Unlock
        if self.htr_serial.isEnabled():
            self.connect_btn.setEnabled(True)
        self.qcm_serial.setEnabled(True)

    def is_connected(self) -> bool:
        """
        Checks if the system is connected
        Enables calibration if is
        """
        connect = self.htr_port is not None and self.qcm_port is not None
        if connect:
            self.enable_calibrate()
            self.start_btn.setEnabled(True)

        return connect

    def start_htr(self):
        '''
        Start running HTR sampling
        '''
        # Make Data Thread
        self.htr_thread = QtCore.QThread()
        
        # Create controller
        self.htr_ctrl = HTRSensorCtrl(port=self.htr_port, baud=BAUD, timeout=SENSOR_TIMEOUT)
        self.htr_ctrl.moveToThread(self.htr_thread)

        # Signal/Slots
        self.htr_thread.started.connect(self.htr_ctrl.run)
        self.htr_ctrl.resistance.connect(self.resistance_processing)
        self.htr_ctrl.humidity.connect(self.humidity_processing)
        self.htr_ctrl.temperature.connect(self.temperature_processing)
        self.htr_ctrl.finished.connect(self.htr_thread.quit)
        self.htr_ctrl.finished.connect(self.htr_ctrl.deleteLater)
        self.htr_thread.finished.connect(self.htr_thread.deleteLater)
    
        # Initialize Data Collection
        self.htr_thread.start()

    def resistance_processing(self, time_at : float, r_data : float):
        """
        Processes the resistance data
        """
        self.resist_data.cb_append_data_point(r_data, time_at)
        resistance.append(r_data)

        # Calculate Resist AVGs
        resist_size = len(resistance)

        self.resist_avg.setText(str(round(sum(resistance)/resist_size, 2)) + f" {REF_RESIST_UNIT}Ω")

        if resist_size > 15:
            self.avg_resist_15.setText(str(round(sum(resistance[-15:])/15, 2)) + f" {REF_RESIST_UNIT}Ω")
        else:
            self.avg_resist_15.setText("N/A")

        if resist_size > 50:
            self.avg_resist_50.setText(str(round(sum(resistance[-50:])/50, 2)) + f" {REF_RESIST_UNIT}Ω")
        else:
            self.avg_resist_50.setText("N/A")

    def humidity_processing(self, time_at : float, h_data : float):
        """
        Processes the humidity data
        """
        self.humd_data.cb_append_data_point(h_data, time_at)
        humidity.append(h_data)

        # Calculate Humidity AVGs
        humd_size = len(humidity)
        
        self.humd_avg.setText(str(round(sum(humidity)/humd_size, 2)) + "%RH")

        if humd_size > 15:
            self.humd_avg_15.setText(str(round(sum(humidity[-15:])/15, 2)) + "%RH")
        else:
            self.humd_avg_15.setText("N/A")

        if humd_size > 50:
            self.humd_avg_50.setText(str(round(sum(humidity[-50:])/50, 2)) + "%RH")
        else:
            self.humd_avg_50.setText("N/A")

    def temperature_processing(self, time_at : float, t_data : float):
        """
        Processes the temperature data
        """
        self.temp_data.cb_append_data_point(t_data, time_at)
        temperature.append(t_data)

        # Calculate Temperature AVGs
        temp_size = len(temperature)
        
        self.temp_avg.setText(str(round(sum(temperature)/temp_size, 2)) + "°C")

        if temp_size > 15:
            self.temp_avg_15.setText(str(round(sum(temperature[-15:])/15, 2)) + "°C")
        else:
            self.temp_avg_15.setText("N/A")

        if temp_size > 50:
            self.temp_avg_50.setText(str(round(sum(temperature[-50:])/50, 2)) + "°C")
        else:
            self.temp_avg_50.setText("N/A")

    def start_qcm_calibrate(self):
        """
        Start calibration for the QCM sensor
        """
        # Make Data Thread
        self.qcm_thread = QtCore.QThread()

        # Create QCM controller
        self.qcm_ctrl = QCMSensorCtrl(port=self.qcm_port)
        self.qcm_ctrl.moveToThread(self.qcm_thread)

        # Setup Timer for Testing
        self.qcm_timer = QtCore.QTimer(self)
        self.qcm_timer.moveToThread(self.qcm_thread)
        self.qcm_timer.timeout.connect(self.calibration_processing)

        # Setup Signals
        self.qcm_thread.started.connect(lambda : self.qcm_ctrl.calibrate(self.qc_type.currentText()))
        self.qcm_thread.started.connect(lambda : self.qcm_timer.start(Constants.plot_update_ms))
        self.qcm_ctrl.calibration_finished.connect(self.qcm_thread.quit)
        self.qcm_ctrl.calibration_finished.connect(self.qcm_ctrl.deleteLater)
        self.qcm_thread.finished.connect(self.qcm_thread.deleteLater)

        # Start
        self.qcm_thread.start()
        
    def calibration_processing(self):
        """
        Process calibration data
        """
        # Consume
        self.qcm_ctrl.worker.consume_queue1()
        self.qcm_ctrl.worker.consume_queue2()
        self.qcm_ctrl.worker.consume_queue3()
        self.qcm_ctrl.worker.consume_queue4()
        # TODO note that data is logged here, when self.worker.consume_queue5() is called
        self.qcm_ctrl.worker.consume_queue5()
        # general error queue
        self.qcm_ctrl.worker.consume_queue6()

        self.qcm_ctrl.worker.consume_queue_F_multi()
        self.qcm_ctrl.worker.consume_queue_D_multi()
        self.qcm_ctrl.worker.consume_queue_A_multi()

        # flag for terminating calibration
        stop_flag = 0

        # vector2[0] and vector3[0] flag error
        vector2 = self.qcm_ctrl.worker.get_t3_buffer()
        vector3 = self.qcm_ctrl.worker.get_d3_buffer()

        labelstatus = 'Calibration Processing'
        labelbar = 'The operation might take just over a minute to complete... please wait...'
        
        # progressbar
        error1, _, _, self._ser_control, self._overtone_number = self.qcm_ctrl.worker.get_ser_error()
        
        if self._ser_control < (Constants.calib_sections):
            self._completed = (self._ser_control/(Constants.calib_sections))*100

        # calibration buffer empty
        if error1== 1 and vector3[0]==1:
            labelstatus = 'Calibration Warning'

            labelbar = 'Calibration Warning: empty buffer! Please, repeat the Calibration after disconnecting/reconnecting Device!'
            stop_flag=1

        # calibration buffer empty and ValueError from the serial port
        elif error1== 1 and vector2[0]==1:
            labelstatus = 'Calibration Warning'

            labelbar = 'Calibration Warning: empty buffer/ValueError! Please, repeat the Calibration after disconnecting/reconnecting Device!'
            stop_flag=1

        # calibration buffer not empty
        elif error1==0:
            labelstatus = 'Calibration Processing'
            labelbar = 'The operation might take just over a minute to complete... please wait...'

            # Success!
            if vector2[0]== 0 and vector3[0]== 0:
                labelstatus = 'Calibration Success'
                
                labelbar = 'Calibration Success for baseline correction!'
                stop_flag=1
            
            # Error Message
            elif vector2[0]== 1 or vector3[0]== 1:
                labelstatus = 'Calibration Warning'

                if vector2[0]== 1:
                    labelbar = 'Calibration Warning: ValueError or generic error during signal acquisition. Please, repeat the Calibration'
                    stop_flag=1 ##
                elif vector3[0]== 1:
                    labelbar = 'Calibration Warning: unable to identify fundamental peak or apply peak detection algorithm. Please, repeat the Calibration!'
                    stop_flag=1 ##
                    
        # progressbar -------------
        self.calibration_bar.setValue(int(self._completed + 10))

        # terminate the  calibration (simulate clicked stop)
        if stop_flag == 1:
            self.qcm_timer.stop()
            self.qcm_ctrl.stop()
            self.enable_calibrate()
            self.statusBar().showMessage(f"[{labelstatus}] {labelbar}")

        # Update Plot
        vector1 = self.qcm_ctrl.worker.get_value1_buffer()
        vector2 = self.qcm_ctrl.worker.get_value2_buffer()

        calibration_readFREQ  = np.arange(len(vector1)) * (Constants.calib_fStep) + Constants.calibration_frequency_start

        self.amp_data.cb_set_data(x=calibration_readFREQ, y=vector1, pen=Constants.plot_colors[0])
        self.phase_data.cb_set_data(x=calibration_readFREQ, y=vector2, pen=Constants.plot_colors[1])

    def stop_sensors(self):
        """
        Stops all the processes in process
        """
        # Close Controllers
        if self.htr_ctrl is not None:
            self.htr_ctrl.stop()
        if self.qcm_ctrl is not None:
            self.qcm_ctrl.stop()
    
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
        
        # Signal Launch
        self.statusBar().showMessage("Attempting to communicate with the sensors...")

        # Disable
        self.disable_all_ctrls()
        
        # Test HTR
        self.test_htr_port()
                
        # Test QCM
        self.test_qcm_port()

    @QtCore.pyqtSlot()
    def on_calibrate_btn_clicked(self):
        # Disable
        self.disable_all_ctrls()

        # Start
        self.start_qcm_calibrate()

    @QtCore.pyqtSlot()
    def on_start_btn_clicked(self):
        # Disable button
        self.start_btn.setEnabled(False)

        # Enable buttons
        self.stop_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)

        # Start HTR
        self.start_htr()

        # Start QCM
        # TODO

    @QtCore.pyqtSlot()
    def on_stop_btn_clicked(self):
        # Disable button
        self.stop_btn.setEnabled(False)
        self.stop_sensors()

        # Enable button
        self.start_btn.setEnabled(True)

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