#!/bin/bash

echo "Start cleaning containers..."

#docker ps -a

#docker kill $(docker ps -a -q)
#docker rm $(docker ps -q -f status=exited)

docker rm -f $(docker ps -aq)

docker ps -a
echo "Clean finished!"
