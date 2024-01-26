from controller import SensorCtrl
import time

# Connection to Snesors
ctrl = SensorCtrl(port="COM5", baud=9600, timeout=.1)

# Serial Monitor
while True:
    print(ctrl.read_from(), end="")
    time.sleep(1.5)