import multiprocessing
import os

from misc.constants import UNCERTAINTIES, Constants, Architecture, OSType

import serial
from serial.tools import list_ports
import numpy as np
import scipy.signal

from openqcm.processes.parser import ParserProcess

TAG = "Calibration"


###############################################################################
# Process for the serial package and the communication with the serial port
# Processes incoming data and calculates outgoing data by the algorithms
###############################################################################
class CalibrationProcess(multiprocessing.Process):

    ###########################################################################
    # BASELINE ESTIMATION
    # Estimates Baseline with Least Squares Polynomial Fit (LSP)
    ###########################################################################
    def baseline_estimation(self, x, y, poly_order):
        # Least Squares Polynomial Fit (LSP)
        coeffs = np.polyfit(x, y, poly_order)
        # Evaluate a polynomial at specific values
        poly_fitted = np.polyval(coeffs, x)
        return poly_fitted, coeffs

    ###########################################################################
    # BASELINE CORRECTION
    # estimates signal-baseline for amplitude and phase
    ###########################################################################
    def baseline_correction(self, readFREQ, data_mag, data_ph):

        # input signal Amplitude
        (self._polyfitted_all, self._coeffs_all) = self.baseline_estimation(
            readFREQ, data_mag, 8
        )
        self._mag_beseline_corrected_all = data_mag - self._polyfitted_all

        # input signal Phase
        (self._polyfitted_all_phase, self._coeffs_all_phase) = self.baseline_estimation(
            readFREQ, data_ph, 8
        )
        self._phase_beseline_corrected_all = data_ph - self._polyfitted_all_phase
        return self._mag_beseline_corrected_all, self._phase_beseline_corrected_all

    ###########################################################################
    # PEAK DETECTION
    # Calculates the relative extrema of data using Signal Processing Toolbox
    ###########################################################################
    def FindPeak(self, freq, mag, phase, dist):

        # freq vector of frequencies and mag and phase vectors of of values,
        # dist is minimal horizontal distance (dist>=1) in samples between neighbouring peaks.
        self.max_indexes_mag = scipy.signal.argrelextrema(
            np.array(mag), comparator=np.greater, order=dist
        )
        self.max_indexes_phase = scipy.signal.argrelextrema(
            np.array(phase), comparator=np.greater, order=dist
        )

        # local maxima amplitude
        self.max_freq_mag = freq[self.max_indexes_mag]
        self.max_value_mag = mag[self.max_indexes_mag]

        # local maxima phase
        self.max_freq_phase = freq[self.max_indexes_phase]
        self.max_value_phase = phase[self.max_indexes_phase]

        return (
            self.max_freq_mag,
            self.max_value_mag,
            self.max_freq_phase,
            self.max_value_phase,
        )

    ###########################################################################
    # Initializing values for process
    ###########################################################################
    def __init__(self, parser_process: ParserProcess):
        """
        :param parser_process: Reference to a ParserProcess instance.
        :type parser_process: ParserProcess.
        """
        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()

        # Instantiate a ParserProcess class for each communication channels
        self._parser1 = parser_process
        self._parser2 = parser_process
        self._parser5 = parser_process
        self._parser6 = parser_process
        self._serial = serial.Serial()

    ###########################################################################
    # Opens a specified serial port
    ###########################################################################
    def open(
        self,
        port,
        speed=Constants.serial_default_QCS,
        timeout=Constants.serial_timeout_ms,
        writeTimeout=Constants.serial_writetimeout_ms,
    ):
        """
        :param port: Serial port name :type port: str.
        :param speed: Baud rate, in bps, to connect to port :type speed: int.
        :param timeout: Sets current read timeout :type timeout: float (seconds).
        :param writetTimeout: Sets current write timeout :type writeTimeout: float (seconds).
        :return: True if the port is available :rtype: bool.
        """
        self._serial.port = port
        self._serial.baudrate = Constants.serial_default_speed  # 115200
        self._serial.stopbits = serial.STOPBITS_ONE
        self._serial.bytesize = serial.EIGHTBITS
        self._serial.timeout = timeout
        self._serial.writetimeout = writeTimeout
        self._QCStype = speed

        # Variable to process the exception
        # Checks QCStype to calibrate
        if self._QCStype == "5 MHz":
            self._QCStype_int = 0
        elif self._QCStype == "10 MHz":
            self._QCStype_int = 1

        print(TAG, "Selected Quartz Crystal Sensor:", self._QCStype)
        return self._is_port_available(self._serial.port)

    ###########################################################################
    # Reads the serial port,processes and adds all the data to internal queues
    ###########################################################################
    def run(self):
        """
        The expected format is a buffer (sweep) and a new buffer as a new sweep.
        The method parses data, converts each value to float and adds to a queue.
        If incoming data can't be converted to float,the data will be discarded.
        """
        # initializations
        self._polyfitted_all = None
        self._coeffs_all = None
        self._polyfitted_all_phase = None
        self._coeffs_all_phase = None
        self._mag_beseline_corrected_all = None
        self._phase_beseline_corrected_all = None
        self._flag = 0
        self._flag2 = 0

        # Checks if the serial port is currently connected
        if self._is_port_available(self._serial.port):

            # Sets start, stop, step and range frequencies
            readFREQ = Constants.calibration_readFREQ
            # Gets the state of the serial port
            if not self._serial.isOpen():
                # Opens the serial port
                self._serial.open()
                self._serial.flushInput()
                self._serial.flushOutput()
                # Initializes the sweep counter
                k = 0
                print(TAG, "Calibration Process Started")
                print(
                    TAG,
                    "The operation might take just over a minute to complete... please wait...",
                )
                #### SWEEPS LOOP ####
                # ----------------------------------------------------------
                temp1 = []
                temp2 = []
                # ----------------------------------------------------------
                while not self._exit.is_set():
                    # Boolean variable to process exceptions
                    self._flag = 0
                    self._flag2 = 0
                    fStep = Constants.calib_fStep  # 1000

                    # Sets start, stop, step and range frequencies
                    startFreq = (
                        Constants.calibration_frequency_start
                        + k * Constants.calib_fRange
                    )  # 5000000/10000000
                    stopFreq = startFreq + Constants.calib_fRange  # 5000000

                    samples = Constants.calib_samples  # 5001/10001
                    # data reset for new sweep
                    data_mag = np.linspace(0, 0, samples)
                    data_ph = np.linspace(0, 0, samples)

                    try:
                        # amplitude/phase convert bit to dB/Deg
                        vmax = 3.3
                        bitmax = 8192
                        ADCtoVolt = vmax / bitmax
                        VCP = 0.9

                        # WRITES encoded command to the serial port
                        cmd = (
                            str(startFreq)
                            + ";"
                            + str(stopFreq)
                            + ";"
                            + str(int(fStep))
                            + "\n"
                        )
                        self._serial.write(cmd.encode())

                        # Initializes buffer and strs
                        buffer = ""
                        strs = ["" for _ in range(samples + 2)]

                        # Initializes the progress bar
                        #################################################################################
                        # CHANGED v2.0
                        # INCREASED maxval=1000000 TO AVOID bar.update(len.buffer) BREAKS THE CALIBRATION
                        #################################################################################
                        # READS and decodes sweep from the serial port
                        while 1:
                            buffer += self._serial.read(
                                self._serial.inWaiting()
                            ).decode()  # Constants.app_encoding
                            if "s" in buffer:
                                break

                        #################################################################################
                        # CHANGED v2.0
                        # PRINT LEN BUFFER WHEN THE EOM is RECEIVED
                        #################################################################################

                        # from a full buffer to a list of string
                        data_raw = buffer.split("\n")
                        length = len(data_raw)

                        # PERFORMS split with the semicolon delimiter
                        for i in range(length):
                            strs[i] = data_raw[i].split(";")

                        # converts the sweep samples before adding to queue
                        for i in range(length - 2):
                            data_mag[i] = float(strs[i][0]) * ADCtoVolt / 2
                            data_mag[i] = (data_mag[i] - VCP) / 0.03
                            data_ph[i] = float(strs[i][1]) * ADCtoVolt / 1.5
                            data_ph[i] = (data_ph[i] - VCP) / 0.01

                        # ------------------------------
                        if k > 0:
                            data_mag = data_mag[1:]
                            data_ph = data_ph[1:]
                        temp1 = np.append(temp1, data_mag)
                        temp2 = np.append(temp2, data_ph)
                        # ------------------------------
                        print(
                            TAG,
                            "signal section #{}/{} acquired successfully\n".format(
                                k + 1, Constants.calib_sections
                            ),
                            end="\r",
                        )  # 10

                    # specify handlers for different exceptions
                    except ValueError:
                        print(TAG, "WARNING: ValueError during calibration!")
                        print(
                            TAG,
                            "Please, repeat the calibration after disconnecting/reconnecting device!",
                        )
                        self._flag = 1

                        #################################################################################
                        # CHANGED v2.0
                        # SERIAL FLUSH INPUT OUTPUT if an EXCEPTION OCCURR
                        #################################################################################
                        self._serial.flushInput()
                        self._serial.flushOutput()
                        self._serial.close()
                        self.stop()

                    except:
                        print(TAG, "WARNING: ValueError during calibration!")
                        print(
                            TAG,
                            "Please, repeat the calibration after disconnecting/reconnecting device!",
                        )
                        self._flag = 1

                        #################################################################################
                        # CHANGED v2.0
                        # SERIAL FLUSH INPUT OUTPUT if an EXCEPTION OCCURR
                        #################################################################################
                        self._serial.flushInput()
                        self._serial.flushOutput()
                        self._serial.close()
                        self.stop()

                    # --------------------------------
                    ## ADDS new serial data to internal queue
                    self._parser1.add1(temp1)
                    self._parser2.add2(temp2)
                    # --------------------------------
                    self._parser6.add6([self._flag, self._flag2, self._flag2, k])
                    k += 1
                    # STOPS acquiring data
                    if k == Constants.calib_sections:  # 10/5
                        self.stop()
                        break
                #### END SWEEPS LOOP ####
                #### STORING DATA TO FILE ###
                path = Constants.cvs_peakfrequencies_path
                # CHECKS QCM Sensor type for saving calibration
                if self._QCStype_int == 0:
                    distance = Constants.dist5
                    path_calib = Constants.csv_calibration_path
                    filename_calib = Constants.csv_calibration_filename  #
                elif self._QCStype_int == 1:
                    distance = Constants.dist10
                    path_calib = Constants.csv_calibration_path10
                    filename_calib = Constants.csv_calibration_filename10  #

                # CHECKS the exceptions
                if self._flag == 0:
                    # CALLS baseline_correction method
                    print(TAG, "Baseline Correction Process Started")
                    (data_mag_baseline, data_ph_baseline) = self.baseline_correction(
                        readFREQ, temp1, temp2
                    )
                    ## ADDS serial data (baseline corrected) to internal queue
                    self._parser1.add1(data_mag_baseline)
                    self._parser2.add2(data_ph_baseline)
                    print(TAG, "Baseline Correction Process Completed")
                    print(TAG, "Peak Detection Process Started")
                    print(TAG, "Finding peaks in acquired signals...")
                    try:
                        # CALLS FindPeak method
                        (max_freq_mag, _, max_freq_phase, _) = self.FindPeak(
                            readFREQ, temp1, temp2, dist=distance
                        )
                        print(
                            TAG,
                            "{} peaks were found at frequencies: {} Hz\n".format(
                                len(max_freq_mag), max_freq_mag
                            ),
                        )
                        if (
                            self._QCStype_int == 0
                            and (max_freq_mag[0] > 4e06 and max_freq_mag[0] < 6e06)
                        ) or (
                            self._QCStype_int == 1
                            and (max_freq_mag[0] > 9e06 and max_freq_mag[0] < 11e06)
                        ):
                            print(TAG, "Found the fundamental frequency!")
                        else:
                            print(
                                TAG, "WARNING: Could not find fundamential frequency!"
                            )
                            print(
                                TAG,
                                "Ideally, please repeat the calibration, or proceed with caution",
                            )
                            print(
                                TAG,
                                "Will attempt to find the fundamental frequency in the phase data",
                            )

                        print(TAG, "Current frequencies found:", max_freq_mag)
                        print(TAG, "Current frequencies phases found:", max_freq_phase)

                        # If list do not match in length, attempt to match
                        # TODO will need to fix this eventually
                        if len(max_freq_mag) < len(max_freq_phase):
                            temp_freq = []
                            print(TAG, "Attempting to match missing frequencies")
                            for i in range(len(max_freq_phase)):
                                found = False
                                for j in range(len(max_freq_mag)):
                                    # Found Match
                                    if max_freq_mag[j] < max_freq_phase[i] * (
                                        1 + UNCERTAINTIES
                                    ) and max_freq_mag[j] > max_freq_phase[i] * (
                                        1 - UNCERTAINTIES
                                    ):
                                        temp_freq.append(max_freq_mag[j])
                                        found = True
                                        break

                                    # If too big, assume none
                                    elif (
                                        max_freq_phase[i] * (1 + UNCERTAINTIES)
                                        < max_freq_mag[j]
                                    ):
                                        temp_freq.append(max_freq_phase[i])
                                        found = True
                                        break

                                # If still not found, just add
                                if not found:
                                    temp_freq.append(max_freq_phase[i])

                            print(TAG, "Newly discovered frequencies:", temp_freq)
                            max_freq_mag = np.array(temp_freq)

                        if (
                            self._QCStype_int == 0
                            and (max_freq_mag[0] > 4e06 and max_freq_mag[0] < 6e06)
                        ) or (
                            self._QCStype_int == 1
                            and (max_freq_mag[0] > 9e06 and max_freq_mag[0] < 11e06)
                        ):
                            print(TAG, "Found the fundamental frequency in the phase !")
                        else:
                            print(
                                TAG,
                                "WARNING: Error during peak detection, could not find fundamential frequency in the phase.",
                            )
                            print(TAG, "Please, repeat the calibration!")
                            raise Exception()

                        # SAVES independently of the state of the export box
                        print(TAG, "Saving data in file...")
                        np.savetxt(
                            path, np.column_stack([max_freq_mag, max_freq_phase])
                        )
                        print(
                            TAG,
                            "Peak frequencies for {} saved in: {}".format(
                                self._QCStype, path
                            ),
                        )

                        # Creates a directory if the specified path doesn't exist
                        dir_name = os.path.dirname(path).strip()
                        if not os.path.isdir(dir_name):
                            os.makedirs(dir_name, exist_ok=True)

                        # creates TXT file
                        np.savetxt(str("{}{}{}.{}".format(dir_name, Constants.slash, filename_calib, Constants.txt_extension)), np.column_stack([readFREQ, temp1, temp2]))

                        print(
                            TAG,
                            "Calibration for {} saved in: {}".format(
                                self._QCStype, path_calib
                            ),
                        )

                    except:
                        print(
                            TAG,
                            "WARNING: Outed. Error during peak detection, incompatible peaks number or frequencies!",
                        )
                        print(TAG, "Please, repeat the calibration!")
                        self._flag2 = 1

                if self._flag == 0 and self._flag2 == 0:
                    print(TAG, "Calibration success for baseline correction!")

                # ADDS error flags to internal queue
                self._parser5.add5([self._flag, self._flag2])
                #### CLOSES serial port ####
                self._serial.close()

    ###########################################################################
    # Stops acquiring data
    ###########################################################################
    def stop(self):
        # Signals the process to stop acquiring data.
        self._exit.set()

    ###########################################################################
    # Automatically selects the serial ports for Teensy (macox/windows)
    ###########################################################################
    @staticmethod
    def get_ports():
        if Architecture.get_os() is OSType.macosx:
            import glob

            return glob.glob("/dev/tty.usbmodem*")
        elif Architecture.get_os() is OSType.linux:
            import glob

            return glob.glob("/dev/ttyACM*")
        else:
            found_ports = []
            port_connected = []
            found = False
            ports_avaiable = list(list_ports.comports())
            for port in ports_avaiable:
                if port[2].startswith("USB VID:PID=16C0:0483"):
                    found = True
                    port_connected.append(port[0])
            if found:
                found_ports = port_connected
            return found_ports

    ###########################################################################
    # Gets a list of the common serial baud rates, in bps (only 115200 used)
    ###########################################################################
    @staticmethod
    def get_speeds():
        #:return: List of the common baud rates, in bps :rtype: str list.
        return [str(v) for v in ["10 MHz", "5 MHz"]]

    ###########################################################################
    # Checks if the serial port is currently connected
    ###########################################################################
    def _is_port_available(self, port):
        """
        :param port: Port name to be verified.
        :return: True if the port is connected to the host :rtype: bool.
        """
        for p in self.get_ports():
            if p == port:
                return True
        return False
