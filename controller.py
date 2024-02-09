# ================================ #
# Code to communicate with sensors #
# ================================ #
from serial import Serial
from serial.tools import list_ports
import time, atexit

from constants import READ_TIMEOUT
from openqcm.core.worker import Worker
from openqcm.common.architecture import Architecture, OSType
from tools import active_ports

from PyQt5.QtCore import QObject, pyqtSignal

class HTRSensorCtrl:
    '''
    Class of sensor controls for the HTR system
    '''

    def __init__(self, port : str="", baud : int=9600, timeout=0.1):
        # Look for used ports
        self.ports = active_ports()

        # Inactive mode if nothing
        self.connected = True
        if port == "" and len(self.ports) <= 0:
            self.connected = False
            print("No open ports detected.")
            return

        # Open specified port or all detected ports
        if port != "":
            print("Opening port " + port)
            self.sensor = Serial(port=port, baudrate=baud, timeout=timeout)

            # Wait for Launch Message
            tick_to_timeout = 0
            while "Running" not in self.read_from():
                # Timeout
                if tick_to_timeout > READ_TIMEOUT:
                    print("Could not connect to specified port")
                    self.sensor.close()
                    self.connected = False
                    break
                tick_to_timeout += 1
                time.sleep(1)
        else:
            for p in self.ports:
                print("Opening port " + p)
                self.sensor = Serial(port=p, baudrate=baud, timeout=timeout)

                # Wait for Launch Message
                tick_to_timeout = 0
                while "Running" not in self.read_from():
                    # Timeout
                    if tick_to_timeout > READ_TIMEOUT:
                        print(f"Could not connect to port {p}")
                        self.sensor.close()
                        break
                    tick_to_timeout += 1
                    time.sleep(1)

                # Connect Check
                if tick_to_timeout > READ_TIMEOUT:
                    self.connected = False
                else:
                    self.connected = True
                    break

        if self.connected:
            # Success
            print(f"Sensors connected at port {self.sensor.port}!")

            # Prep for exit
            atexit.register(self.sensor.close)

    def send_to(self, msg : str):
        '''
        Sends a message to the sensor controller
        '''
        self.sensor.write(msg.encode('utf-8'))

    def update_ref_resist(self, resist : float, mult : str) -> bool:
        '''
        Updates the reference resistor on the sensor
        '''
        self.send_to(f'r{resist}{mult}')

        # Wait for OK Message
        tick_to_timeout = 0
        while "ok" not in self.read_from():
            # Timeout
            if tick_to_timeout > READ_TIMEOUT:
                print("Reference resistor failed to update")
                break
            tick_to_timeout += 1
            time.sleep(1)

    def update_ref_volt(self, volt : float) -> bool:
        '''
        Updates the reference voltage on the sensor
        '''
        self.send_to(f'v{volt}')

        # Wait for OK Message
        tick_to_timeout = 0
        while "ok" not in self.read_from():
            # Timeout
            if tick_to_timeout > READ_TIMEOUT:
                print("Reference voltage failed to update")
                break
            tick_to_timeout += 1
            time.sleep(1)

    def read_from(self):
        '''
        Read from the sensor
        '''
        return self.sensor.readline().decode("utf-8")
        
class HTRTester(QObject):
    finished = pyqtSignal()
    results = pyqtSignal(bool)

    def __init__(self, parent: QObject=None, port="") -> None:
        super().__init__(parent)
        self.port = port

    def run(self):
        '''
        Check if the port is part of the HTR system
        '''
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

class QCMSensorCtrl:
    '''
    Class of sensor controllers for the QCM system
    '''

    def __init__(self) -> None:
        # Create QCM worker
        self.worker = Worker()


        
class QCMTester(QObject):
    finished = pyqtSignal()
    results = pyqtSignal(bool)

    def __init__(self, parent: QObject=None, port="") -> None:
        super().__init__(parent)
        self.port = port

    def run(self):
        '''
        Check if the port is part of the HTR system
        '''
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