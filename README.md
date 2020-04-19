# 微博红人识别平台

前端Vue.js，后端Flask，涉及Spark、Hadoop等分布式技术。现有功能为基于PageRank算法得到新浪微博大V排名。

## 目录说明

必须按照如下目录结构才可直接运行
```
|--$HOME
|----code
|------frontend
|------backend
|----configs
|----script
|----data
|----tools
|----Dockerfile
|----build_docker_image.sh
|----clean_containers.sh
|----create_containers.sh
|----create_network.sh
|----in-docker.sh
|----start_containers.sh
|----start-all.sh
|----stop_containers.sh
```

**tools（请自行下载）**:其中应包括[hadoop-2.7.3.tar.gz](http://archive.apache.org/dist/hadoop/core/hadoop-2.7.3/hadoop-2.7.3.tar.gz)、jdk-8u212-linux-x64.tar.gz、[nginx-1.16.1.tar.gz](https://nginx.org/download/nginx-1.16.1.tar.gz)、[scala-2.12.7.tgz](https://www.scala-lang.org/files/archive/scala-2.12.7.tgz)、[spark-2.4.5-bin-without-hadoop.tgz](https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-2.4.5/spark-2.4.5-bin-without-hadoop.tgz)

**code**：用于展示与分析的程序代码，包括前端（frontend，基于Vue.js搭建，如果要继续进行开发，需要先执行```npm install```安装相应的包）和后端（backend，Flask框架）

**configs**：配置文件

**data（如需要请提issue）**：示例数据，relation_test.txt是用户之间的关注关系（每一行中前者关注后者），userprofile.txt是用户信息，此处由于服务器内存限制，仅从大数据集中取了一小部分数据用作测试

**script**：Hadoop的启动与停止脚本

**Dockerfile**：docker构建脚本，其中各项有较为详尽的注释

**build_docker_image.sh**：构建docker镜像

**clean_containers.sh**：清理容器

**create_containers.sh**：从镜像创建容器并运行

**create_network.sh**：为docker创建子网

**in-docker.sh**：以交互形式进入某一个主机，后面可跟 1或2或3 共3种参数，分别对应node1、node2、node3三个主机

**start_containers.sh**：启动容器

**start-all.sh**：开启ssh服务，并先后启动Hadoop、Spark

**stop_containers.sh**：停止运行容器

## 部署步骤

由于前端是基于Vue.js构建的,所以首先需要在宿主机上安装npm

```
#centos:
sudo yum install npm
#ubuntu:
sudo apt install npm
```

由于docker需要和宿主机内核打交道,所以需要root权限,运行时需要转为root用户或借助sudo

```
#1/2代表1或2，1代表将分布式计算运行在spark集群上（占用内存较大，服务器空闲内存少于4G不建议尝试，容易卡死），2代表以local模式运行
sudo bash run.sh 服务器IP 1/2
```

接下来就可以在浏览器中通过```http://服务器IP:10080```访问平台了
