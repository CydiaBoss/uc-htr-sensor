import re
import numpy as np
from serial import Serial
from serial.tools import list_ports
import time, atexit

from misc.constants import (
    DATA_PARSE,
    READ_DELAY,
    READ_TIMEOUT,
    SETTINGS,
    Constants,
    SourceType,
    Architecture,
    OSType,
)
from misc.logger import Logger as Log

from openqcm.core.worker import Worker

from PyQt5.QtCore import QObject, pyqtSignal

from nidaqmx import Task
from nidaqmx.constants import TerminalConfiguration
from nidaqmx.system.system import System


class RSensorCtrl(QObject):
    """
    Class of sensor controls for the DAQ R system
    """

    # Signals
    finished = pyqtSignal()
    progress = pyqtSignal()
    resistance = pyqtSignal(float, float)

    # Tag
    tag = "RSensorController"

    def __init__(
        self,
        parent: QObject = None,
        device: str = "",
        voltage: float = 5.0,
        reference_resist: float = 10.0,
    ):
        super().__init__(parent)
        # Record ports
        self.device = device
        self.device_object = None

        # Looper
        self.loop = True

        # Set the voltage supply
        self.volt_supply = voltage

        # Set the resistance reference
        self.ref_resist = reference_resist

        # Task
        self.volt_task = None
        self.measure_task = None

    def open(self) -> bool:
        devices = System.local().devices
        # Device not connected
        if self.device not in devices:
            Log.e(self.tag, "R sensor not connected to computer")
            return False

        # Save
        self.device_object = devices[self.device]

        try:
            # Attempt to self check
            self.device_object.self_test_device()

            # Attempt to self calibrate
            self.device_object.self_cal()

            # Return Success!
            return True
        except:
            return False

    def stop(self):
        # Disable Loop
        self.loop = False

        # Disable voltage channel
        if self.volt_task is not None:
            self.volt_task.write(0.0)
            self.volt_task.stop()
            self.volt_task.close()
            self.volt_task = None

        # Disable measure channel
        if self.measure_task is not None:
            self.measure_task.stop()
            self.measure_task.close()
            self.measure_task = None

    def run(self):
        # Open connection and test
        self.open()

        # Create voltage supply task
        self.set_voltage(self.volt_supply)

        # Create measuring task
        self.measure_task = Task("measuring_task")
        self.measure_task.ai_channels.add_ai_voltage_chan(
            self.device_object.ai_physical_chans["ai0"].name, terminal_config=TerminalConfiguration.DIFF, min_val=0
        )
        self.measure_task.ai_channels.add_ai_voltage_chan(
            self.device_object.ai_physical_chans["ai1"].name, terminal_config=TerminalConfiguration.DIFF, min_val=0
        )

        # Start measuring
        self.volt_task.start()
        self.start_time = time.time()
        while self.loop:
            # Read value
            data = self.measure_task.read()

            # Progress
            self.progress.emit()

            # Calculate resistance
            resist = data[0] * self.ref_resist / (data[1] - data[0])

            # Send signal
            self.resistance.emit(time.time() - self.start_time, resist)

            # Sleep for a bit
            time.sleep(READ_DELAY)

        # Finish signal
        self.finished.emit()

    def set_voltage(self, voltage: float):
        self.volt_supply = voltage

        # Kill old task to replace
        if self.volt_task is not None:
            self.volt_task.stop()
            self.volt_task.close()

        # New Task with updated voltage
        self.volt_task = Task("voltage_supply")
        self.volt_task.ao_channels.add_ao_voltage_chan(
            self.device_object.ao_physical_chans["ao1"].name, min_val=0, max_val=5
        )
        print(self.volt_task.write(self.volt_supply, auto_start=True), "wrote success")

    def set_ref_resist(self, resist: float):
        self.ref_resist = resist


class HTRSensorCtrl(QObject):
    """
    Class of sensor controls for the HTR system
    """

    # Signals
    finished = pyqtSignal()
    progress = pyqtSignal()
    resistance = pyqtSignal(float, float)
    humidity = pyqtSignal(float, float)
    temperature = pyqtSignal(float, float)

    # Tag
    tag = "HTRSensorController"

    def __init__(
        self, parent: QObject = None, port: str = "", baud: int = 9600, timeout=0.1
    ):
        super().__init__(parent)
        # Record ports
        self.port = port
        self.baud = baud
        self.timeout = timeout

        # Loop
        self.loop = False

    def open(self) -> bool:
        """
        Open connection to HTR
        """
        # Opening Port
        Log.i(self.tag, "Connecting to HTR sensor...")
        self.serial = Serial(port=self.port, baudrate=self.baud, timeout=self.timeout)

        # Wait for Launch Message
        tick_to_timeout = 0
        while "Running" not in self.read_from():
            # Timeout
            if tick_to_timeout > READ_TIMEOUT:
                Log.e(self.tag, "Could not connect to specified port")
                self.serial.close()
                break
            tick_to_timeout += 1
            time.sleep(1)

        if not self.serial.is_open:
            # Success
            Log.i(self.tag, f"HTR sensor connected at port {self.port}!")

            # Prep for exit
            atexit.register(self.serial.close)

            return True
        return False

    def stop(self):
        """
        Stop command
        """
        self.loop = False
        if not self.serial.is_open:
            self.serial.close()

    def run(self):
        """
        Runs the data gathering thread
        """
        # Opens the connection
        self.open()

        # Adjust references
        self.update_ref_resist(
            float(SETTINGS.get_setting("ref_resist")), SETTINGS.get_setting("ref_resist_unit")
        )
        self.update_ref_volt(float(SETTINGS.get_setting("ref_volt")))

        # Processing Loop
        self.loop = True
        self.start_time = time.time()
        while self.loop:
            # Read Next Line
            row = self.read_from()

            # Record time
            self.progress.emit()

            # Parse Data row
            data = re.search(DATA_PARSE, row)

            # Update Graph if not None
            if data is not None:
                # Ignore for inf
                if data.group(2) != "inf":
                    r_data = float(data.group(2))

                    # Send signal
                    self.resistance.emit(time.time() - self.start_time, r_data)
                else:
                    self.resistance.emit(time.time() - self.start_time, np.inf)

                h_data = float(data.group(3))
                t_data = float(data.group(4))

                # Send signal
                self.humidity.emit(time.time() - self.start_time, h_data)
                self.temperature.emit(time.time() - self.start_time, t_data)

            # Delay a bit
            time.sleep(READ_DELAY)

        # On break
        self.finished.emit()

    def send_to(self, msg: str):
        """
        Sends a message to the sensor controller
        """
        self.serial.write(msg.encode("utf-8"))

    def update_ref_resist(self, resist: float, mult: str) -> bool:
        """
        Updates the reference resistor on the sensor
        """
        self.send_to(f"r{resist}{mult}")

        # Wait for OK Message
        tick_to_timeout = 0
        while "ok" not in self.read_from():
            # Timeout
            if tick_to_timeout > READ_TIMEOUT:
                Log.e(self.tag, "Reference resistor failed to update")
                break
            tick_to_timeout += 1
            time.sleep(1)

    def update_ref_volt(self, volt: float) -> bool:
        """
        Updates the reference voltage on the sensor
        """
        self.send_to(f"v{volt}")

        # Wait for OK Message
        tick_to_timeout = 0
        while "ok" not in self.read_from():
            # Timeout
            if tick_to_timeout > READ_TIMEOUT:
                Log.e(self.tag, "Reference voltage failed to update")
                break
            tick_to_timeout += 1
            time.sleep(1)

    def read_from(self):
        """
        Read from the sensor
        """
        return self.serial.readline().decode("utf-8")


class HTRTester(QObject):
    finished = pyqtSignal()
    results = pyqtSignal(bool)

    def __init__(self, parent: QObject = None, port="") -> None:
        super().__init__(parent)
        self.port = port

    def run(self):
        """
        Check if the port is part of the HTR system
        """
        try:
            temp_serial = Serial(port=self.port, baudrate=9600, timeout=0.1)

            # Status boolean
            status = True

            # Wait for Launch Message
            tick_to_timeout = 0
            while "Running" not in temp_serial.readline().decode("utf-8"):
                # Timeout
                if tick_to_timeout > READ_TIMEOUT:
                    status = False
                    break
                tick_to_timeout += 1
                time.sleep(1)

            # Close
            temp_serial.close()

            # Confirm Launch
            self.results.emit(status)
        except:
            self.results.emit(False)

        # Signal Completion
        self.finished.emit()


class QCMSensorCtrl(QObject):
    """
    Class of sensor controllers for the QCM system
    """

    # Signals
    progress = pyqtSignal()
    frequency = pyqtSignal(float, int)
    dissipation = pyqtSignal(float, int)
    temperature = pyqtSignal(float)

    # References
    reference_value_frequency = 0
    reference_value_dissipation = 0

    def __init__(self, parent: QObject = None, port: str = "") -> None:
        super().__init__(parent)
        # Set port
        self.port = port
        # Create QCM worker
        self.worker = Worker()

    def stop(self) -> None:
        self.worker.stop()

    def calibrate(self, qc_type: str) -> None:
        """
        Starts the calibration process
        """
        self.worker = Worker(
            QCS_on=None,
            port=self.port,
            speed=qc_type,
            samples=Constants.argument_default_samples,
            source=SourceType.calibration,
            export_enabled=False,
            sampling_time=-1,
        )

        # Start
        self.worker.start()

    def single(self, freq: float) -> None:
        """
        Starts the calibration process
        """
        self.worker = Worker(
            QCS_on=None,
            port=self.port,
            speed=freq,
            samples=Constants.argument_default_samples,
            source=SourceType.serial,
            export_enabled=False,
            sampling_time=-1,
        )

        # Setup Slots for Single
        self.worker.progress.connect(self.progress.emit)
        self.worker.frequency.connect(self.frequency.emit)
        self.worker.dissipation.connect(self.dissipation.emit)
        self.worker.temperature.connect(self.temperature.emit)

        # Start
        self.worker.start()

    def multi(self) -> None:
        """
        Starts the calibration process
        """
        self.worker = Worker(
            QCS_on=None,
            port=self.port,
            samples=Constants.argument_default_samples,
            source=SourceType.multiscan,
            export_enabled=False,
            sampling_time=-1,
        )

        # Setup Slots for Multi
        self.worker.progress.connect(self.progress.emit)
        self.worker.frequency.connect(self.frequency.emit)
        self.worker.dissipation.connect(self.dissipation.emit)
        self.worker.temperature.connect(self.temperature.emit)

        # Start
        self.worker.start()


class QCMTester(QObject):
    finished = pyqtSignal()
    results = pyqtSignal(bool)

    def __init__(self, parent: QObject = None, port="") -> None:
        super().__init__(parent)
        self.port = port

    def run(self):
        """
        Check if the port is part of the HTR system
        """
        try:
            temp_serial = Serial(port=self.port, baudrate=9600, timeout=0.1)

            # Close
            temp_serial.close()

            # Status boolean
            status = False

            # Check Port ID for QCM
            if Architecture.get_os() is OSType.windows:
                com_ports = list_ports.comports()
                for com in com_ports:
                    if com[0] == self.port:
                        status = com[2].startswith("USB VID:PID=16C0:0483")
                        break

            # Confirm Launch
            self.results.emit(status)
        except:
            self.results.emit(False)

        # Signal Completion
        self.finished.emit()
