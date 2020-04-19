#!/bin/bash

echo "build centos-bigdata images"

docker build -t centos-bigdata:v1 .
