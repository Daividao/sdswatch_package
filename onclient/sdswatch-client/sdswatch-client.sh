#!/usr/bin/env bash

# clean up old sdswatch-client in case it's running
docker stop sdswatch-client
docker rm sdswatch-client

docker run --name sdswatch-client \ # give a name to the container
--rm \
-u $(id -u):$(id -g) \ # give the container permission to write to data directory
--env HOST=$(curl ifconfig.me) \ # create HOST environment variable in the container with value of host machine's ip address
-v /data/work/jobs:/jobs \ # mount the /data/work/jobs in host machine to /jobs in the container so they share the same thing
-v /export/home/hysdsops/verdi/log:/verdi/ \ 
-v /export/home/hysdsops/verdi/etc/:/usr/share/logstash/config/conf/ \ # mount /export/home/hysdsops/verdi/etc/ instead of logstash.conf
-v /export/home/hysdsops/verdi/share/sdswatch-client/data:/usr/share/logstash/data \ # mount a data directory from host machine to store logstash data for persistence needs
logstash:7.1.1 \
logstash -f /usr/share/logstash/config/conf/logstash.conf --config.reload.automatic # --config.reload.automatic will restart logstash when config file is updated

