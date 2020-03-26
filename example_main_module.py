from sdswatch import SDSWatchLogger
from example_auxiliary_module import download, preprocess

if __name__ == '__main__':
  # instantiate SDS Watch Logger for the first time.
  # IMPORTANT NOTE: SDS Watch assumes the log file is contained in
  # the job directory, so it's important that you have a main module
  # is also contained in the job directory, and instantiate the SDS Watch Logger
  # with the absolute path to the current directory of the main module.
  # For example:
  # if your job name is "job1", then in Verdi, you'll have
  # "jobs/2020/03/17/07/35/job1/example_main_module.py
  # then SDS Watch Logger will send log to
  # "jobs/2020/03/17/07/35/job1/"sdswatch.log"
  # Other paths won't work. 
  sdswatch_logger = SDSWatchLogger(component = "optimization",
                                   component_id = "optimization_xlk2",
                                   local_log_filepath = os.path.dirname(__file__))
  # logging to sdswatch
  sdswatch_logger.log("step", "start_main")
  
  # go to another module, please open example_auxiliary_module.py to see how SDSWatchLogger is
  # called in different modules from the main
  download()
  preprocess()

  # logging to sdswatch
  sdswatch_logger.log("step", "end_main")


