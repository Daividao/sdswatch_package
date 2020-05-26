"""
Generic SDSWatch Logging module to emit log in format
     <timestamp>, <host>, <source_type>, <source_id>, <key>, <value>
"""

import os
import logging
import urllib.request
import time

class SDSWatchLogger:
    __sdsw_logger = None
    
    def __init__(self, file_dir, name, source_type, source_id):
        """
        Configures a logger to write log lines to /file_dir/name.pge.sdswatch.log with
        format <timestamp>, <host>, <source_type>, <source_id>, <metric_key>, <metric_value>

        Args:
          file_dir (str): a full path to where to store the log file
          name (str): name of the log
          source_type (str): type of log
          source_id (str): id of log
        """
        if logging.getLogger("sdswatch").hasHandlers():
            raise Exception("SDSWatchLogger already existed. Please use SDSWatchLogger.get_sdsw_logger() instead")
        
        # use Python logging module to log
        self._logger = self.__get_logger(file_dir, name, source_type, source_id)
 
        # restrict the instantiation of a class to one "single" instance
        SDSWatchLogger.__sdsw_logger = self
        
    def __get_logger(self, file_dir, name, source_type, source_id):
        """
        Configures Python logger
        """
        # get public ip address
        host = urllib.request.urlopen('https://ifconfig.me').read().decode('utf8')

        # preprocess arguments
        source_type = source_type.strip().lower()
        source_id = source_id.strip().lower()
        
        # if the directory containing the output log file doesn't exist,
        # create one
        os.makedirs(file_dir, exist_ok = True)
        file_path = os.path.join(file_dir, name + ".sdswatch.log")

        # define the log format. By default, python logging module already
        # provides timestamp when logging
        log_format = ("\'%(asctime)s.%(msecs)03d\',"
                      "\'" + host + "\',"
                      "\'" + source_type + "\',"
                      "\'" + source_id + "\'," 
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
        logger = logging.getLogger("sdswatch")
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
        if SDSWatchLogger.__sdsw_logger == None:
            raise Exception("SDSWatchLogger hasn't existed. Please instantiate it first !")
        return SDSWatchLogger.__sdsw_logger
