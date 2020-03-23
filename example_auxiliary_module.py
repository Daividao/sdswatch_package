from sdswatch import SDSWatchLogger

def download():
  sdswatch_logger = SDSWatchLogger.getLogger()
  sdswatch_logger.log("step", "start_downloading")
  success = 0
  for i in range(100):
    if i % 10 == 0:
      success += 1
      sdswatch_logger.log("download_ok", "data_"+str(i))
    else:
      sdswatch_logger.log("download_failed", "data_"+str(i))
  
  sdswatch_logger.log("download_success_rate", success / 100)
  sdswatch_logger.log("step", "end_downloading")

def preprocess():
  sdswatch_logger = SDSWatchLogger.getLogger()
  sdswatch_logger.log("step", "start_preprocessing")
  success = 0
  for i in range(100):
    if i % 10 == 0:
      success += 1
      sdswatch_logger.log("preprocess_ok", "data_"+str(i))
    else:
      sdswatch_logger.log("preprocess_failed", "data_"+str(i))

  sdswatch_logger.log("preprocess_success_rate", success / 100)
  sdswatch_logger.log("step", "end_preprocessing")

