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
        reference_resist: float = 10.0,
    ):
        super().__init__(parent)
        # Record ports
        self.device = device
        self.device_object = None

        # Looper
        self.loop = True

        # Set the resistance reference
        self.ref_resist = reference_resist

        # Task
        self.measure_task = None

    def open(self) -> bool:
        devices = System.local().devices
        # Device not connected
        if self.device not in devices:
            print(self.tag, "R sensor not connected to computer")
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

        # Disable measure channel
        if self.measure_task is not None:
            self.measure_task.stop()
            self.measure_task.close()
            self.measure_task = None

    def run(self):
        # Open connection and test
        self.open()

        # Create measuring task
        self.measure_task = Task("measuring_task")
        self.measure_task.ai_channels.add_ai_voltage_chan(
            self.device_object.ai_physical_chans["ai0"].name, terminal_config=TerminalConfiguration.DIFF, min_val=0
        )
        self.measure_task.ai_channels.add_ai_voltage_chan(
            self.device_object.ai_physical_chans["ai1"].name, terminal_config=TerminalConfiguration.DIFF, min_val=0
        )

        # Start measuring
        self.start_time = time.time()
        while self.loop:
            # Read value
            data = self.measure_task.read()

            # Progress
            self.progress.emit()

            # Bypass if 0 error
            if data[1] - data[0] <= 1e-6:
                # Sleep for a bit
                time.sleep(READ_DELAY)
                continue

            # Calculate resistance
            resist = data[0] * self.ref_resist / (data[1] - data[0])

            # Send signal
            self.resistance.emit(time.time() - self.start_time, resist)

            # Sleep for a bit
            time.sleep(READ_DELAY)

        # Finish signal
        self.finished.emit()

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

        # Resistance
        self.resistance_status = True

    def open(self) -> bool:
        """
        Open connection to HTR
        """
        # Opening Port
        print(self.tag, "Connecting to HTR sensor...")
        self.serial = Serial(port=self.port, baudrate=self.baud, timeout=self.timeout)

        # Wait for Launch Message
        tick_to_timeout = 0
        while "Running" not in self.read_from():
            # Timeout
            if tick_to_timeout > READ_TIMEOUT:
                print(self.tag, "Could not connect to specified port")
                self.serial.close()
                break
            tick_to_timeout += 1
            time.sleep(1)

        if not self.serial.is_open:
            # Success
            print(self.tag, f"HTR sensor connected at port {self.port}!")

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

        # Update Period
        self.update_period(READ_DELAY * 1000)

        # Adjust references
        if self.resistance_status:
            self.update_ref_resist(
                float(SETTINGS.get_setting("ref_resist")), SETTINGS.get_setting("ref_resist_unit")
            )
            self.update_ref_volt(float(SETTINGS.get_setting("ref_volt")))
        # Disable if not
        elif self.toggle_resist_sensor():
            # Run again if returned true the first time
            self.toggle_resist_sensor()

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

    def update_ref_resist(self, resist: float, mult: str):
        """
        Updates the reference resistor on the sensor
        """
        self.send_to(f"r{resist}{mult}")

        # Wait for OK Message
        tick_to_timeout = 0
        while "ok" not in self.read_from():
            # Timeout
            if tick_to_timeout > READ_TIMEOUT:
                print(self.tag, "Reference resistor failed to update")
                break
            tick_to_timeout += 1
            time.sleep(1)

    def update_ref_volt(self, volt: float):
        """
        Updates the reference voltage on the sensor
        """
        self.send_to(f"v{volt}")

        # Wait for OK Message
        tick_to_timeout = 0
        while "ok" not in self.read_from():
            # Timeout
            if tick_to_timeout > READ_TIMEOUT:
                print(self.tag, "Reference voltage failed to update")
                break
            tick_to_timeout += 1
            time.sleep(1)

    def update_period(self, period: int):
        """
        Updates the period on the sensor (ms)
        """
        self.send_to(f"p{period}")

        # Wait for OK Message
        tick_to_timeout = 0
        while "ok" not in self.read_from():
            # Timeout
            if tick_to_timeout > READ_TIMEOUT:
                print(self.tag, "Period failed to update")
                break
            tick_to_timeout += 1
            time.sleep(1)

    def toggle_resist_sensor(self) -> bool:
        """
        Toggles the resistance sensor
        """
        self.send_to("t")

        # Wait for OK Message
        tick_to_timeout = 0
        status = self.read_from()
        while "ok" not in status:
            # Timeout
            if tick_to_timeout > READ_TIMEOUT:
                print(self.tag, "Resistance sensor failed to toggle")
                return
            tick_to_timeout += 1
            time.sleep(1)
            # Update
            status = self.read_from()

        # Toggle
        return "true" in status

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
