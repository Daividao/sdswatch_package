"""
SDS Watch Logger module for pge
"""

import os
import logging
import urllib.request
import time

class SDSWatchLogger:
  __logger = logging.getLogger("sdswatch")
  __sdswatch_configured = False
  
  @staticmethod
  def configure_generic_logger(file_dir, name, source_type, source_id):
    """
    Configure a logger to write log lines to /file_dir/name.sdswatch.log with
    format <timestamp>, <host>, <source_type>, <source_id>, <metric_key>, <metric_value>

    Args:
      file_dir (str): a full path to where to store the log file
      name (str): name of the log
      source_type (str): required value for each SDS Watch log line
      source_id (str): required value for each SDS Watch log line
    """
    
    if SDSWatchLogger.__sdswatch_configured:
      raise Exception("SDS Watch has already been configured, and it cannot be configured again")

    SDSWatchLogger.__sdswatch_configured = True
    
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
    SDSWatchLogger.__configure_logger(file_path, formatter)


  @staticmethod
  def configure_pge_logger(file_dir, name):
    """
    Configure a logger to write log lines to /file_dir/name.pge.sdswatch.log with
    format <timestamp>, <metric_key>, <metric_value>

    Args:
      file_dir (str): a full path to where to store the log file
      name (str): name of the log
    """
    
    if SDSWatchLogger.__sdswatch_configured:
      raise Exception("SDS Watch has already been configured, and it cannot be configured again")

    SDSWatchLogger.__sdswatch_configured = True
    
    # if the directory containing the output log file doesn't exist,
    # create one
    os.makedirs(file_dir, exist_ok = True)
    file_path = os.path.join(file_dir, name + ".pge.sdswatch.log")

    # define the log format. By default, python logging module already provides
    # timestamp when logging
    log_format = ("\'%(asctime)s.%(msecs)03d\',"
                  "%(metric_key)s,"
                  "%(metric_value)s")
    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_format, datefmt=datefmt)
    SDSWatchLogger.__configure_logger(file_path, formatter)

  @staticmethod
  def __configure_logger(file_path, formatter):
    # By default, SDSWatch use INFO level for logging
    level = logging.INFO
    
    # specify where to send the log, and make sure to use formatter to format it
    sdswatch_handler = logging.FileHandler(filename = file_path)
    sdswatch_handler.setLevel(level)
    sdswatch_handler.setFormatter(formatter)

    # configure SDS Watch Logger with the above handler
    SDSWatchLogger.__logger.setLevel(level)
    SDSWatchLogger.__logger.addHandler(sdswatch_handler)
    logging.Formatter.converter = time.gmtime
    
    
  @staticmethod
  def log(metric_key, metric_value):
    """
    Write a log line with given format to the file created in configuration methods.
    
    Args:
      metric_key (str or number): value of key token
      metric_value (str or number): value of value token

    Note:
      use double quote to allow comma within metric_value
    """
    
    if not SDSWatchLogger.__sdswatch_configured:
      raise Exception("Please configure SDS Watch Logger before logging")

    SDSWatchLogger.__logger.info('', extra = {"metric_key" : metric_key, "metric_value" : metric_value})
