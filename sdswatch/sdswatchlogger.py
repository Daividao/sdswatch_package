"""
SDS Watch Logger module for Python 3
"""

import os
import logging
import urllib.request
import time

class SDSWatchLogger:
  __logger = logging.getLogger("sdswatch")
  __sdswatch_configured = False
  
  @staticmethod
  def configure(component, component_id, local_log_filedir):
    """
    configure configures the SDS Watch Logger by defining
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
      local_log_filedir (str): a full path to the current directory of the main module
                   which is required to be directly contained inside the job directory.
    """
    if SDSWatchLogger.__sdswatch_configured:
      raise Exception("SDS Watch has already been configured, and it cannot be configured again")
    
    # get public ip address
    ip_address = urllib.request.urlopen('https://ifconfig.me').read().decode('utf8')

    # if the directory containing the output log file doesn't exist,
    # create on
    os.makedirs(local_log_filedir, exist_ok = True)
    local_log_filepath = os.path.join(local_log_filedir, "sdswatch.log")

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

    # configure SDS Watch Logger with the above information
    SDSWatchLogger.__logger.setLevel(level)
    SDSWatchLogger.__logger.addHandler(sdswatch_handler)
    logging.Formatter.converter = time.gmtime
    SDSWatchLogger.__sdswatch_configured = True
    
  @staticmethod
  def log(key, value):
    """
    Write a log line to the file specified in the constructor. In particular,
    here is the schema or structure of the log line inside that file:
       <timestamp>,<public ip address>,<component>,<component_id>,<key>,<value>
    Since key token and value token  are flexible values, developers need to provide them
 
    Args:
      key (str or number): value of key token
      value (str or number): value of value token
    """
    SDSWatchLogger.__logger.info('', extra = {"key" : key, "value" : value})
