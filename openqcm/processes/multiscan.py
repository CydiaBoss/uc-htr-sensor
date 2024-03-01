import multiprocessing

from misc.constants import Constants, Architecture, OSType
from misc.logger import Logger as Log

from openqcm.core.ring_buffer import RingBuffer
from openqcm.common.file_storage import FileStorage

from time import time, sleep
import serial
from serial.tools import list_ports
import numpy as np
from numpy import loadtxt
from scipy.interpolate import UnivariateSpline

from math import factorial

from openqcm.processes.parser import ParserProcess

TAG = "Multiscan"


class MultiscanProcess(multiprocessing.Process):

    # BASELINE CORRECTION
    def baseline_correction(self, x, y, poly_order):

        # Estimate Baseline with Least Squares Polynomial Fit (LSP)
        coeffs = np.polyfit(x, y, poly_order)
        # Evaluate a polynomial at specific values
        poly_fitted = np.polyval(coeffs, x)
        return poly_fitted, coeffs

    # BASELINE COEFFICIENTS
    def baseline_coeffs(self):

        # initializations
        self.polyfitted_all = None
        self.coeffs_all = None
        self.polyfitted_all_phase = None
        self.coeffs_all_phase = None

        # loads Calibration (baseline correction) from file
        (self.freq_all, self.mag_all, self.phase_all) = self.load_calibration_file()

        # Baseline correction: input signal Amplitude (sweep all frequencies)
        (self.polyfitted_all, self.coeffs_all) = self.baseline_correction(
            self.freq_all, self.mag_all, 8
        )
        self.mag_beseline_corrected_all = self.mag_all - self.polyfitted_all

        # Baseline correction: input signal Phase (sweep all frequencies)
        (self.polyfitted_all_phase, self.coeffs_all_phase) = self.baseline_correction(
            self.freq_all, self.phase_all, 8
        )
        self.phase_beseline_corrected_all = self.phase_all - self.polyfitted_all_phase
        return self.coeffs_all

    # SAVITZKY - GOLAY FOLTER
    def savitzky_golay(self, y, window_size, order, deriv=0, rate=1):
        """Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
        The Savitzky-Golay filter removes high frequency noise from data.
        It has the advantage of preserving the original shape and
        features of the signal better than other types of filtering
        approaches, such as moving averages techniques.
        Parameters
        ----------
        y : array_like, shape (N,) the values of the time history of the signal.
        window_size : int the length of the window. Must be an odd integer number.
        order : int the order of the polynomial used in the filtering.
                Must be less then `window_size` - 1.
        deriv: int the order of the derivative to compute (default = 0 means only smoothing)
        Returns
        -------
        ys : ndarray, shape (N) the smoothed signal (or it's n-th derivative).
        Notes
        -----
        The Savitzky-Golay is a type of low-pass filter, particularly
        suited for smoothing noisy data. The main idea behind this
        approach is to make for each point a least-square fit with a
        polynomial of high order over a odd-sized window centered at
        the point.
        Examples
        --------
        t = np.linspace(-4, 4, 500)
        y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
        ysg = savitzky_golay(y, window_size=31, order=4)
        import matplotlib.pyplot as plt
        plt.plot(t, y, label='Noisy signal')
        plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
        plt.plot(t, ysg, 'r', label='Filtered signal')
        plt.legend()
        plt.show()
        References
        ----------
        .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
           Data by Simplified Least Squares Procedures. Analytical
           Chemistry, 1964, 36 (8), pp 1627-1639.
        .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
           W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
           Cambridge University Press ISBN-13: 9780521880688
        """
        try:
            window_size = np.abs(int(window_size))
            order = np.abs(int(order))
        except ValueError as msg:
            raise ValueError("WARNING: window size and order have to be of type int!")
        if window_size % 2 != 1 or window_size < 1:
            raise TypeError("WARNING: window size must be a positive odd number!")
        if window_size < order + 2:
            raise TypeError(
                "WARNING: window size is too small for the polynomials order!"
            )
        order_range = range(order + 1)
        half_window = (window_size - 1) // 2
        # precompute coefficients
        b = np.mat(
            [[k**i for i in order_range] for k in range(-half_window, half_window + 1)]
        )
        m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
        # pad the signal at the extremes with values taken from the signal itself
        firstvals = y[0] - np.abs(y[1 : half_window + 1][::-1] - y[0])
        lastvals = y[-1] + np.abs(y[-half_window - 1 : -1][::-1] - y[-1])
        y = np.concatenate((firstvals, y, lastvals))
        return np.convolve(m[::-1], y, mode="valid")

    ###########################################################################
    # Resonance Frequency, Resonance Peak, Bandwidth and Q-factor/Dissipation
    ###########################################################################
    def parameters_finder(self, freq, signal, overtone_number, threshold):

        f_max = np.max(signal)  # Find maximum
        i_max = np.argmax(signal, axis=0)  # Find index of maximum

        # setup the index for finding the leading edge
        index_m = i_max

        # VER 0.1.3
        if overtone_number == 0:

            # loop until the index at FWHM/others is found
            # VER 0.1.4 find the index for the bandwidth
            while signal[index_m] > (f_max - threshold):
                if index_m < 1:
                    print(TAG, "WARNING: Left value not found")
                    self._err1 = 1
                    break
                index_m = index_m - 1
            # linearly interpolate between the previous values to find the value of freq at the leading edge
            m = (signal[index_m + 1] - signal[index_m]) / (
                freq[index_m + 1] - freq[index_m]
            )
            c = signal[index_m] - freq[index_m] * m
            # VER 0.1.4 find the left index for the bandwidth
            i_leading = (f_max - threshold - c) / m

            # setup index for finding the trailing edge
            index_M = i_max

            # loop until the index at FWHM/others is found
            # VER 0.1.4 find the index for the badwidth
            while signal[index_M] > (f_max - threshold):
                if index_M >= len(signal) - 1:
                    print(TAG, "WARNING: Right value not found")
                    self._err2 = 1
                    break
                index_M = index_M + 1

            # linearly interpolate between the previous values to find the value of freq at the trailing edge
            m = (signal[index_M - 1] - signal[index_M]) / (
                freq[index_M - 1] - freq[index_M]
            )
            c = signal[index_M] - freq[index_M] * m
            # VER 0.1.4 find the right index for the bandwidth
            i_trailing = (f_max - threshold - c) / m

            bandwidth = abs(i_trailing - i_leading)

        else:
            # loop until the index at FWHM/others is found
            # VER 0.1.4 find the index for the bandwidth
            while signal[index_m] > (f_max - threshold):
                if index_m < 1:
                    print(TAG, "WARNING: Left value not found")
                    self._err1 = 1
                    break
                index_m = index_m - 1
            # linearly interpolate between the previous values to find the value of freq at the leading edge
            m = (signal[index_m + 1] - signal[index_m]) / (
                freq[index_m + 1] - freq[index_m]
            )
            c = signal[index_m] - freq[index_m] * m
            # VER 0.1.4 find the left index for the bandwidth
            i_leading = (f_max - threshold - c) / m

            # setup index for finding the trailing edge
            index_M = i_max

            # loop until the index at FWHM/others is found
            # VER 0.1.4 find the index for the badwidth
            while signal[index_M] > f_max - threshold:
                if index_M >= len(signal) - 1:
                    print(TAG, "WARNING: Right value not found")
                    self._err2 = 1
                    break
                index_M = index_M + 1

            # linearly interpolate between the previous values to find the value of freq at the trailing edge
            m = (signal[index_M - 1] - signal[index_M]) / (
                freq[index_M - 1] - freq[index_M]
            )
            c = signal[index_M] - freq[index_M] * m
            # VER 0.1.4 find the right index for the bandwidth
            i_trailing = (f_max - threshold - c) / m

            bandwidth = abs(i_trailing - i_leading)

        # VER 0.1.3
        # frequency and dissipation at fundamental
        if overtone_number == 0:

            freq_resonance = freq[i_max]
            Qfac = bandwidth

        # VER 0.1.3
        # frequency and dissipation at overtones
        else:
            # VER 0.1.4 resonance frequency as the peak
            freq_resonance = freq[i_max]
            # VER 0.1.4
            Qfac = bandwidth

        # VER 0.1.4 changed the return of the method introducing resonance frequency
        return i_max, f_max, bandwidth, index_m, index_M, Qfac, freq_resonance

    # ELABORATE SIGNAL
    # -------------------------------------------------------------------------
    def elaborate_multi(
        self,
        k,
        overtone_number,
        coeffs_all,
        readFREQ,
        samples,
        Xm,
        Xp,
        temperature,
        SG_window_size,
        Spline_points,
        Spline_factor,
        timestamp,
    ):

        # Number of spline points
        points = Spline_points
        # sweep counter
        self._k = k
        # current overtones number
        self._overtone_number = overtone_number
        # evaluated polynomial coefficients
        self._coeffs_all = coeffs_all
        # frequency range, samples number
        self._readFREQ = readFREQ
        self._samples = samples
        # support vectors
        self._Xm = Xm
        self._Xp = Xp
        self._filtered_mag = np.zeros(samples)
        # save current data
        mag = self._Xm
        phase = self._Xp

        # Initializations of support vectors for later storage
        self._Xm = np.linspace(0, 0, self._samples)
        self._Xp = np.linspace(0, 0, self._samples)

        # Evaluate a polynomial at specific values based on the coefficients and frequency range
        self._polyfitted = np.polyval(self._coeffs_all, self._readFREQ)

        # BASELINE CORRECTION ROI (raw data)
        mag_beseline_corrected = mag - self._polyfitted

        # FILTERING - Savitzky-Golay
        filtered_mag = self.savitzky_golay(
            mag_beseline_corrected, window_size=SG_window_size, order=Constants.SG_order
        )

        # FITTING/INTERPOLATING - SPLINE
        xrange = range(len(filtered_mag))
        freq_range = np.linspace(self._readFREQ[0], self._readFREQ[-1], points)
        s = UnivariateSpline(xrange, filtered_mag, s=Spline_factor)
        xs = np.linspace(0, len(filtered_mag) - 1, points)
        mag_result_fit = s(xs)

        # VER 0.1.4 chenge the bandwith threshold value to the constant value THRESHOLD_DB = 0.3
        (index_peak_fit, _, _, _, _, Qfac_fit, frequency_resonance) = (
            self.parameters_finder(
                freq_range, mag_result_fit, overtone_number, Constants.THRESHOLD_DB
            )
        )

        # self._my_list_f[overtone_number].append( freq_range[int(index_peak_fit)] )
        # VER 0.1.4
        # change the dissipation calculation as the inverse of the bandwidth defined above in parameter finder
        self._my_list_f[overtone_number].append(frequency_resonance)
        self._my_list_d[overtone_number].append((Qfac_fit / 1000000))

        # self._temperature_buffer.append(temperature)
        self._temperature_buffer_0.append(temperature)

        if self._k >= self._environment:
            # FREQUENCY
            self._vec_app1[overtone_number] = self.savitzky_golay(
                self._my_list_f[overtone_number].get_all(),
                window_size=Constants.SG_window_environment,
                order=Constants.SG_order_environment,
            )

            self._freq_range_mean[overtone_number] = np.average(
                self._vec_app1[overtone_number]
            )

            # DISSIPATION
            self._vec_app1d[overtone_number] = self.savitzky_golay(
                self._my_list_d[overtone_number].get_all(),
                window_size=Constants.SG_window_environment,
                order=Constants.SG_order_environment,
            )
            # Insert a median
            self._diss_mean[overtone_number] = np.average(
                self._vec_app1d[overtone_number]
            )

            # TEMPERATURE
            if overtone_number == 0:
                self._vec_app1t = self.savitzky_golay(
                    self._temperature_buffer_0.get_all(),
                    window_size=Constants.SG_window_environment,
                    order=Constants.SG_order_environment,
                )
                self._temperature_mean = np.average(self._vec_app1t)

        #  VER 0.2 BETA
        # set the current value of resonance frequecy at specific overtone
        if self._k <= self._environment:
            # current value is raw
            self.freq_res_current_array[overtone_number] = freq_range[
                int(index_peak_fit)
            ]
        else:
            # current value as average
            self.freq_res_current_array[overtone_number] = int(
                self._freq_range_mean[overtone_number]
            )

        # TIME EPOCH
        # ---------------------------------------------------------------------
        w = time() - timestamp

        # TODO the Time is now and it is hard
        if overtone_number == 0:
            self._my_time = w
        # ---------------------------------------------------------------------

        # time array for each harmonic
        self._my_time_array[overtone_number] = w

        # AMPLITUDE
        self._parser1.add1(filtered_mag)
        # PHASE
        self._parser2.add2(phase)

        # Adds "fake" frequency, dissipation and temperature meaan to parser queues
        self._parser3.add3([self._my_time, 0])
        self._parser4.add4([self._my_time, 0])
        self._parser5.add5([self._my_time, self._temperature_mean])

        # add multi overtone frequency - dissipation and correpsonding time array to the parser queues
        self._parser_F_multi.add_F_multi([self._my_time_array, self._freq_range_mean])
        self._parser_D_multi.add_D_multi([self._my_time_array, self._diss_mean])

    def elaborate_ampli_phase_multi(
        self, overtone_index, poly_coeff, freq_sweep, amp_sweep, phase_sweep
    ):

        # calculate polynomial at frequency sweep points
        amp_baseline = np.polyval(poly_coeff, freq_sweep)

        self._my_list_amp[overtone_index] = (amp_sweep - amp_baseline).tolist()

        self._my_list_phase[overtone_index] = phase_sweep.tolist()
        self._my_list_freq[overtone_index] = freq_sweep.tolist()

        # add to new parser
        self._parser_A_multi.add_A_multi([self._my_list_freq, self._my_list_amp])
        self._parser_P_multi.add_P_multi([self._my_list_freq, self._my_list_phase])

    # INIT PROCESS
    # -------------------------------------------------------------------------
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
        self._parser3 = parser_process
        self._parser4 = parser_process
        self._parser5 = parser_process
        # parser process for sweep info nd utility error
        self._parser6 = parser_process

        self._dummy = True

        self.temperature_set_old = 0
        self.cycling_time_set_old = 0
        self.P_share_set_old = 0
        self.I_share_set_old = 0
        self.D_share_set_old = 0

        # DEV
        # control temperature switch default value
        self.ctrl_bool_pre = 0

        # Frequency
        self._parser_F_multi = parser_process
        # Dissipation
        self._parser_D_multi = parser_process
        # Amplitude
        self._parser_A_multi = parser_process
        # Phase
        self._parser_P_multi = parser_process

        # serial process
        self._serial = serial.Serial()

        # self.temperature_set_old = loadtxt(Constants.manual_frequencies_path)

        # init ring buffer for each harmonic
        self._environment = Constants.environment
        self._frequency_buffer_0 = RingBuffer(self._environment)
        self._dissipation_buffer_0 = RingBuffer(self._environment)
        self._temperature_buffer_0 = RingBuffer(self._environment)
        self._frequency_buffer_1 = RingBuffer(self._environment)
        self._dissipation_buffer_1 = RingBuffer(self._environment)
        self._temperature_buffer_1 = RingBuffer(self._environment)
        self._frequency_buffer_2 = RingBuffer(self._environment)
        self._dissipation_buffer_2 = RingBuffer(self._environment)
        self._temperature_buffer_2 = RingBuffer(self._environment)
        self._frequency_buffer_3 = RingBuffer(self._environment)
        self._dissipation_buffer_3 = RingBuffer(self._environment)
        self._temperature_buffer_3 = RingBuffer(self._environment)
        # TODO 5M
        self._frequency_buffer_4 = RingBuffer(self._environment)
        self._dissipation_buffer_4 = RingBuffer(self._environment)
        self._temperature_buffer_4 = RingBuffer(self._environment)

        self._frequency_buffer_0_a = RingBuffer(self._environment)
        self._frequency_buffer_1_a = RingBuffer(self._environment)
        self._frequency_buffer_2_a = RingBuffer(self._environment)
        self._frequency_buffer_3_a = RingBuffer(self._environment)
        self._frequency_buffer_4_a = RingBuffer(self._environment)

        # init frequency dissipation list of ring buffer
        self._my_list_f = [
            self._frequency_buffer_0,
            self._frequency_buffer_1,
            self._frequency_buffer_2,
            self._frequency_buffer_3,
            self._frequency_buffer_4,
        ]
        # VER 0.1.4
        self._my_list_f_a = [
            self._frequency_buffer_0_a,
            self._frequency_buffer_1_a,
            self._frequency_buffer_2_a,
            self._frequency_buffer_3_a,
            self._frequency_buffer_4_a,
        ]

        self._my_list_d = [
            self._dissipation_buffer_0,
            self._dissipation_buffer_1,
            self._dissipation_buffer_2,
            self._dissipation_buffer_3,
            self._dissipation_buffer_4,
        ]

        # TODO IMPORTANT chenge the init of array
        # TODO 5M modified the number of items in the array below

        # init array for frequency, dissipation and temperature
        self._vec_app1 = [0, 0, 0, 0, 0]
        self._freq_range_mean = [0, 0, 0, 0, 0]

        self._vec_app1d = [0, 0, 0, 0, 0]
        self._diss_mean = [0, 0, 0, 0, 0]

        self._my_time = 0
        self._my_time_array = [0, 0, 0, 0, 0]

        # init amplitude, phase frequency sweep buffer for each harmonic
        # fundamental
        self._amp_sweep_0 = None
        self._phase_sweep_0 = None
        self._freq_sweep_0 = None
        # 3rd overtone
        self._amp_sweep_1 = None
        self._phase_sweep_1 = None
        self._freq_sweep_1 = None
        # 5th overtone
        self._amp_sweep_2 = None
        self._phase_sweep_2 = None
        self._freq_sweep_2 = None
        # 7th ovetone
        self._amp_sweep_3 = None
        self._phase_sweep_3 = None
        self._freq_sweep_3 = None
        # 9th overtone
        self._amp_sweep_4 = None
        self._phase_sweep_4 = None
        self._freq_sweep_4 = None

        # init amplitude, phase and frequency list of buffer
        self._my_list_amp = [
            self._amp_sweep_0,
            self._amp_sweep_1,
            self._amp_sweep_2,
            self._amp_sweep_3,
            self._amp_sweep_4,
        ]
        self._my_list_phase = [
            self._phase_sweep_0,
            self._phase_sweep_1,
            self._phase_sweep_2,
            self._phase_sweep_3,
            self._phase_sweep_4,
        ]
        self._my_list_freq = [
            self._freq_sweep_0,
            self._freq_sweep_1,
            self._freq_sweep_2,
            self._freq_sweep_3,
            self._freq_sweep_4,
        ]

        # DEBUG_0.1.1a
        # byte available at port
        self.byte_at_port = 0
        # DEBUG_0.1.1a
        # a boolean variable to check timeout at serial port and brek the for
        self.TIME_OUT = 0

        # VER 0.1.4
        # init TEC controller status variable
        self._data_status = 0

        # VER 0.1.5
        # init TEC error register bit
        self._error_register_bit = 0

        # VER 0.1.4
        # current values of resonance frequency array
        self.freq_res_current_array = [None, None, None, None, None]
        # just another dummy counter
        self._just_another_counter = 0

    # SERIAL PORT OPEN and general setting
    # -------------------------------------------------------------------------
    def open(
        self,
        port,
        speed=Constants.serial_default_speed,
        timeout=Constants.serial_timeout_ms,
        writeTimeout=Constants.serial_writetimeout_ms,
    ):
        """
        :param port: Serial port name :type port: str.
        :param timeout: Sets current read timeout :type timeout: float (seconds).
        :param writetTimeout: Sets current write timeout :type writeTimeout: float (seconds).
        :return: True if the port is available :rtype: bool.
        """
        self._serial.port = port
        self._serial.baudrate = Constants.serial_default_speed
        self._serial.stopbits = serial.STOPBITS_ONE
        self._serial.bytesize = serial.EIGHTBITS
        self._serial.timeout = timeout
        self._serial.writetimeout = writeTimeout

        # Loads frequencies from file
        peaks_mag = self.load_frequencies_file()

        # ---------------------------------------------------------------------
        # Set to fundamental peak
        self._overtone = peaks_mag[0]
        self._overtone_int = 0
        # ---------------------------------------------------------------------

        return self._is_port_available(self._serial.port)

    # RUN PROCESS
    # -------------------------------------------------------------------------
    def run(self):
        """
        The expected format is a buffer (sweep) and a new buffer as a new sweep.
        The method parses data, converts each value to float and adds to a queue.
        If incoming data can't be converted to float,the data will be discarded.
        """

        # init error and flag parameters
        self._flag_error = 0
        self._flag_error_usb = 0
        self._err1 = 0
        self._err2 = 0

        # init frequency sweep and data process param
        startF = []
        stopF = []
        stepF = []
        readF = []
        sg_window_size = []
        spline_factor = []
        spline_points = []

        # get baseline coefficient
        coeffs_all = self.baseline_coeffs()

        # set initial values of sweep buffer
        for nn in Constants.overtone_dummy:
            self._my_list_amp[nn] = self._zerolistmaker(Constants.SAMPLES)
            self._my_list_phase[nn] = self._zerolistmaker(Constants.SAMPLES)
            self._my_list_freq[nn] = self._zerolistmaker(Constants.SAMPLES)

        # Checks if the serial port is currently connected
        if self._is_port_available(self._serial.port):

            # get the number of samples
            samples = Constants.argument_default_samples

            # TODO get the number of overtones in the peak frequencies file
            frequencies_file = self.load_frequencies_file()

            # Get array sweep paramaters
            (
                startF,
                stopF,
                stepF,
                readF,
                sg_window_size,
                spline_factor,
                spline_points,
            ) = self.get_frequencies(samples)

            # Gets the state of the serial port
            if not self._serial.isOpen():

                # open the serial port
                # -------------------------------------------------------------
                self._serial.open()

                # Initializes the sweep counter
                k = 0
                print(TAG, " Buffering and processing early raw data...")

                # creates a timestamp
                timestamp = time()

                # init frequency, dissipation and temperature ring buffer
                self._environment = Constants.environment
                self._frequency_buffer = RingBuffer(self._environment)
                self._dissipation_buffer = RingBuffer(self._environment)
                self._temperature_buffer = RingBuffer(self._environment)

                # ACQUISITION LOOP
                # -------------------------------------------------------------
                while not self._exit.is_set():
                    # VER 0.1.4
                    # get resonance frequencies in acquisition loop.
                    # get and set sweep start, stop and set frequencies sweep parameters, as function of the number of samples
                    # Get array sweep paramaters from frequency peaks file
                    (
                        startF,
                        stopF,
                        stepF,
                        readF,
                        sg_window_size,
                        spline_factor,
                        spline_points,
                    ) = self.get_frequencies(samples)

                    # else:
                    #     # Get array sweep paramaters from the real time frequency peaks file
                    #     (startF, stopF, stepF, readF,
                    #      sg_window_size, spline_factor, spline_points) = self.get_frequencies_RT(samples)

                    # data reset for new sweep
                    data_mag = np.linspace(0, 0, samples)
                    data_ph = np.linspace(0, 0, samples)

                    # DEV RAWDATA SAVE RAW SWEEP DATA
                    # init frequency sweep raw array
                    data_f = np.linspace(0, 0, samples)

                    overtone_index = 0
                    self._boolean_buffer_length = 0

                    # cycle on all overtones
                    for overtone_index in range(len(frequencies_file)):

                        try:
                            # amplitude/phase convert bit to dB/Deg parameters
                            vmax = 3.3
                            bitmax = 8192
                            ADCtoVolt = vmax / bitmax
                            VCP = 0.9

                            # DEBUG_0.1.1a
                            # get swepp time start
                            timeStart = time()

                            # -------------------------------------------------
                            # START SWEEP

                            # WRITE SWEEP COMMAND MESSAGE TO SERIAL PORT
                            # -------------------------------------------------
                            cmd = (
                                str(startF[overtone_index])
                                + ";"
                                + str(stopF[overtone_index])
                                + ";"
                                + str(int(stepF[overtone_index]))
                                + "\n"
                            )
                            self._serial.write(cmd.encode())

                            # DEBUG_0.1.1a
                            # added a short sleep before read serial
                            sleep(Constants.WRITE_SERIAL_WAIT)

                            # Initializes buffer and strs record
                            buffer = ""
                            strs = ["" for _ in range(samples + 2)]

                        except:
                            Log.e(TAG, "Info: exception serial write fail")
                            self._flag_error_usb = 1

                        # Declare all variables
                        data_temp = 0.0

                        if self._flag_error_usb == 0:
                            try:

                                # READ SWEEP DATA AT SERIAL PORT
                                # -------------------------------------------------
                                while 1:
                                    # append string read at serial port to buffer

                                    # DEBUG_0.1.1a
                                    self.byte_at_port = self._serial.inWaiting()
                                    buffer += self._serial.read(
                                        self.byte_at_port
                                    ).decode(Constants.app_encoding)

                                    # check the time elapsed in serial read loop
                                    _time_elapsed = time() - timeStart

                                    # check for EOM character
                                    if "s" in buffer:
                                        # VER 0.1.4
                                        # add a little delay at the end of the sweep
                                        print(cmd)
                                        sleep(Constants.SLEEP_EOM_MULTISCAN)

                                        break

                                    # DEBUG_0.1.1a
                                    # insert a timeout in while acquisition loop to prevent freezing
                                    if _time_elapsed > Constants.TIME_ELAPSED_TIMEOUT:
                                        # DEBUG_0.1.1a
                                        print(
                                            TAG,
                                            "Info: timeout at overtone index = ",
                                            overtone_index,
                                            end="\n",
                                        )
                                        self._flag_error_usb = 1
                                        self.TIME_OUT = 1
                                        # exit the while loop
                                        break

                                if self.TIME_OUT == 1:
                                    # DEBUG_0.1.1a
                                    # break the for ?
                                    self.TIME_OUT = 0
                                    sleep(0.5)
                                    # reset serial input/output buffer
                                    self._serial.reset_input_buffer()
                                    self._serial.reset_output_buffer()
                                    sleep(0.5)
                                    self._flag_error_usb = 1

                                    # exit the for loop to prevent overtone mixing
                                    break

                                # STOP SWEEP
                                # -----------------------------------------

                                if self._flag_error_usb == 0:
                                    # split each line
                                    data_raw = buffer.split("\n")
                                    length = len(data_raw)

                                    #  check the length of the serial read buffer if exceed the number of samples = 500
                                    if length > Constants.argument_default_samples + 2:
                                        print(
                                            TAG,
                                            "Info: exceed read buffer length = ",
                                            length,
                                            end="\n",
                                        )
                                        self._flag_error_usb = 1
                                        data_mag = np.linspace(0, 0, samples)
                                        data_ph = np.linspace(0, 0, samples)
                                        # reset data raw
                                        data_raw = ""
                                        # reset buffer
                                        buffer = ""

                                        # reset serial input/output buffer
                                        sleep(0.5)
                                        self._serial.reset_input_buffer()
                                        self._serial.reset_output_buffer()
                                        sleep(0.5)
                                        self._flag_error_usb = 1
                                        print(
                                            TAG,
                                            "Info: current overtone index = ",
                                            overtone_index,
                                            end="\n",
                                        )
                                        # break

                                    elif (
                                        length < Constants.argument_default_samples + 2
                                    ):
                                        # split data via semicolon ";"
                                        for i in range(length):
                                            strs[i] = data_raw[i].split(";")

                                        # converts data values to gain and phase
                                        for i in range(length - 1):
                                            data_mag[i] = (
                                                float(strs[i][0]) * ADCtoVolt / 2
                                            )
                                            data_mag[i] = (data_mag[i] - VCP) / 0.03
                                            data_ph[i] = (
                                                float(strs[i][1]) * ADCtoVolt / 1.5
                                            )
                                            data_ph[i] = (data_ph[i] - VCP) / 0.01

                                        # --------------------------------------------------------------------------
                                        # DEV RAWDATA  SAVE RAW SWEEP DATA
                                        # --------------------------------------------------------------------------
                                        # build the frequency data array
                                        for i in range(length - 1):
                                            data_f[i] = (
                                                startF[overtone_index]
                                                + i * stepF[overtone_index]
                                            )

                                        # DEV RAWDATA check the OS
                                        if Architecture.get_os() is (
                                            OSType.linux or OSType.macosx
                                        ):
                                            # print ("MAC_OS_X")
                                            slash = "/"

                                        elif Architecture.get_os() is OSType.windows:
                                            # print("WINDOWS")
                                            slash = "\\"
                                        else:
                                            # print ("OTHER_OS")
                                            slash = "/"

                                        FileStorage.TXT_sweeps_save(
                                            (overtone_index * 2) + 1,
                                            str("openQCM")
                                            + slash
                                            + Constants.sweep_export_path,
                                            data_f,
                                            data_mag,
                                            data_ph,
                                        )

                                        # get the temperature value from the buffer
                                        data_temp = float((strs[length - 1][0]))

                                        # VER 0.1.4
                                        # read STATUS TEC BOOL
                                        self._data_status = float((strs[length - 1][1]))

                                        # VER 0.1.5
                                        # read MTD415T Error Register
                                        self._error_register_bit = int(
                                            (strs[length - 1][2])
                                        )
                                        # print ("DEBUG: error register string = ", self._error_register_bit )

                                        # convert decimal to 16 bit binary
                                        # integer to binary string array
                                        bnr = bin(self._error_register_bit).replace(
                                            "0b", ""
                                        )
                                        # reverse the binary string array
                                        bnr_rev = bnr[::-1]
                                        while len(bnr_rev) < 16:
                                            # fill the binary string with zero
                                            bnr_rev += "0"
                                            # reverse the array
                                            bnr = bnr_rev[::-1]

                                        # check the error register bit
                                        for i in range(len(Constants.ERROR_REG_EVENT)):
                                            if bnr_rev[i] == "1":
                                                if i > 0:
                                                    # PRINT THE ERROR MESSAGE, except bit = 0 "Enable pin not set"
                                                    print(
                                                        "WARNING: MTD415T Temperature control error: ",
                                                        Constants.ERROR_REG_EVENT[i],
                                                    )

                            except:
                                print(
                                    TAG,
                                    "Info: exception at serial port read process, overtone =",
                                    overtone_index,
                                    end="\n",
                                )
                                Log.i(
                                    TAG, "Info: exception at serial port read process"
                                )

                                # DEBUG_0.1.1a
                                # reset buffer
                                data_mag = np.linspace(0, 0, samples)
                                data_ph = np.linspace(0, 0, samples)
                                data_temp = 0.0

                                # reset data raw
                                data_raw = ""
                                # reset buffer
                                buffer = ""

                                self._flag_error_usb = 1

                        # DATA PROCESSING
                        # -----------------------------------------------------

                        if self._flag_error_usb == 0:

                            # VER 0.1.4
                            # set the current values of resonance frequencies in file
                            self.set_frequencies_RT(
                                overtone_index,
                                self.freq_res_current_array[overtone_index],
                            )

                            try:
                                # TODO can't access data_temp or smth
                                self.elaborate_multi(
                                    k,
                                    overtone_index,
                                    coeffs_all,
                                    readF[overtone_index],
                                    samples,
                                    data_mag,
                                    data_ph,
                                    data_temp,
                                    sg_window_size[overtone_index],
                                    spline_points[overtone_index],
                                    spline_factor[overtone_index],
                                    timestamp,
                                )

                                self.elaborate_ampli_phase_multi(
                                    overtone_index,
                                    coeffs_all,
                                    readF[overtone_index],
                                    data_mag,
                                    data_ph,
                                )

                            except ValueError:
                                self._flag_error = 1
                                print(TAG, "Info: value error elaborate data", end="\n")
                                Log.i(TAG, "Info: value error elaborate data")

                            except:
                                self._flag_error = 1
                                if k > Constants.environment:
                                    print(
                                        TAG,
                                        "Info: exception general error elaborate data",
                                        end="\n",
                                    )
                                    Log.i(
                                        TAG,
                                        "Info: exception general error elaborate data",
                                    )

                        # VER 0.1.4
                        # add a new element to the error / status parser for the TEC STATUS variable

                        self._parser6.add6(
                            [
                                self._err1,
                                self._err2,
                                k,
                                self._flag_error_usb,
                                overtone_index,
                                self._data_status,
                            ]
                        )

                        # refreshes error variables at each single overtone sweep
                        self._err1 = 0
                        self._err2 = 0
                        self._flag_error_usb = 0
                        self._boolean_buffer_length = 0

                    # Increases sweep counter
                    k += 1

                # END ACQUISITION LOOP
                # -------------------------------------------------------------
                self._serial.close()

    # STOP
    def stop(self):
        # close serial port
        # DEBUG 0.1.1c
        try:
            self._serial.close()
            print("serial COM port is closed")
        except:
            print("WARNING: unable to close COM port ")

        # Signals the process to stop acquiring data.
        try:
            self._exit.set()
            print("exit acquisition loop ")
        except:
            print("WARNING: unable exit acquisition loop")

        # reset the peak frequency value file
        frequency_calibration_array = self.load_frequencies_file()
        path_RT = Constants.cvs_peakfrequencies_RT_path
        np.savetxt(
            path_RT,
            np.column_stack([frequency_calibration_array, frequency_calibration_array]),
        )

    # GET FREQUENCIES
    def get_frequencies(self, samples):
        """
        :param samples: Number of samples :type samples: int.
        :return: overtone :rtype: float.
        :return: fStep, frequency step  :rtype: float.
        :return: readFREQ, frequency range :rtype: float list.
        """

        startF = []
        stopF = []
        SG_window_size = []
        spline_factor = []
        fStep = []
        spline_points = []
        readFREQ = []

        # Loads frequencies from calibration file
        peaks_mag = self.load_frequencies_file()
        # get numbers of overtones stored in calibration
        peaks_mag_length = len(peaks_mag)

        # 10 MHz get frequency sweep param
        if peaks_mag[0] > 9e06 and peaks_mag[0] < 11e06:
            for i in range(peaks_mag_length):
                # get multiscan sweep paramters
                (startF_temp, stopF_temp, SG_window_size_temp, spline_factor_temp) = (
                    self.getMultiscanParameters_10Mhz(peaks_mag, i)
                )

                # assign multiscan sweep param
                # TODO I do not like manage the list in this way try numpy array here
                startF.append(startF_temp)
                stopF.append(stopF_temp)
                SG_window_size.append(SG_window_size_temp)
                spline_factor.append(spline_factor_temp)

                # Sets the frequency step
                fStep_temp = (stopF_temp - startF_temp) / (samples - 1)
                # assing value
                fStep.append(fStep_temp)

                # set spline points
                spline_points_temp = int((stopF_temp - startF_temp)) + 1
                # assing value
                spline_points.append(spline_points_temp)

                # set frequencies array
                frequencies_array_temp = np.arange(samples) * (fStep_temp) + startF_temp
                # assign value
                readFREQ.append(frequencies_array_temp)

        # 5 MHz get frequency sweep param
        if peaks_mag[0] > 4e06 and peaks_mag[0] < 6e06:
            for i in range(peaks_mag_length):
                # get multiscan sweep paramters
                (startF_temp, stopF_temp, SG_window_size_temp, spline_factor_temp) = (
                    self.getMultiscanParameters_5Mhz(peaks_mag, i)
                )

                # assign multiscan sweep param
                # TODO I do not like manage the list in this way try numpy array here
                startF.append(startF_temp)
                stopF.append(stopF_temp)
                SG_window_size.append(SG_window_size_temp)
                spline_factor.append(spline_factor_temp)

                # Sets the frequency step
                fStep_temp = (stopF_temp - startF_temp) / (samples - 1)
                # assing value
                fStep.append(fStep_temp)

                # set spline points
                spline_points_temp = int((stopF_temp - startF_temp)) + 1
                # assing value
                spline_points.append(spline_points_temp)

                # set frequencies array
                frequencies_array_temp = np.arange(samples) * (fStep_temp) + startF_temp
                # assign value
                readFREQ.append(frequencies_array_temp)

        return (
            startF,
            stopF,
            fStep,
            readFREQ,
            SG_window_size,
            spline_factor,
            spline_points,
        )

    # VER 0.1.4
    # get the current values of resonance frequencies
    def get_frequencies_RT(self, samples):

        startF = []
        stopF = []
        SG_window_size = []
        spline_factor = []
        fStep = []
        spline_points = []
        readFREQ = []

        # VER 0.1.4 get current values of resonance frequency from file
        # open the realt-time resonance frequencies file
        peaks_mag_current = self.load_frequencies_file_RT()

        # get numbers of overtones stored in calibration
        peaks_mag_length = len(peaks_mag_current)

        # 10 MHz get frequency sweep param
        if peaks_mag_current[0] > 9e06 and peaks_mag_current[0] < 11e06:
            for i in range(peaks_mag_length):
                # get multiscan sweep paramters
                (startF_temp, stopF_temp, SG_window_size_temp, spline_factor_temp) = (
                    self.getMultiscanParameters_10Mhz(peaks_mag_current, i)
                )

                # assign multiscan sweep param
                # TODO I do not like manage the list in this way try numpy array here
                startF.append(startF_temp)
                stopF.append(stopF_temp)
                SG_window_size.append(SG_window_size_temp)
                spline_factor.append(spline_factor_temp)

                # Sets the frequency step
                fStep_temp = (stopF_temp - startF_temp) / (samples - 1)
                # assing value
                fStep.append(fStep_temp)

                # set spline points
                spline_points_temp = int((stopF_temp - startF_temp)) + 1
                # assing value
                spline_points.append(spline_points_temp)

                # set frequencies array
                frequencies_array_temp = np.arange(samples) * (fStep_temp) + startF_temp
                # assign value
                readFREQ.append(frequencies_array_temp)

        # 5 MHz get frequency sweep param
        if peaks_mag_current[0] > 4e06 and peaks_mag_current[0] < 6e06:
            for i in range(peaks_mag_length):
                # get multiscan sweep paramters
                (startF_temp, stopF_temp, SG_window_size_temp, spline_factor_temp) = (
                    self.getMultiscanParameters_5Mhz(peaks_mag_current, i)
                )

                # assign multiscan sweep param
                # TODO I do not like manage the list in this way try numpy array here
                startF.append(startF_temp)
                stopF.append(stopF_temp)
                SG_window_size.append(SG_window_size_temp)
                spline_factor.append(spline_factor_temp)

                # Sets the frequency step
                fStep_temp = (stopF_temp - startF_temp) / (samples - 1)
                # assing value
                fStep.append(fStep_temp)

                # set spline points
                spline_points_temp = int((stopF_temp - startF_temp)) + 1
                # assing value
                spline_points.append(spline_points_temp)

                # set frequencies array
                frequencies_array_temp = np.arange(samples) * (fStep_temp) + startF_temp
                # assign value
                readFREQ.append(frequencies_array_temp)

        return (
            startF,
            stopF,
            fStep,
            readFREQ,
            SG_window_size,
            spline_factor,
            spline_points,
        )

    def getMultiscanParameters_10Mhz(self, peaks, overtone):

        if overtone == 0:
            start = peaks[0] - Constants.L10_fundamental
            stop = peaks[0] + Constants.R10_fundamental
            SG_win_size = Constants.SG_window_size10_fundamental
            SP_factor = Constants.Spline_factor10_fundamental

        elif overtone == 1:
            start = peaks[1] - Constants.L10_3th_overtone
            stop = peaks[1] + Constants.R10_3th_overtone
            SG_win_size = Constants.SG_window_size10_3th_overtone
            SP_factor = Constants.Spline_factor10_3th_overtone

        elif overtone == 2:
            start = peaks[2] - Constants.L10_5th_overtone
            stop = peaks[2] + Constants.R10_5th_overtone
            SG_win_size = Constants.SG_window_size10_5th_overtone
            SP_factor = Constants.Spline_factor10_5th_overtone

        return (start, stop, SG_win_size, SP_factor)

    def getMultiscanParameters_5Mhz(self, peaks, overtone):
        # 5 MHz fundamental
        if overtone == 0:
            start = peaks[0] - Constants.L5_fundamental
            stop = peaks[0] + Constants.R5_fundamental
            SG_win_size = Constants.SG_window_size5_fundamental
            SP_factor = Constants.Spline_factor5_fundamental
        # 15 MHz 3rd overtone
        elif overtone == 1:
            start = peaks[1] - Constants.L5_3th_overtone
            stop = peaks[1] + Constants.R5_3th_overtone
            SG_win_size = Constants.SG_window_size5_3th_overtone
            SP_factor = Constants.Spline_factor5_3th_overtone
        # 25 MHz 5th overtone
        elif overtone == 2:
            start = peaks[2] - Constants.L5_5th_overtone
            stop = peaks[2] + Constants.R5_5th_overtone
            SG_win_size = Constants.SG_window_size5_5th_overtone
            SP_factor = Constants.Spline_factor5_5th_overtone
        # 35 MHz 7th overtone
        elif overtone == 3:
            start = peaks[3] - Constants.L5_7th_overtone
            stop = peaks[3] + Constants.R5_7th_overtone
            SG_win_size = Constants.SG_window_size5_7th_overtone
            SP_factor = Constants.Spline_factor5_7th_overtone
        # 45 MHz 7th overtone
        # TODO
        elif overtone == 4:
            start = peaks[4] - Constants.L5_9th_overtone
            stop = peaks[4] + Constants.R5_9th_overtone
            SG_win_size = Constants.SG_window_size5_9th_overtone
            SP_factor = Constants.Spline_factor5_9th_overtone

        return (start, stop, SG_win_size, SP_factor)

    def get_readFREQ(self, samples, overtone):
        # init temp var
        startF = []
        stopF = []
        SG_window_size = []
        spline_factor = []
        fStep = []
        spline_points = []

        # Loads frequencies from calibration file
        peaks_mag = self.load_frequencies_file()

        # 10 MHz quartz resonators
        if peaks_mag[0] > 9e06 and peaks_mag[0] < 11e06:
            # get multiscan sweep paramters
            (startF_temp, stopF_temp, SG_window_size_temp, spline_factor_temp) = (
                self.getMultiscanParameters_10Mhz(peaks_mag, overtone)
            )

            # assign multiscan sweep param for 10 MHz quartz resonators
            # TODO I do not like manage the list in this way try numpy array here
            startF.append(startF_temp)
            stopF.append(stopF_temp)
            SG_window_size.append(SG_window_size_temp)
            spline_factor.append(spline_factor_temp)

            # Sets the frequency step
            fStep_temp = (stopF_temp - startF_temp) / (samples - 1)
            # assing value
            fStep.append(fStep_temp)

            # set spline points
            spline_points_temp = int((stopF_temp - startF_temp)) + 1
            # assing value
            spline_points.append(spline_points_temp)

            # set frequencies array
            frequencies_array_temp = np.arange(samples) * (fStep_temp) + startF_temp

        # 5 MHz quartz resonators
        if peaks_mag[0] > 4e06 and peaks_mag[0] < 6e06:
            # get multiscan sweep paramters
            (startF_temp, stopF_temp, SG_window_size_temp, spline_factor_temp) = (
                self.getMultiscanParameters_5Mhz(peaks_mag, overtone)
            )

            # assign multiscan sweep param for 5 MHz quartz resonators
            # TODO I do not like manage the list in this way try numpy array here
            startF.append(startF_temp)
            stopF.append(stopF_temp)
            SG_window_size.append(SG_window_size_temp)
            spline_factor.append(spline_factor_temp)

            # Sets the frequency step
            fStep_temp = (stopF_temp - startF_temp) / (samples - 1)
            # assing value
            fStep.append(fStep_temp)

            # set spline points
            spline_points_temp = int((stopF_temp - startF_temp)) + 1
            # assing value
            spline_points.append(spline_points_temp)

            # set frequencies array
            frequencies_array_temp = np.arange(samples) * (fStep_temp) + startF_temp

        return frequencies_array_temp

    # VER 0.1.4
    # set the current values of resonance frequencies in file
    def set_frequencies_RT(self, overtone_RT, frequency_RT):

        # open file
        frequency_array_RT = self.load_frequencies_file_RT()

        # get overtone and frequencie
        frequency_array_RT[overtone_RT] = frequency_RT

        # update and write file with current value of frequency at specified overtone
        path_RT = Constants.cvs_peakfrequencies_RT_path
        np.savetxt(path_RT, np.column_stack([frequency_array_RT, frequency_array_RT]))

    # LOAD FREQUENCIES FILE
    @staticmethod
    def load_frequencies_file():
        data = loadtxt(Constants.cvs_peakfrequencies_path)
        peaks_mag = data[:, 0]
        # peaks_phase = data[:,1] #unused at the moment
        return peaks_mag

    # VER 0.1.4
    # load file containing the current values of resonance frequencies
    @staticmethod
    def load_frequencies_file_RT():
        # VER 0.1.4
        data = loadtxt(Constants.cvs_peakfrequencies_RT_path)
        peaks_mag_RT = data[:, 0]
        # peaks_phase = data[:,1] #unused at the moment
        return peaks_mag_RT

    # LOAD CALIBRATION FILE
    def load_calibration_file(self):
        # Loads Fundamental frequency and Overtones from file
        peaks_mag = self.load_frequencies_file()

        # Checks QCS type 5Mhz or 10MHz
        if peaks_mag[0] > 4e06 and peaks_mag[0] < 6e06:
            filename = Constants.csv_calibration_path
        elif peaks_mag[0] > 9e06 and peaks_mag[0] < 11e06:
            filename = Constants.csv_calibration_path10

        data = loadtxt(filename)
        freq_all = data[:, 0]
        mag_all = data[:, 1]
        phase_all = data[:, 2]
        return freq_all, mag_all, phase_all

    # GET SWEEP PARAMTERS
    def get_sweep_parameters():
        # TODO develop if necessary a simple get sweep param
        print("GET SWEEP PARAMETERS HERE")

    # TODO get all overtone
    @staticmethod
    def get_speeds():
        #:return: List of the Overtones :rtype: str list.
        # Loads frequencies from  file (path: 'common\')
        data = loadtxt(Constants.cvs_peakfrequencies_path)
        peaks_mag = data[:, 0]
        reversed_peaks_mag = peaks_mag[::-1]
        return [str(v) for v in reversed_peaks_mag]

    # SEARCH TEENSY COM PORTS
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
            # VER 0.1.5 change the iedntification of the COM port connected to Teensy 4.0
            # using USB VID:PID=16C0:0483  VID 0 VENDOR_ID and PID = PRODUCT_ID of USB devices to identify hardware
            # port[2] = hwid Technical description of serial port
            for port in ports_avaiable:
                if port[2].startswith("USB VID:PID=16C0:0483"):
                    found = True
                    port_connected.append(port[0])
                # else:
                #    Gets a list of the available serial ports.
                #    found_ports.append(port[0])
            if found:
                found_ports = port_connected
            return found_ports

    # COM PORT AVAILABLE
    def _is_port_available(self, port):
        """
        :param port: Port name to be verified.
        :return: True if the port is connected to the host :rtype: bool.
        """
        for p in self.get_ports():
            if p == port:
                return True
        return False

    def _zerolistmaker(self, n):
        listofzeros = [0] * n
        return listofzeros
