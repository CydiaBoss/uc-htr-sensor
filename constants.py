from pglive.kwargs import Axis
from enum import Enum
import numpy as np
from pyqtgraph import AxisItem
from time import strftime, localtime
import datetime 

from openqcm.common.architecture import Architecture,OSType

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

# QC Types
QC_5MHZ = "5 MHz"
QC_10MHZ = "10 MHz"

# Internal Usage
DATA_PARSE = r"([a-zA-Z ])Ω:(inf|\d+\.\d{2}),%RH:(inf|\d+\.\d{2}),°C:(inf|\d+\.\d{2})"
TIME_AXIS_CONFIG = {
    "orientation": "bottom",
    "text": "Time", 
    "units": "s", 
    "tick_angle":-45, 
    Axis.TICK_FORMAT: Axis.TIME
}

# QCM Specific Constants
###############################################################################    
# Enum for the types of sources. Indices MUST match app_sources constant
###############################################################################
class SourceType(Enum):
    serial = 1
    calibration = 0
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
    app_title = "openQCM Next Python SW"
    # VER 0.1.5
    # app version is the string checked for software update 
    app_version = '0.1.5'
    app_sources = ["Calibration", "Single Measurement", "Multiscan Measurement"]
    app_encoding = "utf-8"
    
    # VER 0.1.5 Firmware version compatible with the current application
    # check for more information the arduino source code attached
    FW_VERSION = '0.1.5'
    
    ###################
    # PLOT parameters #
    ###################
    
    # TODO DEV SWEEP1HZ change the plot update to 200 mss at least
    
# =============================================================================
#     plot_update_ms = 100
# =============================================================================
    
    # VER 0.1.4
    # change plot update time to 250 ms general improvement of overall software timing
    plot_update_ms = 250
    
    
    plot_colors = ['#ff0000', '#0072bd', '#00ffff', '#edb120', '#000000', '#77ac30', '#4dbeee', '#a2142f'] 
    plot_max_lines = len(plot_colors)
    
    plot_line_width = 1.2
    
    # #ffffff
    plot_title_color = 'default'
    
    plot_color_multi = ['#DF0101','#3C3C3C','#01DF01', '#01A9DB', '#7401DF'] 
                        
    name_legend = ["0th", "3rd", "5th", "7th", "9th"]                        
    
    overtone_dummy = [0, 1, 2, 3, 4]
    
    plot_background_color = "w"
    
    # samples of data ring buffer 
    # VER 0.1.4 reduce ring buffer size to 10 samples
    environment = 10
    
    # real-time chart history length 
    ring_buffer_samples = 16384 #8192
    
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
        
    # VER 0.2 BETA TODO
    # change the number of data points so that you have a frequency sweep step of 1 HZ
    
    # VER 0.1.3 change the number of data points so that you have a frequency sweep step of 50 Hz
    # FREQUENCY_STEP = 50 
    
    # VER 0.1.4 decrease the frequency sampling rate to 1 Hz  
    # change frequency step to change the frequency sampling rate and the sweep data points accordingly
    FREQUENCY_STEP = 1
    argument_default_samples = int((LEFT + RIGHT)/FREQUENCY_STEP + 1)
    SAMPLES = int((LEFT + RIGHT)/FREQUENCY_STEP)
    
    # VER 0.1.4 define the threshold in dB for the bandwidth calculation 
    THRESHOLD_DB = 0.3
    
    ###########################
    # Ring Buffers Parameters #
    ###########################
   
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
    
    # Savitzky-Golay order of the polynomial fit (common for all)
    SG_order = 3
    
    # VER 0.1.4 TODO
    # Savitzky-Golay window size definition 
    SG_WINDOW_SIZE = 51
    
    # VER 0.1.4
    #--------------
    # 5MHz 
    #--------------
    # left and right frequencies
    L5_fundamental = LEFT
    R5_fundamental = RIGHT
    # Savitzky-Golay size of the data window 
    SG_window_size5_fundamental = SG_WINDOW_SIZE
    # Spline smoothing factor
    Spline_factor5_fundamental = SPLINE_FACTOR
    
    # left and right frequencies
    L5_3th_overtone = LEFT
    R5_3th_overtone = RIGHT
    # Savitzky-Golay size of the data window 
    SG_window_size5_3th_overtone = SG_WINDOW_SIZE
    # Spline smoothing factor
    Spline_factor5_3th_overtone = SPLINE_FACTOR
    
    # left and right frequencies
    L5_5th_overtone = LEFT
    R5_5th_overtone = RIGHT
    # Savitzky-Golay size of the data window 
    SG_window_size5_5th_overtone = SG_WINDOW_SIZE
    # Spline smoothing factor
    Spline_factor5_5th_overtone = SPLINE_FACTOR
    
    # VER 0.1.2
    # change the sweep range same sweep range for all overtones
    L5_7th_overtone = LEFT
    R5_7th_overtone = RIGHT
    # Savitzky-Golay size of the data window 
    SG_window_size5_7th_overtone = SG_WINDOW_SIZE
    # Spline smoothing factor
    Spline_factor5_7th_overtone = SPLINE_FACTOR
    
    # left and right frequencies 
    L5_9th_overtone = LEFT
    R5_9th_overtone = RIGHT
    # Savitzky Golay size of the data window 
    SG_window_size5_9th_overtone = SG_WINDOW_SIZE
    # Spline smoothing factor
    Spline_factor5_9th_overtone = SPLINE_FACTOR

    #--------------
    # 10MHz 
    #--------------
    # VER 0.1.4    
    # left and right frequencies fundamental 
    L10_fundamental = LEFT
    R10_fundamental = RIGHT
    # Savitzky-Golay size of the data window 
    SG_window_size10_fundamental = SG_WINDOW_SIZE
    # Spline smoothing factor
    Spline_factor10_fundamental = SPLINE_FACTOR
     
    # left and right frequencies 3rd overtone
    L10_3th_overtone = LEFT
    R10_3th_overtone = RIGHT
    # Savitzky-Golay size of the data window 
    SG_window_size10_3th_overtone = SG_WINDOW_SIZE    
    # Spline smoothing factor
    Spline_factor10_3th_overtone = SPLINE_FACTOR
    
    # left and right frequencies 5th overtone
    L10_5th_overtone = LEFT
    R10_5th_overtone = RIGHT
    # Savitzky-Golay size of the data window 
    SG_window_size10_5th_overtone = SG_WINDOW_SIZE
    # Spline smoothing factor
    Spline_factor10_5th_overtone = SPLINE_FACTOR
  
    ##########################
    # SERIAL PORT Parameters #
    ##########################
    serial_default_speed = 115200
    serial_default_overtone = None
    serial_default_QCS = "@10MHz"
    
    # VER 0.1.4
    # change / increased serial timeout parameters to improve the serial communication 
    serial_writetimeout_ms = 4.0
    serial_timeout_ms = 4.0
    
    null_string = ""
    
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
    # VER 0.1.4
    # change / increased the process join timeout
    process_join_timeout_ms = 4000
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
    
    # VER 0.1.2 
    # set directory slash, solving bug for macOS Big Sur
    # sets the slash depending on the OS types
    if Architecture.get_os() is (OSType.linux or OSType.macosx):
        # print ("MAC_OS_X")
        slash = "/"

    elif Architecture.get_os() is OSType.windows:
        # print("WINDOWS")
        slash = "\\"
    else:
        # print ("OTHER_OS")
        slash = "/"
       
    csv_delimiter = "," # for splitting data of the serial port and CSV file storage
    csv_default_prefix = "%Y-%b-%d_%H-%M-%S"#"%H-%M-%S-%d-%b-%Y" # Hour-Minute-Second-month-day-Year
    csv_extension = "csv"
    txt_extension = "txt"
    csv_export_path = "logged_data"
    
    # DEV RAWDATA
    sweep_export_path = "sweep_data"
    
    csv_filename = (strftime(csv_default_prefix, localtime())) #+'_DataLog')
    csv_sweeps_export_path = "{}{}{}".format(csv_export_path,slash,csv_filename)
    csv_sweeps_filename = "sweep"
    
    # Calibration: scan (WRITE for @5MHz and @10MHz QCS) path: 'common\'
    csv_calibration_filename    = "Calibration_5MHz"
    csv_calibration_filename10  = "Calibration_10MHz"
    csv_calibration_export_path = "openQCM" #"common"
    
    # Calibration: baseline correction (READ for @5MHz and @10MHz QCS) path: 'common\'
    csv_calibration_path   = "{}{}{}.{}".format(csv_calibration_export_path,slash,csv_calibration_filename,txt_extension)
    csv_calibration_path10 = "{}{}{}.{}".format(csv_calibration_export_path,slash,csv_calibration_filename10,txt_extension)
    
    # Frequencies: Fundamental and overtones (READ and WRITE for @5MHz and @10MHz QCS)
    csv_peakfrequencies_filename   = "PeakFrequencies"
    cvs_peakfrequencies_path    = "{}{}{}.{}".format(csv_calibration_export_path,slash,csv_peakfrequencies_filename,txt_extension)
    
    
    # VER 0.1.4
    # add a new peak freqencies file storing the current value of resonance frequencies 
    csv_peakfrequencies_RT_filename   = "PeakFrequenciesRT"
    cvs_peakfrequencies_RT_path    = "{}{}{}.{}".format(csv_calibration_export_path, slash, csv_peakfrequencies_RT_filename, txt_extension)
    
    # TODO freuqwency start and stop file path
    manual_frequencies_filename = "config"
    manual_frequencies_path = "{}{}{}.{}".format(csv_calibration_export_path,slash,manual_frequencies_filename,txt_extension)
    
    sweep_file = "sweep"
    sweep_file_path = "{}{}{}.{}".format(csv_calibration_export_path, slash, sweep_file , txt_extension)
    
    ##########################
    # CALIBRATION PARAMETERS #
    ##########################
    
    # Peak Detection - distance in samples between neighbouring peaks
    calibration_frequency_start =  1000000
    calibration_frequency_stop  = 51000000 

    # VER 0.1.4a Change the calibration frequency step to increase the resolution 
    # calibration frequewncy range for each section 
    calib_fRange = 5000000 
    # calibration frequency section 
    calib_sections = 10
    
    # VER 0.1.4a CHANGE CALIBRATION  FREQUENCY STEP to 500 Hz 
    calib_fStep = 500
    calibration_fStep = calib_fStep
    
    # number of samples in a calibration section 
    calib_samples = int((calib_fRange / calib_fStep) + 1)
    
    # VER 0.1.4a calibration total frequency array 
    calibration_default_samples = int( (calib_samples - 1) * calib_sections) + 1
    calibration_readFREQ  = np.arange(calibration_default_samples) * (calib_fStep) + calibration_frequency_start
    

    # VER 0.1.4a change the peak detection distance in accordance with the frequency step
    # Peak Detection - distance in samples between neighbouring peaks
    # 5 MHz sensor minimum frequency distance between successive peaks = 8 MHz
    dist5MHz = 8000000
    # 5 MHz sensor minimum frequency distance between successive peaks = 10 MHz
    dist10MHz = 10000000 
    # 5 MHz minimum distance in terms of samples
    dist5  =  int(dist5MHz/calib_fStep) 
    # 10 MHz minimum distance in terms of samples
    dist10 =  int(dist10MHz/calib_fStep)
     
    
    ##############################
    # Parameters for the average #
    ##############################  
   
    SG_order_environment = 1
    SG_window_environment = 3
    
###############################################################################
#  Provides a date-time aware axis
###############################################################################  
class DateAxis(AxisItem): 
    def __init__(self, *args, **kwargs):
        super(DateAxis, self).__init__(*args, **kwargs)            
          
    def tickStrings(self, values, scale, spacing):    
        TS_MULT_us = 1e6
        try:
            z= [(datetime.datetime.utcfromtimestamp(float(value)/TS_MULT_us)).strftime("%H:%M:%S") for value in values]
        except: 
            z= ''
        return z

###############################################################################
#  Provides a non scientific axis notation
###############################################################################  
class NonScientificAxis(AxisItem):
    def __init__(self, *args, **kwargs):
        super(NonScientificAxis, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [int(value*1) for value in values] 
