#!/bin/bash

bash ./stop_containers.sh

echo "Begin to start containers..."
docker start node1
docker start node2
docker start node3

bash ./start-all.sh

echo "Containers started."
docker ps -a
