"""
SDS Watch Logger module for Python 3
"""

import os
import logging
import urllib.request
import time

class SDSWatchLogger:
  __sdswatch_logger = None
  """
  This is a class for logging into SDSWatch ElasticSearch database to 
  do visualization in real time. 
  """
  
  def __init__(self, component, component_id, local_log_filepath):
    """
    SDS Watch Logger constructor.
    
    Notes:
      You can only instatiate only once. To use
        SDS Watch Logger in multiple modules, instantiate once in your main module
        and use SDSWatchLogger.getLogger() in other modules.

    Args:
      component (str): required value for each SDS Watch log line
      component_id (str): requred value for each SDS Watch log line
      local_log_filepath (str): a full path to the location of log files on your
        local machine, and the file should have ".sdswatch.log" at the end"

    Raises:
      Exception if SDSWatchLogger.__sdswatch_logger already exists or 
        invalid arguments for local_log_filepath
    """
    if SDSWatchLogger.__sdswatch_logger != None:
      raise Exception("you can only instantiate SDSWatch once, please use "
                      + "SDSWatchLogger.getLogger() instead")
    else:
      __sdswatch_logger = self

    if not local_log_filepath.endswith(".sdswatch.log"):
      raise Exception("SDS Watch requires \'local_log_filepath\' to have "
                           + "\'.sdswatch.log\'at the end")

    self.logger = logging.getLogger("sdswatch")
    self.__configure(component, component_id, local_log_filepath)
    
  @staticmethod
  def getLogger():
    """
    Returns:
      SDSWatchLogger (obj): the one and only instance of SDSWatchLogger

    Raises:
      Exception if SDSWatchLogger hasn't been instantiated
    """
    if SDSWatchLogger.__sdswatch_loger == None:
      raise Exception("SDS Watch Logger hasn't been created, please instantiate it first")
    return SDSWatchLogger.__sdswatch_logger

  def log(self, key, value):
    """
    Write a log line to the file specified in the constructor. In particular,
    here is the schema or structure of the log line inside that file:
       <timestamp>,<public ip address>,<component>,<component_id>,<key>,<value>
    Since key token and value token  are flexible values, developers need to provide them
 
    Args:
      key (str or number): value of key token
      value (str or number): value of value token
    """
    self.logger.info('', extra = {"key" : key, "value" : value})
    
  def __configure(self, component, component_id, local_log_filepath):
    """
    __configure configures the SDS Watch Logger by defining
    the format of each log line and where to store it. Regarding the
    format of the log line, SDS Watch requires the following schema:
    '<timestamp>', '<public ip>', '<component>', '<component_id>', '<key>', '<value>'
    where comma is delimiter and each schema token needs to be quoted to allow commas within
    the quotes

    Notes:
      This function is supposed to be private, and should not be called
        anywhere else except the constructor

    Args:
      componen (str): required value for each SDS Watch log line
      component_id (str): required value for each SDS Watch log line
      local_log_filepath (str): a full path to the location of output file, and
        the file should have ".sdswatch.log" at the end
    """
    # get public ip address
    ip_address = urllib.request.urlopen('https://ifconfig.me').read().decode('utf8')

    # if the directory containing the output log file doesn't exist,
    # create on
    os.makedirs(os.path.dirname(local_log_filepath), exist_ok = True)

    # by default, SDS Watch Logger uses info level for logging
    level = logging.INFO

    # define the log format. By default, python logging module already provides
    # timestamp when logging
    log_format = ("\'%(asctime)s.%(msecs)03d\',"
                  "\'" + ip_address + "\',"
                  "\'" + component + "\',"
                  "\'" + component_id + "\',"
                  "\'%(key)s\',"
                  "\'%(value)s\'")
    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_format, datefmt=datefmt)

    # specify where to send the log, and make sure to use defined formatter
    # to process it
    sdswatch_handler = logging.FileHandler(filename = local_log_filepath)
    sdswatch_handler.setLevel(level)
    sdswatch_handler.setFormatter(formatter)

    # get "SDS Watch" logger object
    sdswatch_logger = self.logger

    # configure SDS Watch Logger with the above information
    sdswatch_logger.setLevel(level)
    sdswatch_logger.addHandler(sdswatch_handler)
    logging.Formatter.converter = time.gmtime
