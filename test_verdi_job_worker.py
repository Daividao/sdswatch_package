import os
import subprocess
from datetime import datetime
import time
from sdswatch.sdswatchagent import SDSWatchAgent

def get_path(job_name):
  path = ""
  current_time = datetime.utcnow().strftime('%Y/%m/%d/%H/%M')
  current_dirpath = os.path.dirname(os.path.abspath(__file__))
  path = os.path.join(current_dirpath, "jobs", current_time, job_name, "")
  return path

current_dirpath = os.path.dirname(os.path.abspath(__file__))
jobs_path = os.path.join(current_dirpath, "jobs", "")

total_jobs = 4
i = 0

while i < total_jobs:
  # job dir
  job_dir = "job_" + str(i)

  # make dirs    
  path = get_path(job_dir)
  os.makedirs(path, exist_ok = True)

  # instantiate SDS Watch Agent for each job and add log directory to monitor
  # Also specify which elasticsearch port to send to
  sdswatch_agent = SDSWatchAgent(path, "http://localhost:9200")

  # run SDS Watch Agent, it will send sdswatch log to ElasticSearch
  sdswatch_agent.run()
  
  # create fake PGE in the job directory
  subprocess.run(["cp", "test_job.py", path + job_dir + ".py"]) 
 
  # run sample PGE code
  subprocess.run(["python3", path + job_dir + ".py"])
  
  # kill SDS Watch Agent
  sdswatch_agent.stop()
   
  i += 1
