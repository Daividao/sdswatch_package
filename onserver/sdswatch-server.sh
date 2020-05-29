#!/usr/bin bash

docker stop $(docker ps -q -a)
docker rm $(docker ps -q -a)
docker rmi docker.elastic.co/logstash/logstash:7.1.1
docker rmi docker.elastic.co/kibana/kibana:7.1.1
docker rmi docker.elastic.co/elasticsearch/elasticsearch:7.1.1 
docker-compose build
docker-compose up
