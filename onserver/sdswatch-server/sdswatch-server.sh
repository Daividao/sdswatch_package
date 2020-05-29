#!/usr/bin bash

# stop sdswatch-logstash, sdswatch-elasticsearch,
# sdswatch-redis, load-kibana-dasbhboard if it they exist.
# This is a bad syntax because I stop everything
docker stop $(docker ps -q -a)
docker rm $(docker ps -q -a)

# re-download images
# reason: If I don't do it, I got a very weird error.
docker rmi docker.elastic.co/logstash/logstash:7.1.1
docker rmi docker.elastic.co/kibana/kibana:7.1.1
docker rmi docker.elastic.co/elasticsearch/elasticsearch:7.1.1 


docker-compose build
docker-compose up
