import os
import subprocess
import time

def main():
  sdswatch_agent = SDSWatchAgent("logstash", "indexer.conf.sdswatch")
  sdswatch_agent.activate()

class SDSWatchAgent:
  def __init__(self, pipeline, config_filename):
    self.pipeline = pipeline
    self.config_filename = config_filename
  
  def activate(self):
    if self.pipeline.lower() == "logstash":
      """
      path.data is saved in /usr/local/var/lib/<current_time>/
      """
      current_time = time.localtime()
      current_time = time.strftime('%Y-%m-%dT%H:%M:%S', current_time)
      path_data = "/usr/local/var/lib/logstash_path_data/" + str(current_time) + "/"
      config_file = (os.path.dirname(os.path.realpath(__file__)) +
                     "/configs/" +
                     self.pipeline.lower() +
                     "/" +
                     self.config_filename)
      subprocess.run(["logstash -f", config_file, "--path.data", path_data])
