from pglive.kwargs import Axis
from enum import Enum
import numpy as np
from pyqtgraph import AxisItem
from time import strftime, localtime
from datetime import datetime 
import platform, sys

from misc.settings import Settings

from enum import Enum

# Settings
SETTINGS = Settings()
AUTO_EXPORT = True
AUTO_FLUSH = 50
BAUD = 9600
SENSOR_TIMEOUT = 0.1
READ_TIMEOUT = 5
READ_DELAY = 1.0
MIN_WIDTH = 1750
MIN_HEIGHT = 1000
UNCERTAINTIES = 0.10

# Folders
DATA_FOLDER = "data"
LOG_FOLDER = "logs"

# References
REF_RESIST_UNIT = lambda : SETTINGS.get_setting("ref_resist_unit") or " "

# QC Types
QC_5MHZ = "5 MHz"
QC_10MHZ = "10 MHz"

# Internal Usage
DATA_PARSE = r"([a-zA-Z ])Ω:(inf|\d+\.\d{2}),%RH:(inf|\d+\.\d{2}),°C:(inf|\d+\.\d{2})"
REF_RESIST_PARSE = r"(\d+(\.\d+)?)([a-zA-Z ])"
TIME_AXIS_CONFIG = {
    "orientation": "bottom",
    "text": "Time", 
    "units": "s", 
    "tick_angle":-45, 
    Axis.TICK_FORMAT: Axis.DURATION
}
FREQ_AXIS_CONFIG = {
    "orientation": "bottom",
    "text": "Frequency", 
    "units": "Hz", 
}

# Progress
QPB_DEFAULT_STYLE = """
QProgressBar{
    border: 1px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: lightblue;
    width: 10px;
    margin: 1px;
}
"""

QPB_COMPLETED_STYLE = """
QProgressBar::chunk {
    background-color: lightgreen;
}
"""

QPB_ERROR_STYLE = """
QProgressBar::chunk {
    background-color: lightpink;
}
"""

# QCM Specific Constants
###############################################################################
# Architecture specific methods: OS types, Python version
###############################################################################
class Architecture:

    ###########################################################################
    # Gets the current OS
    ###########################################################################    
    @staticmethod
    def get_os():
        #:return: OS type by OSType enum.
        tmp = str(Architecture.get_os_name())
        if "Linux" in tmp:
            return OSType.linux
        elif "Windows" in tmp:
            return OSType.windows
        elif "Darwin" in tmp:
            return OSType.macosx
       
        # macOS 12 compatibility SOLVED 
        elif "macOS" in tmp :
            return OSType.macosx
        
        else:
            return OSType.unknown
        
    ###########################################################################
    # Gets the current OS name string (as reported by platform)
    ###########################################################################
    @staticmethod
    def get_os_name():
        #:return: OS name :rtype: str.
        return platform.platform()

    ###########################################################################
    # Gets the PWD or CWD of the currently running application
    # (Print Working Directory, Change Working Directory)
    ###########################################################################    
    @staticmethod
    def get_path():
        #:return: Path of the PWD or CWD :rtype: str.
        return sys.path[0]

    ###########################################################################
    # Gets the running Python version
    ###########################################################################
    @staticmethod
    def get_python_version():
        #:return: Python version formatted as major.minor.release :rtype: str.
        version = sys.version_info
        return str("{}.{}.{}".format(version[0], version[1], version[2]))

    ###########################################################################
    # Checks if the running Python version is >= than the specified version
    ###########################################################################    
    @staticmethod
    def is_python_version(major, minor=0):
        """
        :param major: Major value of the version :type major: int.
        :param minor: Minor value of the version :type minor: int.
        :return: True if the version specified is >= than the current version.
        :rtype: bool.
        """
        version = sys.version_info
        if version[0] >= major and version[1] >= minor:
            return True
        return False

###############################################################################
# Enum for OS types
###############################################################################            
class OSType(Enum):
    unknown = 0
    linux = 1
    macosx = 2
    windows = 3

###############################################################################    
# Enum for the types of sources. Indices MUST match app_sources constant
###############################################################################
class SourceType(Enum):
    serial = 0
    calibration = 1
    multiscan = 2
    
###############################################################################
# Specifies the minimal Python version required
###############################################################################
class MinimalPython:
    major = 3
    minor = 2
    release = 0    

###############################################################################    
# Common constants and parameters for the application.
###############################################################################
class Constants:
    
    ##########################
    # Application Parameters #
    ##########################
    app_title = "Real-Time QCM GUI"
    app_version = '2.1'
    app_sources = ["Multi-Measurement", "Measurement openQCM Q-1 Device", "Calibration openQCM Q-1 Device"]
    app_encoding = "utf-8"
    
    
    ###################
    # PLOT parameters #
    ###################
    plot_update_ms = 200
    plot_colors = ['#ff0000', '#0072bd', '#00ffff', '#edb120', '#7e2f8e', '#77ac30', '#4dbeee', '#a2142f'] 
    plot_max_lines = len(plot_colors)
    plot_title_color = 'default'

    plot_color_multi = ['#DF0101','#3C3C3C','#01DF01', '#01A9DB', '#7401DF'] 
                        
    name_legend = ["0th", "3rd", "5th", "7th", "9th"]                        
    
    overtone_dummy = [0, 1, 2, 3, 4]
    
    plot_background_color = "w"
    
    ####################
    #  SAMPLES NUMBER  #
    ####################
    argument_default_samples = 501
    
    ####################################
    # FILTERING and FITTING parameters #
    ####################################
    # Notes:
    # left and right frequencies in the area of the resonance frequency
    # Savitzky-Golay size of the data window 
    # Savitzky-Golay order of the polynomial fit
    # Number of spline points: same as the frequency band +1 (es.5001)
    # Spline smoothing factor
    
    # Savitzky-Golay order of the polynomial fit (common for all)
    SG_order = 3

    #--------------
    # 5MHz 
    #--------------
    # left and right frequencies
    L5_fundamental = 5500
    R5_fundamental = 2500
    # Savitzky-Golay size of the data window 
    SG_window_size5_fundamental = 9
    # Spline smoothing factor
    Spline_factor5_fundamental = 0.05
    # left and right frequencies
    L5_3th_overtone = 7500
    R5_3th_overtone = 2500
    # Savitzky-Golay size of the data window 
    SG_window_size5_3th_overtone = 11
    # Spline smoothing factor
    Spline_factor5_3th_overtone = 0.01
    
    # left and right frequencies
    L5_5th_overtone = 10000
    R5_5th_overtone = 2500
    # Savitzky-Golay size of the data window 
    SG_window_size5_5th_overtone = 11
    # Spline smoothing factor
    Spline_factor5_5th_overtone = 0.01
    
    # left and right frequencies
    L5_7th_overtone = 50000
    R5_7th_overtone = 2500
    # Savitzky-Golay size of the data window 
    SG_window_size5_7th_overtone = 33
    # Spline smoothing factor
    Spline_factor5_7th_overtone = 0.01
    
    # left and right frequencies 
    L5_9th_overtone = 5000000
    R5_9th_overtone = 100000
    # Savitzky-Golay size of the data window 
    SG_window_size5_9th_overtone = 5
    # Spline smoothing factor
    Spline_factor5_9th_overtone = 0.5
    
    #--------------
    # 10MHz 
    #--------------
    # left and right frequencies
    L10_fundamental = 7500
    R10_fundamental = 2500
    # Savitzky-Golay size of the data window 
    SG_window_size10_fundamental = 11
    # Spline smoothing factor
    Spline_factor10_fundamental = 0.01
    
    # left and right frequencies
    L10_3th_overtone = 13500
    R10_3th_overtone = 2500
    # Savitzky-Golay size of the data window 
    SG_window_size10_3th_overtone = 11    
    # Spline smoothing factor
    Spline_factor10_3th_overtone = 0.01
    
    # left and right frequencies
    L10_5th_overtone = 23000
    R10_5th_overtone = 3000
    # Savitzky-Golay size of the data window 
    SG_window_size10_5th_overtone = 19
    # Spline smoothing factor
    Spline_factor10_5th_overtone = 0.01

    ##########################
    # SERIAL PORT Parameters #
    ##########################
    serial_default_speed = 115200
    serial_default_overtone = None
    serial_default_QCS = "10 MHz"
    serial_writetimeout_ms = 0
    serial_timeout_ms = None#0.01
    
    # VER 0.1.4
    # change / increased serial time elasped timeout to improve the serial communication 
    TIME_ELAPSED_TIMEOUT = 4.0
    
    WRITE_SERIAL_WAIT = 0.1 
    
    # VER 0.1.4
    # TIME WAITING CONSTANTS 
    SLEEP_EOM_MULTISCAN = 0.05
    SLEEP_EOM_SINGLE    = 0.2

    ######################
    # Process parameters #
    ######################
    process_join_timeout_ms = 2000
    simulator_default_speed = 0.1 # not used
    parser_timeout_ms = 0.005
    
    ##################
    # Log parameters #
    ##################
    log_export_path = "logged_data"
    log_filename = "{}.log".format(app_title)
    log_max_bytes = 5120
    log_default_level = 1
    log_default_console_log = False
    
    ######################################
    # File parameters for exporting data #
    ######################################
    # sets the slash depending on the OS types
    if Architecture.get_os() is (OSType.macosx or OSType.linux):
       slash="/"
    else:
       slash="\\"
       
    csv_delimiter = "," # for splitting data of the serial port and CSV file storage
    csv_default_prefix = "%Y-%b-%d_%H-%M-%S"#"%H-%M-%S-%d-%b-%Y" # Hour-Minute-Second-month-day-Year
    csv_extension = "csv"
    txt_extension = "txt"
    csv_export_path = "data"
    csv_filename = (strftime(csv_default_prefix, localtime()))
    csv_sweeps_export_path = "{}{}{}".format(csv_export_path,slash,csv_filename)
    csv_sweeps_filename = "sweep"
    
    # Calibration: scan (WRITE for 5 MHz and 10 MHz QCS) path: 'common\'
    csv_calibration_filename    = "calibration_5MHz"
    csv_calibration_filename10  = "calibration_10MHz"
    csv_calibration_export_path = "core" #"common"
    
    ################## 
    # Calibration: baseline correction (READ for 5 MHz and 10 MHz QCS) path: 'common\'
    csv_calibration_path   = "{}{}{}.{}".format(csv_calibration_export_path,slash,csv_calibration_filename,txt_extension)
    csv_calibration_path10 = "{}{}{}.{}".format(csv_calibration_export_path,slash,csv_calibration_filename10,txt_extension)
    
    # Frequencies: Fundamental and overtones (READ and WRITE for 5 MHz and 10 MHz QCS)
    csv_peakfrequencies_filename   = "peak_freq"
    cvs_peakfrequencies_path    = "{}{}{}.{}".format(csv_calibration_export_path,slash,csv_peakfrequencies_filename,txt_extension)
    #cvs_peakfrequencies_path10 = "{}{}{}.{}".format(csv_calibration_export_path,slash,csv_peakfrequencies_filename10,txt_extension)    
    #########################    
    
    # VER 0.1.4
    # add a new peak freqencies file storing the current value of resonance frequencies 
    csv_peakfrequencies_RT_filename   = "peak_freq_rt"
    cvs_peakfrequencies_RT_path    = "{}{}{}.{}".format(csv_calibration_export_path, slash, csv_peakfrequencies_RT_filename, txt_extension)
    
    manual_frequencies_filename = "config"
    manual_frequencies_path = "{}{}{}.{}".format(csv_calibration_export_path,slash,manual_frequencies_filename,txt_extension)
    
    sweep_file = "sweep"
    sweep_file_path = "{}{}{}.{}".format(csv_calibration_export_path, slash, sweep_file , txt_extension)
    
    ##########################
    # CALIBRATION PARAMETERS #
    ##########################
    
    # VER 0.1.4a change the peak detection distance in accordance with the frequency step
    # Peak Detection - distance in samples between neighbouring peaks
    # 5 MHz sensor minimum frequency distance between successive peaks = 8 MHz
    dist5MHz = 8000000
    # 5 MHz sensor minimum frequency distance between successive peaks = 10 MHz
    dist10MHz = 10000000 
    
    # Peak Detection - distance in samples between neighbouring peaks
    dist5  =  8000 # for 5 MHz
    dist10 =  10000 # for 10 MHz
    calibration_default_samples = 50001
    calibration_frequency_start =  1000000
    calibration_frequency_stop  = 51000000 
    calibration_fStep = (calibration_frequency_stop - calibration_frequency_start) / (calibration_default_samples-1)
    calibration_readFREQ  = np.arange(calibration_default_samples) * (calibration_fStep) + calibration_frequency_start
    #-------------------
    calib_fStep = 1000
    calib_fRange = 5000000 #
    calib_samples = 5001
    calib_sections = 10
    
    ###########################
    # Ring Buffers Parameters #
    ###########################
    ring_buffer_samples = 16363
    
    PID_default_settings = ["Default #0 (Factory)", "Default #1"]
    
    # default factory #0 and default openQCM #1 list element
    cycling_time_setting  = [50, 50]
    P_share_setting  = [1000, 500]
    I_share_setting  = [200, 50]
    D_share_setting  = [100, 300]
    
    PID_Setting_default_index = 1
    
    # set temperature default parameter
    Temperature_Set_Value = 25.00
    # set PID default parameter 
    cycling_time_default = cycling_time_setting[1]
    P_share_default = P_share_setting[1]
    I_share_default = I_share_setting[1]
    D_share_default = D_share_setting[1]
    # boolean variable temperature setting 
    PID_boolean_default = 0 
    # boolean control temperature setting 
    CTRL_boolean_default = 0
    
    ##############################
    # Parameters for the average #
    ##############################  
    environment = 50 #######################################################################################################
    SG_order_environment = 1
    SG_window_environment = 3
    
    # VER 0.1.4 init the sampling time list
    SAMPLING_TIME_LIST = ["Default", "10", "30", "60"]
    SAMPLING_TIME_LIST_DEFAULT_INDEX = 0
    
    # VER 0.1.4
    # define and init TEC status control variable
    # -------------------------------------------
    # temperature control active, temperature is out of range, electric current is null
    STATUS_CONTROL_ACTIVE_LOW_CURRENT_NULL = -1
    
    # temperature control NOT active 
    STATUS_CONTROL_NOT_ACTIVE = 0
    
    # temperature control active, temperature is out of range, electric current is NOT null
    STATUS_CONTROL_ACTIVE_LOW_CURRENT_NOT_NULL = 1
    
    # temperature control active and temperature in range
    STATUS_CONTROL_ACTIVE_HIGH = 2
    
    # VER 0.1.5
    # init MTD415T error register list, 
    # as in paragraph 6.3 Error Register and Safety Bitmask, MTD415T Data Sheet Rev. 1.2
    ERROR_REG_EVENT = ["Enable pin not set", 
                       "Internal temperature too high", 
                       "Thermal Latch-Up",
                       "Cycling time too small", 
                       "No Sensor detected", 
                       "No TEC detected", 
                       "TEC mispoled", 
                       "Not used", "Not used", "Not used", "Not used", "Not used", "Not used"
                       "Value out of range", 
                       "Invalid command", 
                       "Not used"] 
    
    ####################
    #  SAMPLES NUMBER  #
    ####################
    
    # VER 0.1.4
    # change the sweep parameters to 12 KHz left range and 6 KHz right range 
    # for a total range fo frequency sweep = 18 KHz
    LEFT = 12000
    
    # VER 0.1.4 increase sweep right range, because the sweep box is now center on the peak of the resonance curve     
    RIGHT = 6000
    
    # VER 0.1.3 
    # change the spline factor for a better smoothing of the raw amplitude signal 
    # SPLINE_FACTOR = 0.1     # VER 0.1.3 TODO spline factor depends on the number of sample SAMPLES = int((LEFT + RIGHT)/FREQUENCY_STEP)

    # VER 0.1.4 increase spline factor for smoothing with 1 Hz sampling frequency   
    SPLINE_FACTOR = 1
    # VER 0.1.4 find the best spline factor 
    
    # VER 0.1.4 decrease the frequency sampling rate to 1 Hz  
    # change frequency step to change the frequency sampling rate and the sweep data points accordingly
    FREQUENCY_STEP = 1
    SAMPLES = int((LEFT + RIGHT)/FREQUENCY_STEP)
    
    # VER 0.1.4 define the threshold in dB for the bandwidth calculation 
    THRESHOLD_DB = 0.3
   
    
    # TODO MAXIMUM NUMBER OF OVERTONES 
    overtone_maximum_number = 4
    
    ####################################
    # FILTERING and FITTING parameters #
    ####################################
    # Notes:
    # left and right frequencies in the area of the resonance frequency
    # Savitzky-Golay size of the data window 
    # Savitzky-Golay order of the polynomial fit
    # Number of spline points: same as the frequency band +1 (es.5001)
    # Spline smoothing factor
    
    # VER 0.1.4 TODO
    # Savitzky-Golay window size definition 
    SG_WINDOW_SIZE = 51
        
###############################################################################
#  Provides a date-time aware axis
###############################################################################  
class DateAxis(AxisItem): 
    def __init__(self, *args, **kwargs):
        super(DateAxis, self).__init__(*args, **kwargs)            
          
    def tickStrings(self, values, scale, spacing):    
        TS_MULT_us = 1e6
        try:
            z= [(datetime.datetime.utcfromtimestamp(float(value)/TS_MULT_us)).strftime("%b-%d %H:%M:%S") for value in values]
        except: 
            z= ''
        return z
        #return [(datetime.datetime.utcfromtimestamp(float(value)/TS_MULT_us)).strftime("%b-%d %H:%M:%S") for value in values]


###############################################################################
#  Provides a non scientific axis notation
###############################################################################  
class NonScientificAxis(AxisItem):
    def __init__(self, *args, **kwargs):
        super(NonScientificAxis, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [int(value*1) for value in values] 