from sdswatch import SDSWatchLogger
from example_auxiliary_module import download, preprocess

if __name__ == '__main__':

  # when you are running multiple jobs, you should have a different log directory for each job
  log_directory = "job3"
  local_log_filepath = ("/Users/trandaod/Desktop/ELK/sdswatch/example_sdswatchlogger/example_logs/" +
                        log_directory +
                        "/example_log.sdswatch.csv")

  # instantiate SDS Watch Logger for the first time
  component = "optimization"
  component_id = "optimization_xlk2"
  sdswatch_logger = SDSWatchLogger(component, component_id, local_log_filepath)
  sdswatch_logger.log("step", "start_main")
  download()
  preprocess()
  sdswatch_logger.log("step", "end_main")


