import atexit
import logging, os, sys
import logging.handlers
from enum import Enum
import time

from misc.constants import MAX_LOG, LOG_FOLDER, Constants, Architecture


###############################################################################
# Enumeration for the Logger levels
###############################################################################
class LoggerLevel(Enum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG


###############################################################################
# Logging package - All packages can use this module
###############################################################################
class Logger:

    ###########################################################################
    # Creates logging file (.txt)
    ###########################################################################
    def __init__(self, level=LoggerLevel.INFO, enable_console=True):
        """
        :param level: Level to show in log.
        :type level: int.
        """
        log_format_file = logging.Formatter("%(asctime)s,%(levelname)s,%(message)s")
        log_format_console = logging.Formatter("%(levelname)s %(message)s")
        self.logger = logging.getLogger()
        self.logger.setLevel(level.value)

        # Make directory if needed
        log_dir_path = os.path.dirname(f"{LOG_FOLDER}/")
        os.makedirs(log_dir_path, exist_ok=True)

        # Grab current log files
        log_files = [f for f in os.listdir(log_dir_path) if f.endswith(".log") and os.path.isfile(os.path.join(log_dir_path, f))]
        log_files.sort()

        # Delete older files
        while len(log_files) > MAX_LOG:
            os.remove(os.path.join(log_dir_path, log_files.pop(0)))

        file_handler = logging.handlers.RotatingFileHandler(
            "{}/{}".format(LOG_FOLDER, f"{int(time.time())}.log"),
            maxBytes=5120,
            backupCount=0,
        )
        file_handler.setFormatter(log_format_file)
        self.logger.addHandler(file_handler)

        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(log_format_console)
            self.logger.addHandler(console_handler)
        self._show_user_info()

        # Prep for shutdown
        atexit.register(self.close)

    ###########################################################################
    # Closes the enabled loggers.
    ###########################################################################
    @staticmethod
    def close():
        logging.shutdown()

    ###########################################################################
    # Logs at debug level (debug,info,warning and error messages)
    ###########################################################################
    @staticmethod
    def d(tag, *msg):
        """
        :param tag: TAG to identify the log :type tag: str.
        :param msg: Message to log.         :type msg: str.
        """
        logging.debug("[{}] {}".format(str(tag), " ".join([str(x) for x in msg])))

    ####
    @staticmethod
    def i(tag, *msg):
        logging.info("[{}] {}".format(str(tag), " ".join([str(x) for x in msg])))

    ####
    @staticmethod
    def w(tag, *msg):
        logging.warning("[{}] {}".format(str(tag), " ".join([str(x) for x in msg])))

    ####
    @staticmethod
    def e(tag, *msg):
        logging.error("[{}] {}".format(str(tag), " ".join([str(x) for x in msg])))

    ###########################################################################
    # logs and prints architecture-related informations
    ###########################################################################
    @staticmethod
    def _show_user_info():
        tag = "Startup"
        Logger.i(tag, "{} - {}".format(Constants.app_title, Constants.app_version))
        Logger.i(tag, "Platform: {}".format(Architecture.get_os_name()))
        Logger.i(tag, "Path: {}".format(Architecture.get_path()))
        Logger.i(tag, "Python version: {}".format(Architecture.get_python_version()))
