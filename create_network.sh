#!/bin/bash

echo create network
docker network create --subnet=172.18.0.0/16 bigdata
echo create success 
docker network ls
