#!/bin/bash

echo "Start stopping containers..."
docker stop node1
docker stop node2
docker stop node3

echo "Containers stopped."
docker ps
