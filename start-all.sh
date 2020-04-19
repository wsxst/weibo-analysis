#!/bin/bash

#保证ssh服务启动
num=0
flags=(0 0 0)
while [ $num -ne 3 ]
do
	for i in 1 2 3
	do
		if [ ${flags[`expr $i - 1`]} -eq 0 ]
		then
			flag=$(docker ps -qf name=node$i)
			if [ -n "$flag" ]
			then
				docker exec -it node$i /usr/sbin/sshd
				num=`expr $num + 1`
			fi
		fi
	done
done
num=0
while [ $num -ne 3 ]
do
	for i in 1 2 3
	do
		flag=$(docker exec -it node$i ps -ef|grep ssh|grep -v grep)
		if [ -n "$flag" ]
		then
			num=`expr $num + 1`
		fi
	done
done

#复制测试数据,启动Hadoop,将测试数据加载到HDFS上;复制Spark配置文件,启动Spark
for i in 1 2 3
do
	docker cp ./configs/spark-env.sh node$i:///usr/local/spark-2.4.5-bin-without-hadoop/conf/spark-env.sh
	j=`expr $i + 1`
	docker exec -it node$i bash -c "echo \"export SPARK_LOCAL_IP=172.18.0.$j\" >> /usr/local/spark-2.4.5-bin-without-hadoop/conf/spark-env.sh"
done
docker cp ./data node1:/data/test_data
docker exec -it node1 /usr/local/hadoop-2.7.3/start-hadoop.sh
docker exec -it node1 hdfs dfs -mkdir /data
docker exec -it node1 hdfs dfs -mkdir /res
docker exec -it node1 hdfs dfs -put /data/test_data/relation_test.txt /data
docker exec -it node1 hdfs dfs -put /data/test_data/userprofile.txt /data
docker exec -it node1 /usr/local/spark-2.4.5-bin-without-hadoop/sbin/start-all.sh

#复制前后端production版本代码,启动Nginx,启动后端服务程序
echo "export const backend_ip=\"$1\";" > ./code/frontend/src/api/config.js
cd ./code/frontend && npm install cnpm -g --registry=https://registry.npm.taobao.org && cnpm install && npm run build && cd ../.. 
docker cp ./code node1:/
docker exec -it node1 nginx
docker exec -d node1 python3 /code/backend/backend.py $2
