from sdswatch.sdswatchlogger import SDSWatchLogger as sdsw_logger
from example_auxiliary_module import download

sdsw_logger.configure_pge_logger("/Users/trandaod/Desktop/jpl/", "example_hello_world")

if __name__ == "__main__":
  print("ok")
  sdsw_logger.log("key1", "value1")
  download()
  sdsw_logger.log("key2", "value2")
  


