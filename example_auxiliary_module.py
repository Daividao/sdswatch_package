from sdswatch.sdswatchlogger import SDSWatchLogger as sdsw_logger

def download():
  sdsw_logger.log("step", "start_downloading")
  success = 0
  for i in range(100):
    if i % 10 == 0:
      success += 1
      sdsw_logger.log("download_ok", "data_"+str(i))
    else:
      sdsw_logger.log("download_failed", "data_"+str(i))
  
  sdsw_logger.log("download_success_rate", success / 100)
  sdsw_logger.log("step", "end_downloading")

def preprocess():
  sdsw_logger.log("step", "start_preprocessing")
  success = 0
  for i in range(100):
    if i % 10 == 0:
      success += 1
      sdsw_logger.log("preprocess_ok", "data_"+str(i))
    else:
      sdsw_logger.log("preprocess_failed", "data_"+str(i))

  sdsw_logger.log("preprocess_success_rate", success / 100)
  sdsw_logger.log("step", "end_preprocessing")

