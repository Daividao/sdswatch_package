# SDSWatchLogger Package

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
logger = SDSWatchLogger.get_logger()

# to log 
logger.log(metric_key="key",
           metric_value="value")
```
For pge type:
```
from sdswatch.pgelogger import PGESDSWatchLogger

# you can only instantiate once
logger = PGESDSWatchLogger(file_dir="/path/to/dir", 
                         name="job_type")

# to use the logger in other modules after the first instantiation
logger = PGESDSWatchLogger.get_logger()

# to log 
logger.log(metric_key="key",
           metric_value="value")
```
