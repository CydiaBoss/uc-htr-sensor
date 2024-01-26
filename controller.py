# ================================ #
# Code to communicate with sensors #
# ================================ #
from serial import Serial
import time
import atexit

class SensorCtrl:
    '''
    Class of sensor controls
    '''

    def __init__(self, port : str, baud : int=9600, timeout=0.1):
        self.sensor = Serial(port=port, baudrate=baud, timeout=timeout)

        # Wait for Launch Message
        tick_to_timeout = 0
        while "Running" not in self.read_from():
            # Timeout
            if tick_to_timeout > 15:
                print("System failed to start. Closing.")
                self.sensor.close()
                exit(code=404)
            tick_to_timeout += 1
            time.sleep(1)

        # Success
        print("Sensors connected!")

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

    def update_ref_volt(self, volt : float) -> bool:
        '''
        Updates the reference voltage on the sensor
        '''
        self.send_to(f'v{volt}')

    def read_from(self):
        '''
        Read from the sensor
        '''
        return self.sensor.readline().decode("utf-8")