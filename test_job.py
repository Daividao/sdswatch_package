from sdswatch.sdswatchlogger import SDSWatchLogger as sdsw_logger

"""
This code is used to create fake jobs that produces SDSWatch logs for test_verdi_job_worker.py
"""

if __name__ == '__main__':
  # SIMULATION for demonstration purpose, creat fake component, component id and fake step where
  # component and component id are mandatory key for sdswatch, and step is just the key
  # that I'm personally interested in. There is no restriction on how you can name your key
  # and its corresponding value.
  example_components = ["component_1", "componnent_2", "component_3"]
  example_component_ids = [["component_1_0", "component_1_1", "component_1_2"],
                           ["component_2_0", "component_2_1"],
                           ["component_3_2", "component_3_1", "component_3_3"]]
                           
  # SIMULATION for demonstration purpose, component_1 has 4 steps, component_2 has 8 steps and all component_3 has 12 steps
  example_steps = [4, 8, 12]
                           
  import random
  i_component = random.choice(range(len(example_components)))
  i_component_id = random.choice(range(len(example_component_ids[i_component])))
  component = example_components[i_component]
  component_id = example_component_ids[i_component][i_component_id]


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
  # instantiate sdswatch logger
  import os
  sdsw_logger.configure(component = component,
                        component_id = component_id,
                        local_log_filedir = os.path.dirname(os.path.abspath(__file__)))
  
  # logging to sdswatch
  sdsw_logger.log("step", "start")
  
  import time
  
  # SIMULATION for demonstration purpose, since each component has different steps
  time.sleep(30)
  for i in range(example_steps[i_component]):
    sdsw_logger.log("step", str(i))
    time.sleep(5)
  
  # logging to sdswatch
  sdsw_logger.log("step", "end")


