import os
import subprocess
import time

current_dir = os.path.dirname(os.path.realpath(__file__))
logstash_config_filepath = os.path.join(current_dir, "configs", "logstash", "indexer.conf.logstash")
# splunk_config_filepath = os.path.join(current_dir, "configs", "splunk", "indexer.conf.splunk")
# datadog_config_filepath = os.path.join(current_dir, "configs", "datadog", "indexer.conf.datadog")

class SDSWatchAgent:
  def __init__(self, pipeline, log_dir):
    self.pipeline = pipeline
    self.log_dir = log_dir
    self.process = None

  def run(self):
    if self.pipeline.lower() == "logstash":
      self.__logstash_run()

  def stop(self):
    if self.pipeline.lower() == "logstash":
      self.__logstash_stop()
      
  def __logstash_run(self):
    def __logstash_make_config():
      # create a directory to store sincedb_path
      sincedb_filedir = os.path.join(self.log_dir, "sdswatch_logstash", "sincedb_path", "")
      os.makedirs(sincedb_filedir, exist_ok = True)

      # generate a configuration file to listen to a log file of only one job
      global logstash_config_filepath
      job_config_filedir = os.path.join(self.log_dir, "sdswatch_logstash", "config", "")
      os.makedirs(job_config_filedir, exist_ok = True)
      job_config_filepath = os.path.join(job_config_filedir, "indexer.conf.logstash")
      with open(job_config_filepath, 'a') as dst_conf:
        dst_conf.write("input {\n")
        dst_conf.write("  file {\n")
        dst_conf.write("    path => {}\n".format("\"" + self.log_dir + "sdswatch.log\""))
        dst_conf.write("    start_position => \"beginning\"\n")
        dst_conf.write("    sincedb_path => \"{}null\"\n".format(sincedb_filedir))
        dst_conf.write("  }\n")
        dst_conf.write("}\n\n")
        with open(logstash_config_filepath, "r") as src_conf:
          for line in src_conf:
            dst_conf.write(line)             
      return job_config_filepath

    # create directory to store logstash path data
    path_data_filedir = os.path.join(self.log_dir, "sdswatch_logstash", "path.data", "")
    os.makedirs(path_data_filedir, exist_ok = True)

    # make a config file to monitor only a log directory
    job_config_filepath = __logstash_make_config()
    
    # run logstash
    self.process = subprocess.Popen(["logstash", "-f", job_config_filepath, "--path.data", path_data_filedir])
    
  def __logstash_stop(self):
    if self.process == None:
      raise Exception("SDS Watch agent hasn't been activated yet")
    self.process.terminate()
    
