"""
SDSWatch Logging module for PGE to emit log in format
     <timestamp>, <key>, <value>
"""

import os
import logging
import urllib.request
import time

class PGESDSWatchLogger:
    __pge_sdsw_logger = None
    
    def __init__(self, file_dir, name):
        """
        Configures a logger to write log lines to /file_dir/name.pge.sdswatch.log with
        format <timestamp>, <metric_key>, <metric_value>

        Args:
          file_dir (str): a full path to where to store the log file
          name (str): name of the log
        """
        if logging.getLogger("pgesdswatch").hasHandlers():
            raise Exception("PGESDSWatchLogger already existed. Please use PGESDSWatchLogger.get_sdsw_logger() instead")
        
        # use Python logging module to log
        self._logger = PGESDSWatchLogger.__get_logger(file_dir, name)
 
        # restrict the instantiation of a class to one "single" instance
        PGESDSWatchLogger.__pge_sdsw_logger = self

    @staticmethod
    def __get_logger(file_dir, name):
        """
        Configures Python logger
        """
        # if the directory containing the output log file doesn't exist,
        # create one
        os.makedirs(file_dir, exist_ok = True)
        file_path = os.path.join(file_dir, name + ".pge.sdswatch.log")

        # define the log format. By default, python logging module already
        # provides timestamp when logging
        log_format = ("\'%(asctime)s.%(msecs)03d\'," 
                      "%(metric_key)s,"
                      "%(metric_value)s")
        datefmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(log_format, datefmt=datefmt)

        # By default, SDSWatch use INFO level for logging
        level = logging.INFO
        
        # specify where to send the log, and make sure to use formatter to format it
        sdswatch_handler = logging.FileHandler(filename = file_path)
        sdswatch_handler.setLevel(level)
        sdswatch_handler.setFormatter(formatter)

        # configure SDS Watch Logger with the above handler
        logger = logging.getLogger("pgesdswatch")
        logger.setLevel(level)
        logger.addHandler(sdswatch_handler)
        logging.Formatter.converter = time.gmtime
        return logger
        

    def log(self, metric_key, metric_value):
        """
        Writes a log line with given format to the file created in configuration methods.
        
        Args:
          metric_key (str or number): value of key token
          metric_value (str or number): value of value token

        Note:
          use double quote to allow comma within metric_value
        """
        self._logger.info('', extra = {"metric_key" : metric_key, "metric_value" : metric_value})
        
    @staticmethod
    def get_logger():
        """
        Returns PGESDSWatchLogger if already instantiated
        """
        if PGESDSWatchLogger.__pge_sdsw_logger == None:
            raise Exception("PGESDSWatchLogger hasn't existed. Please instantiate it first !")
        return PGESDSWatchLogger.__pge_sdsw_logger
