#!/bin/bash
/usr/share/kibana/dashboard/wait-for-it.sh kibana:5601 -t 200
sleep 60
curl -f -XDELETE -H 'Content-Type: application/json' -H 'kbn-xsrf: true' 'http://kibana:5601/api/saved_objects/index-pattern/sdswatch*'
curl -XPOST -H 'Content-Type: application/json' -H 'kbn-xsrf: true' 'http://kibana:5601/api/kibana/settings/defaultIndex' -d '{"value": "sdswatch*"}'
curl -XPOST kibana:5601/api/kibana/dashboards/import -H 'kbn-xsrf: true' -H 'Content-type:application/json' -d @/usr/share/kibana/dashboard/sdswatch-dashboard.json 
echo 'Templates all loaded up'
