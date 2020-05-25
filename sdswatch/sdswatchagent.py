# require at least python 2.7
import os
import subprocess
import time
import shutil
import fileinput

# get full path to logstash configuration file. Note that "sdswatchagent.py" is in the same directory as "configs" directory.
current_dir = os.path.dirname(os.path.realpath(__file__))
default_config_file_path = os.path.join(current_dir, "configs", "indexer.conf.logstash")

class SDSWatchAgent:
    def __init__(self, redis_ip, logstash_setup_dir_path, worker_dir_path):
        # redis port to which logstash can send logs
        self.redis_ip = redis_ip

        # if there is job being monitored.
        self.job_being_monitored = False
        
	# name of sdswatch log from pge in job directory
	self.pge_log_name = "pge.sdswatch.log"

	# name of sdswatch log from job_worker
	self.worker_log_name = "job_worker.sdswatch.log"

        # set up Logstash
        self.logstash_setup_dir_path = logstash_setup_dir_path
        self.worker_dir_path = worker_dir_path
        self.job_dir_path = "" # location of job directory to monitor SDSWatch logs. Updated when new job found
        self.pge_sincedb_file_path = "" # sincedb file of pge logs which Logstash used to store history. Updated when new job found.
        self.config_file_path = "" # Logstash configuration file to parse SDSWatch logs. Updated when new job found.
        self.__setup_logstash_and_run()
        
    def monitor_new_job(self, job_dir_path):
        self.job_being_monitored = True
        self.job_dir_path = job_dir_path
        # path to new job directory containing pge.sdswatch.log
        new_path = "    path => {}\n".format("\"" + os.path.join(self.job_dir_path, self.pge_log_name) + "\"")

        # get all lines in the Logstash configuration file
        lines = None
        with open(self.config_file_path, 'r') as conf:
            lines = conf.readlines()
            
        # update path which is at line 3 in the Logstash configuration file
        lines[2] = new_path

        # write everything back
        with open(self.config_file_path, 'w') as conf:
            conf.writelines(lines)
            
        # wait for Logstash to reload. Since Logstash check the changes in the configuration file every 3s, we need to wait 4 second
        # to make sure that Logstash doesn't use the old configuration of previous job to write to the new sincedb file
        time.sleep(4)
        
        # empty sincedb file of old job. Logstash use sincedb to ignore already processed logs
        open(self.pge_sincedb_file_path, 'w').close()

    def wait(self):
        while self.__is_logstash_sending_logs():
            time.sleep(1)
            
        self.job_being_monitored = False
        print("SDSWatch Logs have been successfully shipped to database")
        
    
    def __setup_logstash_and_run():
        # create a .sdswatch directory to store all Logstash setup files and make sure it is empty
        sdswatch_dir_path = os.path.join(self.logstash_setup_dir_path, ".sdswatch", "")
        if os.path.exists(sdswatch_dir_path) and os.path.isdir(sdswatch_dir_path):
            shutil.rmtree(sdswatch_dir_path)
        os.makedirs(sdswatch_dir_path, exist_ok = True)
        
        # create a directory to store Logstash sincedb null file of pge
        pge_sincedb_dir_path = os.path.join(sdswatch_dir_path, "pge_sincedb", "")
        os.makedirs(pge_sincedb_dir_path, exist_ok = True)
        self.pge_sincedb_file_path = os.path.join(pge_sincedb_dir_path, "null")

        # create a directory to store Logstash sincedb null file of worker
        worker_sincedb_dir_path = os.path.join(sdswatch_dir_path, "worker_sincedb", "")
        os.makedirs(worker_sincedb_dir_path, exist_ok = True)
        worker_sincedb_file_path = os.path.join(worker_sincedb_dir_path, "null")

        # create a directory to store Logstash config file
        config_dir_path = os.path.join(sdswatch_dir_path, "config", "")
        os.makedirs(config_dir_path, exist_ok = True)
        self.config_file_path = os.path.join(config_dir_path, "indexer.conf.logstash")

        # create a directory to store Logstash data
        data_dir_path = os.path.join(sdswatch_dir_path, "data", "")
        os.makedirs(data_dir_path, exist_ok = True)

        # create a fake pge job directory to start up Logstash
        startup_dir_path = os.path.join(sdswatch_dir_path, "startup", "")
        os.makedirs(startup_dir_path, exist_ok = True)
        
        # generate input section and output section for Logstash configuration file
        with open(self.config_file_path, 'a') as dst_conf:
            # generate input section to monitor empty startup log
            dst_conf.write("input {\n")
            dst_conf.write("  file {\n")
            dst_conf.write("    path => {}\n".format("\"" + startup_dir_path + self.pge_log_name + "\""))
            dst_conf.write("    start_position => \"beginning\"\n")
            dst_conf.write("    sincedb_path => {}\n".format("\"" + self.sincedb_file_path + "\""))
            dst_conf.write("  }\n")
            dst_conf.write("  file {\n")
            dst_conf.write("    path => {}\n".format("\"" + self.worker_dir_path + self.worker_log_name + "\""))
            dst_conf.write("    start_position => \"beginning\"\n")
            dst_conf.write("    sincedb_path => {}\n".format("\"" + worker_sincedb_file_path + "\""))
            dst_conf.write("  }\n")
            dst_conf.write("}\n\n")

            # copy already written filter section
            global default_config_file_path
            with open(default_config_file_path, "r") as src_conf:
                for line in src_conf:
                    # ignore comment
                    if line.startswith("#"):
                        continue
                    dst_conf.write(line)
            dst_conf.write("\n")
            
            # generate output part to send logs to redis port
            dst_conf.write("output {\n")
            if self.redis_ip != "":
                dst_conf.write("  elasticsearch {\n") # NEED TO CHANGE TO REDIS IN PRODUCTION !!!
                dst_conf.write("    hosts => {}\n".format("\"" + self.redis_ip + "\""))
                dst_conf.write("    index => \"sdswatch\"\n")
                dst_conf.write("  }\n")
            dst_conf.write("  stdout {\n")
            dst_conf.write("    codec => rubydebug\n")
            dst_conf.write("  }\n")
            dst_conf.write("}\n\n")

        # run Logstash. By default --config.reload.automatic check for changes in configuration file every 3 seconds
        subprocess.run(["logstash", "-f", self.config_file_path, "--path.data", data_dir_path, "--config.reload.automatic"])

        # wait for Logstash to successfully start. It takes a while to start.
        time.sleep(60)

    def __is_logstash_sending_logs(self):
        def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
            return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
        
        if not self.job_being_monitored:
            return False
        
        # get file path of sincedb file of pge and sdswatch log of pge to make sure if all logs have been shipped
        sincedb_null = self.pge_sincedb_file_path
        sdswatch_log = os.path.join(self.job_dir_path, self.pge_log_name)

        # check if there exists logs to ship
        if not os.path.exists(sdswatch_log):
            return False

        #  example of output1: 4171377 -rw-r--r--  1 trandaod  staff  3204733 Apr 11 13:30 /Users/trandaod/Desktop/ELK/sdswatch/sdswatch_package/jobs/2020/04/11/20/30/job_0/sdswatch.log
        output1 = subprocess.getoutput("ls -li " + sdswatch_log)
        total = float(output1.split()[5])
        if isclose(total, 0.0):
          return False

        # check if logstash has started reading sdswatch logs
        if not os.path.exists(sincedb_null):
          return True

        # example of output2: 4171377 1 4 3204733 1586637095.3862529 /Users/trandaod/Desktop/ELK/sdswatch/sdswatch_package/jobs/2020/04/11/20/30/job_0/sdswatch.log
        output2 = subprocess.getoutput("cat " + sincedb_null)
        if len(output2.split()) == 0:
          return True
        
        completed = float(output2.split()[3])
        percentage = int(100 * completed / total)
        return percentage < 100
    
