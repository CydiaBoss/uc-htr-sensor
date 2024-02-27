from multiprocessing import Queue

from misc.constants import Constants, SourceType
from misc.logger import Logger as Log

from openqcm.processes.parser import ParserProcess
from openqcm.processes.serial import SerialProcess
from openqcm.processes.calibration import CalibrationProcess
from openqcm.processes.multiscan import MultiscanProcess
from openqcm.core.ring_buffer import RingBuffer

import numpy as np
from numpy import loadtxt
import datetime

# VER 0.1.2
from time import time, strftime, localtime, sleep

# NEW Signals
from PyQt5.QtCore import pyqtSignal, QObject

TAG = ""#"[Worker]"

###############################################################################
# Service that creates and concentrates all processes to run the application
###############################################################################
class Worker(QObject):

    # Signals
    progress = pyqtSignal()
    frequency = pyqtSignal(float)
    dissipation = pyqtSignal(float)
    temperature = pyqtSignal(float)

    ###########################################################################
    # Creates all processes involved in data acquisition and processing
    ###########################################################################
    def __init__(self, 
                      parent = None,
                      QCS_on = None,
                      port = None,
                      speed = Constants.serial_default_overtone,
                      samples = Constants.argument_default_samples,
                      source = SourceType.serial,
                      export_enabled = False, 
                      sampling_time = None):
        """
        :param port: Port to open on start :type port: str.
        :param speed: Speed for the specified port :type speed: float.
        :param samples: Number of samples :type samples: int.
        :param source: Source type :type source: SourceType.
        :param export_enabled: If true, data will be stored or exported in a file :type export_enabled: bool.
        :param export_path: If specified, defines where the data will be exported :type export_path: str.
        """
        super().__init__(parent)

        # data queues 
        self._queue1 = Queue()
        self._queue2 = Queue()
        self._queue3 = Queue()
        self._queue4 = Queue()
        self._queue5 = Queue()
        self._queue6 = Queue()
        
        self._queue_F_multi = Queue()
        self._queue_D_multi = Queue()
        
        # TODO AMPLI init the queue for amplitude sweep 
        self._queue_A_multi = Queue()
        self._queue_P_multi = Queue()
        self._queue_F_SWEEP_multi = Queue()
        
        # TODO AMPLI init the list of array for amplitude sweep
        self._A_multi = None 
        self._P_multi = None 
        
        self._A_multi_buffer = None
        self._P_multi_buffer = None
        self._F_Sweep_multi_buffer = None
        
        # data buffers
        self._data1_buffer = None # amplitude 
        self._data2_buffer = None # phase 
        self._d1_buffer = None  # Frequency     type RingBuffer
        self._d2_buffer = None  # Dissipation   type RingBuffer
        self._d3_buffer = None  # Temperature   type RingBuffer
        self._t1_buffer = None  # time (frequency) type RingBuffer
        self._t2_buffer = None  # time (dissipation) type RingBuffer
        self._t3_buffer = None  # time (temperature) type RingBuffer
        self._ser_error1 = 0
        self._ser_error2 = 0
        self._ser_err_usb= 0
        self._control_k = 0
        
        self._F_multi_buffer = None
        self._D_multi_buffer = None
        
        self._F_store = None 
        self._D_store = None 
        self._time_buffer = None
        self._time_store = None
        
        # current overtone number 
        self._overtone_number = 0
        # total number of overtone 
        self._number_of_peaks = 0
        
        # VER 0.1.4
        # TEC status var
        self._TEC_status = 0
        
        # instances of the processes
        self._acquisition_process = None
        self._parser_process = None
        
        # others
        self._QCS_on = QCS_on # QCS installed on device (unused now)
        self._port = port     # serial port 
        # overtones (str) if 'serial' is called
        # QCS (str) if 'calibration' is called 
        self._speed = speed 
        self._samples = samples
        self._source = source
        self._export = export_enabled
        
        # Supporting variables
        self._d1_store = None # data storing
        self._d2_store = None # data storing
        
        # SINGLE 
        self._readFREQ = None # frequency range
        self._fStep    = None # sample rate
        self._overtone_name  = None # fundamental/overtones name (str)
        self._overtone_value = None # fundamental/overtones value(float)
        
        # MULTI 
        self._readFREQ_array = None 
        
        self._count = 0 # sweep counter
        self._flag = True
        self._timestart = 0
        
        # VER 0.1.2
        # init log file name 
        self._csv_filename = ""
        
        # VER 0.1.4
        self._sampling_time = sampling_time
        self.time_elapsed = 0
        # init a ring buffer of corresponding size 
        self.ring_buffer_len =  1
        
        # init a list of ring buffer 
        self._F_store_buffer = None 
        self._D_store_buffer = None 
        self._T_store_buffer = None
        
        self._F_store_buffer_averaging = None 
        self._D_store_buffer_averaging = None
        self._T_store_buffer_averaging = None
        
    ###########################################################################
    # Starts all processes, based on configuration given in constructor.
    ###########################################################################
    def start(self):
        
        # GET SAMPLES
        # ---------------------------------------------------------------------
        # single frequency measurement 
        if self._source == SourceType.serial:
           self._samples = Constants.argument_default_samples

        # calibration 
        elif self._source == SourceType.calibration:
           self._samples = Constants.calibration_default_samples
           self._readFREQ = Constants.calibration_readFREQ  

        # multi frequency measurement 
        elif self._source == SourceType.multiscan: 
            self._samples = Constants.argument_default_samples   
            
        # Setup/reset the internal buffers
        self.reset_buffers(self._samples)
        
        # Instantiates process
        self._parser_process = ParserProcess(self._queue1, self._queue2, self._queue3, self._queue4, self._queue5, self._queue6, 
                                             self._queue_F_multi, self._queue_D_multi, self._queue_A_multi, self._queue_P_multi)
        
        # GET and SET SOURCE TYPE 
        # ---------------------------------------------------------------------
        # Checks the type of source
        # single frequency measurement 
        if self._source == SourceType.serial:
            self._acquisition_process = SerialProcess(self._parser_process)

        # calibration
        elif self._source == SourceType.calibration:
            self._acquisition_process = CalibrationProcess(self._parser_process)

        # multi frequency measurement 
        elif self._source == SourceType.multiscan:
            self._acquisition_process = MultiscanProcess(self._parser_process)
            
        # OPEN PROCESS 
        # ---------------------------------------------------------------------    
        if self._acquisition_process.open(port=self._port, speed=self._speed):
            
            # SINGLE 
            # -----------------------------------------------------------------
            if self._source == SourceType.serial:
                (self._overtone_name,
                    self._overtone_value, 
                    self._fStep, 
                    self._readFREQ, 
                    SG_window_size, 
                    spline_points, 
                    _) = self._acquisition_process.get_frequencies(self._samples)
                
                print("")
                print(TAG, "DATA MAIN INFORMATION")
                print(TAG, "Selected frequency: {} - {}Hz".format(self._overtone_name,self._overtone_value))
                print(TAG, "Frequency start: {}Hz".format(self._readFREQ[0]))
                print(TAG, "Frequency stop:  {}Hz".format(self._readFREQ[-1]))
                print(TAG, "Frequency range: {}Hz".format(self._readFREQ[-1]-self._readFREQ[0]))
                print(TAG, "Number of samples: {}".format(self._samples-1))
                print(TAG, "Sample rate: {}Hz".format(self._fStep))
                print(TAG, "History buffer size: 180 min\n")
                print(TAG, "MAIN PROCESSING INFORMATION")
                print(TAG, "Method for baseline estimation and correction:")
                print(TAG, "Least Squares Polynomial Fit (LSP)")
                
                print(TAG, "Savitzky-Golay Filtering")
                print(TAG, "Order of the polynomial fit: {}".format(Constants.SG_order))
                print(TAG, "Size of data window (in samples): {}".format(SG_window_size))
                print(TAG, "Oversampling using spline interpolation")
                print(TAG, "Spline points (in samples): {}".format(spline_points-1))
                print(TAG, "Resolution after oversampling: {}Hz".format((self._readFREQ[-1]-self._readFREQ[0])/(spline_points-1)))
               
            # CALIBRATION
            elif self._source == SourceType.calibration:
                print("")
                print(TAG, "MAIN CALIBRATION INFORMATION")
                print(TAG, "Calibration frequency start:  {}Hz".format(Constants.calibration_frequency_start))
                print(TAG, "Calibration frequency stop:  {}Hz".format(Constants.calibration_frequency_stop))
                print(TAG, "Frequency range: {}Hz".format(Constants.calibration_frequency_stop-Constants.calibration_frequency_start))
                print(TAG, "Number of samples: {}".format(Constants.calibration_default_samples-1))
                print(TAG, "Sample rate: {}Hz".format(Constants.calibration_fStep))
               
               
            # START MULTI SCAN FREQUENCY PROCESS 
            elif self._source == SourceType.multiscan: 
                # get the number of total peaks in PeakFrequencies.txt
                data  = loadtxt(Constants.cvs_peakfrequencies_path)
                peaks_mag = data[:,0]
                self._number_of_peaks = len(peaks_mag) - 1
            
            # START PROCESSES ACQUISITION and PARSER 
            # -----------------------------------------------------------------
            self._acquisition_process.start()
            self._parser_process.start()
            
            # VER 0.1.2
            # format the log data file 
            csv_default_prefix = "%Y-%b-%d_%H-%M-%S"
            self._csv_filename = (strftime(csv_default_prefix, localtime()))
            
            return True
        
        else:
            print(TAG, 'Warning: port is not available')
            Log.i(TAG, "Warning: Port is not available")
            return False

    ###########################################################################
    # Stops all running processes
    ###########################################################################    
    def stop(self):
        
        # VER 0.1.2
        # consume all queues 
        self.consume_queue1()
        self.consume_queue2()
        self.consume_queue3()
        self.consume_queue4()
        self.consume_queue5() 
        self.consume_queue6() 
        self.consume_queue_F_multi()
        self.consume_queue_D_multi()
        self.consume_queue_A_multi()
        
        # worker processes are still running when you press stop button on main gui 
        # when stop is called, terminate the processes alive in the worker 

        if self._acquisition_process is not None and self._acquisition_process.is_alive():
            # stop the process 
            self._acquisition_process.stop()
            
            # terminate the process 
            # https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process.terminate
            self._acquisition_process.terminate()
            
            # wait for a while 
            sleep(1)
            
        self._parser_process.stop()

        Log.i(TAG, "Running processes stopped...")
        Log.i(TAG, "Processes finished")
        
    
    # TODO DELETE TEMPERATURE FUNCTION 
    def get_Temperature_set_Worker(self, value):
         print ("SET TEMPERATURE WORKER")
         self._acquisition_process.get_Temperature_set_Serial(value)
        
    # TODO DELETE TEMPERATURE FUNCTION 
    def my_stop(self):
        self._acquisition_process.serial_close()
    
    # TODO DELETE TEMPERATURE FUNCTION 
    def serial_write(self, port, message):
        # self._acquisition_process.open(port)
        self._acquisition_process.write(port, message.encode())
                    
    ###########################################################################
    # Empties the internal queues, updating data to consumers
    ###########################################################################    
    def consume_queue1(self):
        # queue1 for serial data: amplitude
        while not self._queue1.empty():
            self._queue_data1(self._queue1.get(False))
    
    def consume_queue2(self):
        # queue2 for serial data: phase
        while not self._queue2.empty():
            self._queue_data2(self._queue2.get(False))

    # FREQUENCY 
    def consume_queue3(self):
        # queue3 for elaborated data: resonance frequency
        while not self._queue3.empty():
            self._queue_data3(self._queue3.get(False))
            
    def consume_queue4(self):
        # queue3 for elaborated data: Q-factor/Dissipation
        while not self._queue4.empty():
            self._queue_data4(self._queue4.get(False))    
           
    def consume_queue5(self):
        # queue3 for elaborated data: Temperature
        while not self._queue5.empty():
            self._queue_data5(self._queue5.get(False)) 
    
    def consume_queue6(self):
        # queue3 for elaborated data: errors
        while not self._queue6.empty():
            self._queue_data6(self._queue6.get(False))
            
    def consume_queue_F_multi(self): 
        # consume the parser queue until is empty
        while not self._queue_F_multi.empty():
            # get the data from the parser queue and put it in the circular buffer
            self._queue_data_F_multi(self._queue_F_multi.get(False))
        
    def consume_queue_D_multi(self):   
        while not self._queue_D_multi.empty():
            self._queue_data_D_multi(self._queue_D_multi.get(False))
        
    def _queue_data_F_multi(self, data):
        # Add values
        self._store_signal_values(data[1])
        self._store_signal_values_time (data[0])
        
    def _store_signal_values(self, values):
        # detect how many data are present to plot
        size = len(values)
        # store the data in respective buffers
        for idx in range(size):
            self._F_multi_buffer[idx].append(values[idx])
            # store the current array of frequency data 
            self._F_store[idx] = values[idx]
       
    def get_F_values_buffer(self, idx=0):
        """
        Gets the complete buffer for a line data, depending on specified index.
        :param idx: Index of the line data to get.
        :type idx: int.
        :return: float list.
        """
        return self._F_multi_buffer[idx].get_all()
    
    def _store_signal_values_time (self, values): 
        size = len(values)
        for idx in range(size):
            # append current time values
            self._time_buffer[idx].append(values[idx])
            # store the current array of time data
            self._time_store[idx] = values[idx]
            
    def get_time_values_buffer(self, idx = 0):
        # get all time buffer 
        return self._time_buffer[idx].get_all()
    
    def _queue_data_D_multi(self, data):
        # Add values
        self._store_signal_values_D(data[1])
        
    def _store_signal_values_D(self, values):
        # detect how many data are present to plot
        size = len(values)
        # store the data in respective buffers
        for idx in range(size):
            self._D_multi_buffer[idx].append(values[idx])
            # store the current array of dissipation  data 
            self._D_store[idx] = values[idx]
    
    def get_D_values_buffer(self, idx=0):
        """
        Gets the complete buffer for a line data, depending on specified index.
        :param idx: Index of the line data to get.
        :type idx: int.
        :return: float list.
        """
        return self._D_multi_buffer[idx].get_all()
    
    def consume_queue_A_multi(self):
        while not self._queue_A_multi.empty():
            self._queue_data_A_multi(self._queue_A_multi.get(False))
    
    def _queue_data_A_multi(self, data):
        # Add values
        self._store_signal_values_A (data[1])
        self._store_signal_values_F_sweep (data[0])
    
    def _store_signal_values_A (self, values):
        # detect how many data are present 
        size = len(values)
        # store the data in respective buffers
        for idx in range(size):
            self._A_multi_buffer[idx] = values[idx]
    
    def _store_signal_values_F_sweep (self, values):
        # detect how many data are present 
        size = len(values)
        # store the data in respective buffers
        for idx in range(size):
            self._F_Sweep_multi_buffer[idx] = values[idx]
            
            
    def get_A_values_buffer(self, idx=0): 
        return self._A_multi_buffer[idx]
    
    def consume_queue_P_multi(self):
        while not self._queue_P_multi.empty():
            self._queue_data_P_multi(self._queue_P_multi.get(False))
    
    def _queue_data_P_multi(self, data):
        # Add values
        self._store_signal_values_P (data[1])
        self._store_signal_values_F_sweep (data[0])
    
    def _store_signal_values_P (self, values):
        # detect how many data are present 
        size = len(values)
        # store the data in respective buffers
        for idx in range(size):
            self._P_multi_buffer[idx] = values[idx]
            
    def get_P_values_buffer(self, idx=0): 
        return self._P_multi_buffer[idx]
        
    
    def get_F_Sweep_values_buffer(self, idx = 0):
        
        return self._F_Sweep_multi_buffer[idx]
        # print (self._F_Sweep_multi_buffer[idx])
       
    ###########################################################################
    # Adds data to internal buffers.
    ###########################################################################    
    def _queue_data1(self,data):
        #:param data: values to add for serial data: amplitude :type data: float.
        self._data1_buffer = data
    
    #####    
    def _queue_data2(self,data):
        #:param data: values to add for serial data phase :type data: float.
        self._data2_buffer = data
    
    # FREQUENCY 
    def _queue_data3(self,data):
        #:param data: values to add for Resonance frequency :type data: float.
        self._t1_store = data[0] # time (unused)
        self._d1_store = data[1] # data
        self._t1_buffer.append(data[0])
        self._d1_buffer.append(data[1])
        self.frequency.emit(data[1])
        
    # DISSIPATION 
    def _queue_data4(self,data):
        # Additional function: exports processed data in a file if export box is checked.
        #:param data: values to add for Q-factor/dissipation :type data: float.
        self._t2_store = data[0] # time (unused)
        self._d2_store = data[1] # data
        self._t2_buffer.append(data[0])
        self._d2_buffer.append(data[1])
        self.dissipation.emit(data[1])
    
    # TEMPERATURE
    def _queue_data5(self,data):
        # Additional function: exports processed data in a file if export box is checked.
        #:param data: values to add for temperature :type data: float.
        self._t3_store = data[0] # time (unused)
        self._d3_store = data[1] # data 
        
        self._t3_buffer.append(data[0])
        self._d3_buffer.append(data[1])
        self.temperature.emit(data[1])

        # Ping progress signal
        self.progress.emit()
        
        # TODO datalog the time is now 
        # for storing relative time 
        if  self._flag and ~np.isnan(self._d3_store):
            # SINGLE 
            if self._source == SourceType.serial:
                self._timestart = time()
                
            # MULTI 
            elif self._source == SourceType.multiscan:
                epoch= datetime.datetime(1970, 1, 1, 0, 0) #offset-naive datetime
                ts_mult=1e6
                self._timestart = (int((datetime.datetime.now() - epoch).total_seconds()*ts_mult))
                
                # VER 0.1.3
                self.time_pre =  self._timestart
            
            self._flag = False
    
        #####
    def _queue_data6(self,data):
        #:param data: values to add for serial error :type data: float.
        self._ser_error1 = data[0]
        self._ser_error2 = data[1]
        self._control_k = data[2]
        self._ser_err_usb = data[3]
        try:
            self._overtone_number = data[4]

            # VER 0.2 
            # get TEC status 
            self._TEC_status = data[5]
        except IndexError:
            pass
        
    ###########################################################################
    # Gets data buffers for plot (Amplitude,Phase,Frequency and Dissipation) 
    ###########################################################################        
    def get_value1_buffer(self):
        #:return: float list.
        return self._data1_buffer
    
    #####
    def get_value2_buffer(self):
        #:return: float list.
        return self._data2_buffer

    # Frequency: get all frequency buffer 
    def get_d1_buffer(self):
        #:return: float list.
        return self._d1_buffer.get_all()
        
    ##### Gets time buffers
    def get_t1_buffer(self):
        #:return: float list.
        return self._t1_buffer.get_all()
    
    #####
    def get_d2_buffer(self):
        #:return: float list.
        return self._d2_buffer.get_all()
    
    ##### Gets time buffers
    def get_t2_buffer(self):
        #:return: float list.
        return self._t2_buffer.get_all()
    
    #####
    def get_d3_buffer(self):
        #:return: float list.
        return self._d3_buffer.get_all()
    
    ##### Gets time buffers
    def get_t3_buffer(self):
        #:return: float list.
        return self._t3_buffer.get_all()
    
    ##### Gets serial error
    def get_ser_error(self):
        """
        Returns: Error #1, Error #2, Control K, USB Error, Overtone Number Error
        """
        #:return: float list.
        return self._ser_error1,self._ser_error2, self._control_k, self._ser_err_usb, self._overtone_number
    
    # VER 0.1.3
    # get TEC status and pass the value to the main 
    def get_TEC_status(self): 
        return self._TEC_status
    
    # VER 0.1.4
    def get_time_elapsed (self):
        # print ("HELLO WORLD")
        return (self.time_elapsed)
    
    ###########################################################################
    # Checks if processes are running
    ###########################################################################
    def is_running(self):  
        return self._acquisition_process is not None and self._acquisition_process.is_alive()

    ###########################################################################
    # Gets the available ports for specified source
    ###########################################################################
    @staticmethod
    def get_source_ports(source):
        """
        :param source: Source to get available ports :type source: SourceType.
        :return: List of available ports :rtype: str list.
        """
        
        # SINGLE
        if source == SourceType.serial:
            print(TAG,'Port connected:',SerialProcess.get_ports())
            return SerialProcess.get_ports()
        # CALIBRATION
        elif source == SourceType.calibration:
            print(TAG,'Port connected:',CalibrationProcess.get_ports())
            return CalibrationProcess.get_ports()
        # MULTI 
        elif source == SourceType.multiscan:
            # TODO check get multiscan process serial port connected  
            # print (" WORKER get type of meas ")
            print(TAG,'Port connected:',MultiscanProcess.get_ports())
            return MultiscanProcess.get_ports()
        else:
            print(TAG,'Warning: unknown source selected')
            Log.w(TAG,"Unknown source selected")
            return None
        
        
    ###########################################################################
    # Gets the available speeds for specified source
    ###########################################################################
    @staticmethod
    def get_source_speeds(source):
        """
        :param source: Source to get available speeds :type source: SourceType.
        :return: List of available speeds :rtype: str list.
        """
        if source == SourceType.serial:
            return SerialProcess.get_speeds()
        
        elif source == SourceType.calibration:
            return CalibrationProcess.get_speeds()
        
        # multi 
        elif source == SourceType.multiscan:
            return MultiscanProcess.get_speeds()
        else:
            print(TAG,'Unknown source selected')
            Log.w(TAG, "Unknown source selected")
            return None
        
    
    ###########################################################################
    # Setup/Clear the internal buffers
    ###########################################################################
    def reset_buffers(self, samples):
        #:param samples: Number of samples for the buffers :type samples: int.
        
        # Initialises data buffers
        self._data1_buffer = np.zeros(samples) # amplitude
        self._data2_buffer = np.zeros(samples) # phase

        # Initialises supporting variables
        self._d1_store = 0
        self._d2_store = 0
        self._d3_store = 0
        self._t1_store = 0
        self._t2_store = 0
        self._t3_store = 0
        self._ser_error1 = 0
        self._ser_error2 = 0
        self._ser_err_usb= 0
        #self._control_k = 0
        
        self._d1_buffer = RingBuffer(Constants.ring_buffer_samples)  # Resonance frequency 
        self._d2_buffer = RingBuffer(Constants.ring_buffer_samples)  # Dissipation
        self._d3_buffer = RingBuffer(Constants.ring_buffer_samples)  # temperature
        self._t1_buffer = RingBuffer(Constants.ring_buffer_samples)  # time (Resonance frequency)
        self._t2_buffer = RingBuffer(Constants.ring_buffer_samples)  # time (Dissipation)
        self._t3_buffer = RingBuffer(Constants.ring_buffer_samples)  # time (temperature)
        
        # init frequency and dissipation array of ring buffer 
        self._F_multi_buffer = []
        self._D_multi_buffer = []
        self._time_buffer = []
        
        self._A_multi_buffer = []
        self._F_Sweep_multi_buffer = []
        
        # append ring buffer
        for _ in Constants.overtone_dummy:
            self._F_multi_buffer.append(RingBuffer(Constants.ring_buffer_samples))
            self._D_multi_buffer.append(RingBuffer(Constants.ring_buffer_samples))
            self._time_buffer.append(RingBuffer(Constants.ring_buffer_samples))

        self._A_multi_buffer = self._zerolistmaker(len(Constants.overtone_dummy))
        self._F_Sweep_multi_buffer = self._zerolistmaker(len(Constants.overtone_dummy))
        
        # INIT self._F_store and self._D_store list 
        # TODO IMPORTANT self._F_store and self._D_store same legth of self._F_multi_buffer and self._D_multi_buffer
        self._F_store = self._zerolistmaker(len(Constants.overtone_dummy))
        self._D_store = self._zerolistmaker(len(Constants.overtone_dummy))
        self._time_store = self._zerolistmaker(len(Constants.overtone_dummy))
        # self._time_buffer = self._zerolistmaker(len(Constants.overtone_dummy))
        
        # init a ring buffer of corresponding size 
        SAMPLING_TIME_DEFAULT = 7
        self.ring_buffer_len =  int(self._sampling_time/SAMPLING_TIME_DEFAULT)
        
        # VER 0.1.4
        # init the list of storedata averaging 
        self._F_store_buffer_averaging = self._zerolistmaker(len(Constants.overtone_dummy)) 
        self._D_store_buffer_averaging = self._zerolistmaker(len(Constants.overtone_dummy))
        self._T_store_buffer_averaging = self._zerolistmaker(len(Constants.overtone_dummy))
        
        # init frequency dissipation and temperature array of ring buffer 
        self._F_store_buffer = [] 
        self._D_store_buffer = [] 
        self._T_store_buffer = []

        for _ in Constants.overtone_dummy:
            self._F_store_buffer.append(RingBuffer(self.ring_buffer_len))
            self._D_store_buffer.append(RingBuffer(self.ring_buffer_len))
            self._T_store_buffer.append(RingBuffer(self.ring_buffer_len))

    ############################################################################
    # Gets frequency range
    ############################################################################
    
    def get_frequency_range(self):
        """
        :param samples: Number of samples for the buffers :type samples: int.
        :return: overtone :type overtone: float.
        :return: frequency range :type readFREQ: float list.
        """
        if self._source == SourceType.serial:
            return self._readFREQ
        
        elif self._source == SourceType.multiscan:
            return self._readFREQ
    
    def get_frequency_range_multi(self, samples, overtone):
        if self._source == SourceType.multiscan:
            readFREQ_out = self._acquisition_process.get_readFREQ(samples, overtone)
        return readFREQ_out
    
    ############################################################################
    # Gets overtones name, value and frequency step
    ############################################################################
    
    def get_overtone(self):
        """
        :param samples: Number of samples for the buffers :type samples: int.
        :return: overtone :type overtone: float.
        :return: frequency range :type readFREQ: float list.
        """
        return self._overtone_name,self._overtone_value, self._fStep
    
    def _load_frequencies_file(self):
            data  = loadtxt(Constants.cvs_peakfrequencies_path)
            peaks_mag = data[:,0]
            return peaks_mag
        
    def _zerolistmaker(self, n):
        listofzeros = [0] * n
        return listofzeros
    
