import os
import subprocess
import time

current_dir = os.path.dirname(os.path.realpath(__file__))
logstash_config_filepath = os.path.join(current_dir, "configs", "indexer.conf.logstash")

class SDSWatchAgent:
  def __init__(self, log_dir, elasticsearch_ip):
    # directory of the sdswatch log file. This should be directly in the job directory
    self.log_dir = log_dir

    # ip adress of elasticsearch so logstash can send logs to
    self.elasticsearch_ip = elasticsearch_ip

    # name of the hidden directory used to store information required to run Logstash services
    self.sdswatch_dir = ".sdswatch"
    
    # generate the Logstash configuration for each job directory
    # this configuration file is also stored in .sdswatch
    self.config_filepath = self.__logstash_make_config()

    # cache the process so we can kill it later
    self.process = None
    
  def __logstash_make_config(self):
    # create a directory to store sincedb_path, sincedb_path directory is inside .sdswatch
    sincedb_filedir = os.path.join(self.log_dir, self.sdswatch_dir, "sincedb_path", "")
    os.makedirs(sincedb_filedir, exist_ok = True)

    # generate a configuration file to listen to a log file of only one job
    # the filter configuration is already written because it is the same for all sdswatch logs
    # the input and output configuration will be generated depending on how agent is instantiated
    global logstash_config_filepath
    job_config_filedir = os.path.join(self.log_dir, self.sdswatch_dir, "config", "")
    os.makedirs(job_config_filedir, exist_ok = True)
    job_config_filepath = os.path.join(job_config_filedir, "indexer.conf.logstash")
    with open(job_config_filepath, 'a') as dst_conf:
      # generate input part to monitor a particular job directory
      dst_conf.write("input {\n")
      dst_conf.write("  file {\n")
      dst_conf.write("    path => {}\n".format("\"" + self.log_dir + "sdswatch.log\""))
      dst_conf.write("    start_position => \"beginning\"\n")
      dst_conf.write("    sincedb_path => \"{}null\"\n".format(sincedb_filedir))
      dst_conf.write("  }\n")
      dst_conf.write("}\n\n")

      # copy filter part which is the same for all sdswatch log
      with open(logstash_config_filepath, "r") as src_conf:
        for line in src_conf:
          dst_conf.write(line)

      # generate output part to send log to a specific elasticsearch port
      dst_conf.write("\n")
      dst_conf.write("output {\n")
      
      if self.elasticsearch_ip != "":
        dst_conf.write("  elasticsearch {\n")
        dst_conf.write("    hosts => {}\n".format("\"" + self.elasticsearch_ip + "\""))
        dst_conf.write("    index => \"sdswatch\"\n")
        dst_conf.write("  }\n")
     
      dst_conf.write("  stdout {\n")
      dst_conf.write("    codec => rubydebug\n")
      dst_conf.write("  }\n")
        
      dst_conf.write("}\n\n")
          
    return job_config_filepath
    
  def run(self):
    self.__logstash_run()

  def stop(self):
    self.__logstash_stop()

  def __logstash_run(self):
    # create directory to store logstash path data
    path_data_filedir = os.path.join(self.log_dir, self.sdswatch_dir, "path.data", "")
    os.makedirs(path_data_filedir, exist_ok = True)

    # make a config file to monitor only a log directory
    job_config_filepath = self.config_filepath
    
    # run logstash
    self.process = subprocess.Popen(["logstash", "-f", job_config_filepath, "--path.data", path_data_filedir])
    
  def __logstash_stop(self):
    if self.process == None:
      raise Exception("SDS Watch agent hasn't been activated yet")
    self.process.terminate()
    del self
    
