#!/usr/bin/env bash

# clean up old sdswatch-client in case it's running
docker stop sdswatch-client
docker rm sdswatch-client

docker run --name sdswatch-client \
--rm \
-u $(id -u):$(id -g) \
--env HOST=$(curl ifconfig.me) \
-v /data/work/jobs:/jobs \
-v /export/home/hysdsops/verdi/log:/verdi/ \
-v /export/home/hysdsops/verdi/etc/:/usr/share/logstash/config/conf/ \
-v /export/home/hysdsops/verdi/share/sdswatch-client/data:/usr/share/logstash/data \
logstash:7.1.1 \
logstash -f /usr/share/logstash/config/conf/logstash.conf --config.reload.automatic

