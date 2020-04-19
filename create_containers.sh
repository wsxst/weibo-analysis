#!/bin/bash

echo "Create and start containers..."

echo "Create and start node1 container..."
docker run -d \
--restart=always \
--net bigdata \
--ip 172.18.0.2 \
--privileged \
-p 17070:7070 \
-p 51070:50070 \
-p 18088:8088 \
-p 19000:9000 \
-p 10080:80 \
-p 15000:5000 \
--name node1 \
--hostname node1 \
--add-host node2:172.18.0.3 \
--add-host node3:172.18.0.4 \
centos-bigdata:v1
echo "Create and start node2 container..."
docker run -d \
--restart=always \
--net bigdata \
--ip 172.18.0.3 \
--privileged \
-p 28081:8081 \
-p 52075:50075 \
-p 29000:9000 \
--name node2 \
--hostname node2 \
--add-host node1:172.18.0.2 \
--add-host node3:172.18.0.4 \
centos-bigdata:v1
echo "Create and start node3 container..."
docker run -d \
--restart=always \
--net bigdata \
--ip 172.18.0.4 \
--privileged \
-p 38081:8081 \
-p 53075:50075 \
-p 39000:9000 \
--name node3 \
--hostname node3 \
--add-host node1:172.18.0.2 \
--add-host node2:172.18.0.3  \
centos-bigdata:v1

bash ./start-all.sh $1 $2

echo "Finished!"
docker ps

