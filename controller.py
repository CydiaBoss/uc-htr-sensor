# ================================ #
# Code to communicate with sensors #
# ================================ #
from serial import Serial
import time, atexit

from constants import READ_TIMEOUT
from tools import active_ports

class SensorCtrl:
    '''
    Class of sensor controls
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

        # Open first port or specified port
        self.sensor = Serial(port=port if port != "" else self.ports[0], baudrate=baud, timeout=timeout)

        # Wait for Launch Message
        tick_to_timeout = 0
        while "Running" not in self.read_from():
            # Timeout
            if tick_to_timeout > READ_TIMEOUT:
                print("System failed to start. Closing.")
                self.sensor.close()
                exit(code=404)
            tick_to_timeout += 1
            time.sleep(1)

        # Success
        print(f"Sensors connected at port {self.sensor.port}!")

        # Prep for exit
        atexit.register(lambda : self.sensor.close())

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