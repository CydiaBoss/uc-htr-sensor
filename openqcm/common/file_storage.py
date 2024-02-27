from openqcm.common.file_manager import FileManager
from misc.constants import Constants
import numpy as np

TAG = ""#"[FileStorage]"

###############################################################################
# Stores and exports data to file (CSV/TXT): saves incoming and outcoming data
###############################################################################
class FileStorage:

    ###########################################################################
    # Saves a CSV-formatted Text file per sweeps in an assigned directory
    ###########################################################################     
    @staticmethod
    def TXT_sweeps_save(filename, path, data_save1, data_save2, data_save3):
        """
        :param filename: Name for the file :type filename: str.
        :param path: Path for the file     :type path: str.
        :param path: Path for the file     :type path: str.
        :param data_save1: data to store (frequency) :type float. 
        :param data_save2: data to store (Amplitude) :type float.
        :param data_save2: data to store (Phase)     :type float.
        """
        # Creates a directory if the specified path doesn't exist
        FileManager.create_dir(path)
        # Creates a file full path based on parameters
        full_path = FileManager.create_full_path(filename, extension=Constants.txt_extension, path=path)
        # creates TXT file
        np.savetxt(full_path, np.column_stack([data_save1, data_save2, data_save3]))  
