#!/bin/bash

bash create_network.sh && \
#这一步中间可能会下载失败，重新运行构建镜像的脚本即可
bash build_docker_image.sh && \
bash create_containers.sh $1 $2
