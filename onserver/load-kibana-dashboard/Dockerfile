FROM alpine:3.9

# install wget and unzip
RUN apk update
RUN apk add bash curl && rm -rf /var/cache/apk/*

# create data directory
RUN mkdir -p /usr/share/kibana/dashboard/

# Move the dashboard into the container
COPY ./sdswatch-dashboard.json /usr/share/kibana/dashboard/sdswatch-dashboard.json

# Move the script into the container
COPY ./load-kibana-dashboard.sh /usr/share/kibana/dashboard/load-kibana-dashboard.sh

# Move wait-for-it
COPY ./wait-for-it.sh /usr/share/kibana/dashboard/wait-for-it.sh

# give everybody access
RUN chmod -R 777 /usr/share/kibana/dashboard/*

