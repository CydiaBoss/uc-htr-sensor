import multiprocessing

TAG = ""  # "[Parser]"


###############################################################################
# Process to parse incoming data and distribute it to worker
###############################################################################
class ParserProcess(multiprocessing.Process):

    ###########################################################################
    # Initializing values for process
    ###########################################################################
    def __init__(
        self,
        data_queue1: multiprocessing.Queue,
        data_queue2: multiprocessing.Queue,
        data_queue3: multiprocessing.Queue,
        data_queue4: multiprocessing.Queue,
        data_queue5: multiprocessing.Queue,
        data_queue6: multiprocessing.Queue,
        data_queue_F_multi: multiprocessing.Queue,
        data_queue_D_multi: multiprocessing.Queue,
        data_queue_A_multi: multiprocessing.Queue,
        data_queue_P_multi: multiprocessing.Queue,
    ):
        """
        :param data_queue{i}: References to queue where processed data will be put.
        :type data_queue{i}: multiprocessing Queue.
        """
        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()

        self._out_queue1 = data_queue1
        self._out_queue2 = data_queue2
        self._out_queue3 = data_queue3
        self._out_queue4 = data_queue4
        self._out_queue5 = data_queue5
        self._out_queue6 = data_queue6

        # frequency out queue
        self._out_queue_F_multi = data_queue_F_multi
        # dissipation out queue
        self._out_queue_D_multi = data_queue_D_multi
        # ampli out queue
        self._out_queue_A_multi = data_queue_A_multi
        # phase out queue
        self._out_queue_P_multi = data_queue_P_multi

    ###########################################################################
    # Add new raw data and calculated data to the corresponding internal queue
    ###########################################################################
    def add1(self, data):
        """
        Adds new raw data to internal queue1 (serial data: amplitude).
        :param data: Raw data coming from acquisition process.
        :type data: float.
        """
        self._out_queue1.put(data)

    def add2(self, data):
        """
        Adds new raw data to internal queue2 (serial data: phase).
        :param data: Raw data coming from acquisition process.
        :type float: float.
        """
        self._out_queue2.put(data)

    def add3(self, data):
        """
        Adds new processed data to internal queue3 (Resonance frequency).
        :param data: Calculated data.
        :type data: float.
        """
        self._out_queue3.put(data)

    def add4(self, data):
        """
        Adds new processed data to internal queue3 (Q-factor/dissipation).
        :param data: Calculated data.
        :type data: float.
        """
        self._out_queue4.put(data)

    def add5(self, data):
        """
        Adds new processed data to internal queue3 (Q-factor/dissipation).
        :param data: Calculated data.
        :type data: float.
        """
        self._out_queue5.put(data)

    def add6(self, data):
        """
        Adds new processed data to internal queue3 (Q-factor/dissipation).
        :param data: Calculated data.
        :type data: float.
        """
        self._out_queue6.put(data)

    def add_F_multi(self, data):

        self._out_queue_F_multi.put(data)

    def add_D_multi(self, data):

        self._out_queue_D_multi.put(data)

    def add_A_multi(self, data):
        self._out_queue_A_multi.put(data)

    def add_P_multi(self, data):
        self._out_queue_P_multi.put(data)

    def stop(self):
        """
        Signals the process to stop parsing data.
        :return:
        """
        self._exit.set()
