from pglive.kwargs import Axis

# Settings
AUTO_EXPORT = True
AUTO_FLUSH = 50
BAUD = 9600
SENSOR_TIMEOUT = 0.1
READ_TIMEOUT = 5
READ_DELAY = 1.0

# References
REF_RESIST = 10
REF_RESIST_UNIT = ' '
REF_VOLT = 5.099

# Internal Usage
DATA_PARSE = r"([a-zA-Z ])Ω:(inf|\d+\.\d{2}),%RH:(inf|\d+\.\d{2}),°C:(inf|\d+\.\d{2})"
TIME_AXIS_CONFIG = {
    "orientation": "bottom",
    "text": "Time", 
    "units": "s", 
    "tick_angle":-45, 
    Axis.TICK_FORMAT: Axis.TIME
}