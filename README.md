# SDSWatch

## Content
### 1. SDSWatchLogger Package (in sdswatch directory)
### 2. Install SDSWatch on client side (in onclient directory)
### 3. Install SDSWatch on server side (in onserver directory)


# 1. SDSWatchLogger Package (in sdswatch directory)

## Install
```
pip3 install git+https://github.com/hysds/hysds-sdswatch.git@master
```

## Methods that SDSWatchLogger provides
For generic type:
```
from sdswatch.logger import SDSWatchLogger

# you can only instantiate once
logger = SDSWatchLogger(file_dir="/path/to/dir", 
                        name="logname", 
                        source_type="source_type", 
                        source_id="source_id")

# to use the logger in other modules after the first instantiation
# logger = SDSWatchLogger.get_logger()

# to log 
logger.log(metric_key="key1", metric_value="value1")
logger.log(metric_key="key2", metric_value="value2")
logger.log(metric_key="key3", metric_value="value3")

```
Example generic type logs (log file will be created by the logger):
```
'2020-05-25 01:52:40.569',100.20.1.18,source_type,source_id,key1,value1
'2020-05-25 01:52:40.569',100.20.1.18,source_type,source_id,key2,value2
'2020-05-25 01:52:40.569',100.20.1.18,source_type,source_id,key3,value3
```
For pge type:
```
from sdswatch.pgelogger import PGESDSWatchLogger

# you can only instantiate once
logger = PGESDSWatchLogger(file_dir="/path/to/dir", 
                           name="job_type")

# to use the logger in other modules after the first instantiation
# logger = PGESDSWatchLogger.get_logger()

# to log
logger.log(metric_key="key1", metric_value="value1")
logger.log(metric_key="key2", metric_value="value2")
logger.log(metric_key="key3", metric_value="value3")
```
Example pge type logs (log file will be created by the logger):
```
'2020-05-25 01:52:40.569',key1,value1
'2020-05-25 01:52:40.570',key2,value2
'2020-05-25 01:52:40.570',key3,value3
```
