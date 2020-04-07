from sdswatch.sdswatchlogger import SDSWatchLogger as sdsw_logger

"""
This code is used to create fake jobs with fake metrics that produces SDSWatch logs for test_verdi_job_worker.py
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
  import os
  sdsw_logger.configure(component = component,
                        component_id = component_id,
                        local_log_filedir = os.path.dirname(os.path.abspath(__file__)))
  
  # logging to sdswatch
  sdsw_logger.log("step", "start")
  
  import time
  
  # SIMULATION for demonstration purpose, since each component has different steps
  time.sleep(25)
  for i in range(1, example_steps[i_component]):
    sdsw_logger.log("step", str(i))
    if i_component == 0:
       sdsw_logger.log("total_attempted_downloads", "50")
       for i in range(50):
         if i % 2 == 0:
           sdsw_logger.log("download_ok", "1")
         else:
           sdsw_logger.log("download_ok", "0")
    elif i_component == 1:
        sdsw_logger.log("total_attempted_process", "20")
        for i in range(20):
          if i % 4 == 0:
            sdsw_logger.log("processed", "0")
          else:
            sdsw_logger.log("processed", "1")
          
    elif i_component == 2:
        sdsw_logger.log("total_attempted_receivers", "40")
        for i in range(40):
          if i % 5 == 0:
            sdsw_logger.log("received", "1")
          else:
            sdsw_logger.log("received", "0")
    sdsw_logger.log("LoL", "LoL")
    time.sleep(5)
  
  # logging to sdswatch
  sdsw_logger.log("step", "end")


