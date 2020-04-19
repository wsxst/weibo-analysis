from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import time
from pyspark import SparkContext, SparkConf
from tqdm import tqdm
from collections import Counter
from math import pow
from hdfs.client import Client
import os, sys
import pdb
import copy
from operator import add


app = Flask(__name__)
CORS(app, resources='/*')


def computeContribs(neighbors, rank):
    for neighbor in neighbors: yield (neighbor, rank / len(neighbors))


def get_ranks():
    if len(client.list("/res")) == 0:
        return None
    return sc.textFile("hdfs:///res/res.txt").map(lambda line: (line.split("\t")[0], float(line.split("\t")[1])))


def to_txt(data):
    return "\t".join(str(d) for d in data)


def write_ranks(ranks):
    if len(client.list("/res")) != 0:
        print(client.list("/res"))
        client.delete("/res/res.txt",True)
    ranks.map(to_txt).saveAsTextFile("hdfs:///res/res.txt")


def dynamic_compute():
    links = sc.textFile(hdfs_relation_file_path) \
        .map(lambda line: (line.split("\t")[0], line.split("\t")[1])) \
        .groupByKey() \
        .persist()

    print("links count:", links.count())

    flag = 0
    pre = None

    ranks = get_ranks()
    print(ranks.collect())
    for x in tqdm(range(iter_num)):
        contribs = links.join(ranks) \
            .flatMap(
            lambda page__neighbors_rank: computeContribs(page__neighbors_rank[1][0], page__neighbors_rank[1][1]))
        ranks = contribs.reduceByKey(add) \
            .map(lambda page_contrib: (page_contrib[0], page_contrib[1] * stay_prob + (1 - stay_prob)))
        if flag == 0:
            flag = 1
            tt=ranks.collectAsMap()
            pre = Counter(ranks.collectAsMap())
        else:
            tmp = Counter(ranks.collectAsMap())
            #print(tmp)
            
            tmp1 = copy.deepcopy(tmp)
            tmp1.subtract(pre)
            #print(tmp1)
            tmp_dict = dict(tmp1)
            
            #print(tmp_dict)
            #pdb.set_trace()
            stop_flag = False
            for k in reversed(range(1, stop_thres)):
                res_list = [(abs(tmp_dict[k1]) <= pow(10, -k)) for k1 in tmp_dict]
                flag1 = True
                for res in res_list:
                    if not res:
                        flag1 = False
                        break
                if flag1:
                    print("[MY_INFO]Threshold reaches 1e-", k)
                    if k == stop_thres - 1:
                        stop_flag = True
                    break
            if stop_flag:
                break
            pre = tmp
    res = ranks.collect()
    write_ranks(ranks)
    # for ranks in res:
    #     print(ranks)
    print("Over!")
    return res


def user_exist(id):
    with client.read(userprofile_file_path, encoding='utf-8', delimiter='\n') as reader:
        for i, line in enumerate(reader):
            line = line.strip()
            if line == "":
                continue
            pair = line.split("\t")
            if pair[0] == str(id):
                return True
    return False


# TODO:
def add_user():
    pass


def delete_user(id):
    if not user_exist(id):
        return None, False
    new_lines = []
    with client.read(relation_file_path, encoding='utf-8', delimiter='\n') as reader:
        for i, line in enumerate(reader):
            line = line.strip()
            if line == "":
                continue
            pair = line.split("\t")
            if not (pair[0] == id or pair[1] == id):
                new_lines.append(line)
    new_lines_str = ""
    for new_line in new_lines:
        new_lines_str += new_line + "\n"
    print(new_lines_str)
    client.write(relation_file_path, new_lines_str, overwrite=True, append=False, encoding="utf-8")
    new_lines = []
    with client.read(userprofile_file_path, encoding='utf-8', delimiter='\n') as reader:
        for i, line in enumerate(reader):
            line = line.strip()
            if line == "":
                continue
            pair = line.split("\t")
            if not pair[0] == id:
                new_lines.append(line)
    new_lines_str = ""
    for new_line in new_lines:
        new_lines_str += new_line + "\n"
    client.write(userprofile_file_path, new_lines_str, overwrite=True, append=False, encoding="utf-8")
    return dynamic_compute(), True


def get_followers(id):
    if not user_exist(id):
        return None, False
    res = []
    with client.read(relation_file_path, encoding='utf-8', delimiter='\n') as reader:
        for i, line in enumerate(reader):
            line = line.strip()
            if line == "":
                continue
            pair = line.split("\t")
            #print("line:",line)
            if pair[1] == str(id):
                res.append(pair[0])
    return res, True


def get_followees(id):
    if not user_exist(id):
        return None, False
    res = []
    with client.read(relation_file_path, encoding='utf-8', delimiter='\n') as reader:
        for i, line in enumerate(reader):
            line = line.strip()
            if line == "":
                continue
            pair = line.split("\t")
            if pair[0] == str(id):
                res.append(pair[1])
    return res, True


def get_profile(id):
    if not user_exist(id):
        return None, False
    res = {}
    with client.read(userprofile_file_path, encoding='utf-8', delimiter='\n') as reader:
        for i, line in enumerate(reader):
            line = line.strip()
            if line == "":
                continue
            pair = line.split("\t")
            if pair[0] == str(id):
                res["id"] = id
                res["name"] = pair[1]
                res["province"] = pair[2]
                res["city"] = pair[3]
                res["register_time"] = pair[4]
                res["last_login_time"] = pair[5]
                res["gender"] = pair[6]
                res["follows"] = int(pair[7])
                res["fans"] = int(pair[8])
                res["posts"] = int(pair[9])
                res["homepage"] = pair[10]
                res["desc"] = pair[11]
                break
    return res, True


def get_posts(id):
    if not user_exist(id):
        return None, False
    res_list = []
    with client.read(weibo_file_path, encoding='utf-8', delimiter='\n') as reader:
        for i, line in enumerate(reader):
            line = line.strip()
            if line == "":
                continue
            pair = line.split("\t")
            if pair[1] == str(id):
                res = {}
                res["id"] = pair[0]
                res["post_user_id"] = id
                res["forward"] = pair[2]
                res["comment"] = pair[3]
                res["post_time"] = pair[4]
                res["conent"] = pair[5]
                res_list.append(res)
    return res_list, True


def users_exist(id1, id2):
    find_flag1 = False
    find_flag2 = False
    with client.read(userprofile_file_path, encoding='utf-8', delimiter='\n') as reader:
        for i, line in enumerate(reader):
            line = line.strip()
            if line == "":
                continue
            pair = line.split("\t")
            if pair[0] == id1:
                find_flag1 = True
            if pair[0] == id2:
                find_flag2 = True
    if not find_flag1 or not find_flag2:
        return False
    return True


def follow(id1, id2):
    if not users_exist(id1, id2):
        return None, 0, 0, 0, 0, False
    lines = []
    index = -1
    u1_old = -1
    u1_new = -1
    u2_old = -1
    u2_new = -1
    with client.read(relation_file_path, encoding='utf-8', delimiter='\n') as reader:
        for i, line in enumerate(reader):
            line = line.strip()
            if line == "":
                continue
            lines.append(line)
            pair = line.split("\t")
            if pair[0] == id1 and pair[1] == id2:
                index = i
                break
    if index != -1:
        return None, 0, 0, 0, 0, False
    new_line = id1 + "\t" + id2 + "\n"
    client.write(relation_file_path, new_line, overwrite=False, append=True, encoding='utf-8')
    num = 0
    ranks = get_ranks()
    for pair in ranks.collect():
        if pair[0] == id1:
            u1_old = pair[1]
            num += 1
        if pair[0] == id2:
            u2_old = pair[1]
            num += 1
        if num == 2:
            break
    res = dynamic_compute()
    num = 0
    for pair in res:
        if pair[0] == id1:
            u1_new = pair[1]
            num += 1
        if pair[0] == id2:
            u2_new = pair[1]
            num += 1
        if num == 2:
            break
    return res, u1_old, u1_new, u2_old, u2_new, True


def unfollow(id1, id2):
    if not users_exist(id1, id2):
        return None, 0, 0, 0, 0, False
    lines = []
    index = -1
    u1_old = -1
    u1_new = -1
    u2_old = -1
    u2_new = -1
    with client.read(relation_file_path, encoding='utf-8', delimiter='\n') as reader:
        for i, line in enumerate(reader):
            line = line.strip()
            if line == "":
                continue
            lines.append(line)
            pair = line.split("\t")
            if pair[0] == id1 and pair[1] == id2:
                index = i
                break
    if index == -1:
        return None, 0, 0, 0, 0, False
    lines.pop(index)
    lines_str = ""
    for line in lines:
        lines_str += line + "\n"
    client.write(relation_file_path, lines_str, overwrite=True, append=False, encoding='utf-8')
    num = 0
    ranks = get_ranks()
    for pair in ranks.collect():
        if pair[0] == id1:
            u1_old = pair[1]
            num += 1
        if pair[0] == id2:
            u2_old = pair[1]
            num += 1
        if num == 2:
            break
    res = dynamic_compute()
    num = 0
    for pair in res:
        if pair[0] == id1:
            u1_new = pair[1]
            num += 1
        if pair[0] == id2:
            u2_new = pair[1]
            num += 1
        if num == 2:
            break
    return res, u1_old, u1_new, u2_old, u2_new, True


def first_compute_pr():
    client.upload(data_dir_path, "/data/test_data/relation_test.txt", cleanup=True, overwrite=True)
    client.upload(data_dir_path, "/data/test_data/userprofile.txt", cleanup=True, overwrite=True)
    links = sc.textFile(hdfs_relation_file_path) \
        .map(lambda line: (line.split("\t")[0], line.split("\t")[1])) \
        .groupByKey() \
        .persist()

    ranks = links.map(lambda page_neighbor: (page_neighbor[0], 1.0))
    write_ranks(ranks)
    return dynamic_compute()


@app.route('/',methods=['GET','POST'])
def ping():
    return 'Hello, World!'


def make_data(ranks):
    res = {}
    res["data"] = []
    num = 1
    ranks = sorted(ranks, key=lambda x:x[1], reverse=True)
    for i in ranks:
        _dict = {}
        _dict["rank"] = num
        num = num + 1
        _dict["id"] = i[0]
        _dict["score"] = i[1]
        res["data"].append(_dict)
    return res


@app.route('/analyze/static', methods=['POST'])
def fun0():
    start_t = time.time()
    ranks = first_compute_pr()
    res = make_data(ranks)
    end_t = time.time()
    print("*"*10)
    print("[Static analysis time]"+str(end_t-start_t)+"s")

    return jsonify(res)


@app.route('/relation/follow',methods=['POST'])
def fun1():
    start_t = time.time()
    data = json.loads(request.get_data(as_text=True))
    uid1 = data["id1"]
    uid2 = data["id2"]
    ranks, u1_old, u1_new, u2_old, u2_new, flag = follow(uid1, uid2)
    res = {}
    if not flag:
        res["msg"] = "error"
    else:
        res = make_data(ranks)
        res["u1_old"] = u1_old
        res["u1_new"] = u1_new
        res["u2_old"] = u2_old
        res["u2_new"] = u2_new
        res["msg"] = "success"
        end_t = time.time()
        print("[Dynamic analysis time]"+str(end_t-start_t)+"s")

    return jsonify(res)


@app.route('/relation/cancelfollow',methods=['POST'])
def fun2():
    start_t = time.time()
    data = json.loads(request.get_data(as_text=True))
    uid1 = data["id1"]
    uid2 = data["id2"]
    ranks, u1_old, u1_new, u2_old, u2_new, flag = unfollow(uid1, uid2)
    res = {}
    if not flag:
        res["msg"] = "error"
    else:
        res = make_data(ranks)
        res["u1_old"] = u1_old
        res["u1_new"] = u1_new
        res["u2_old"] = u2_old
        res["u2_new"] = u2_new
        res["msg"] = "success"
        end_t = time.time()
        print("[Dynamic analysis time]"+str(end_t-start_t)+"s")

    return jsonify(res)


# TODO:
@app.route('/user/add',methods=['POST'])
def fun3():
    pass


@app.route('/user/remove',methods=['POST'])
def fun4():
    start_t = time.time()
    data = json.loads(request.get_data(as_text=True))
    ranks, flag = delete_user(data["id"])
    print(ranks)
    res = {}
    if not flag:
        res["msg"] = "error"
    else:
        res = make_data(ranks)
        res["msg"] = "success"
        end_t = time.time()
        print(res)
        print("[Dynamic analysis time]"+str(end_t-start_t)+"s")
    return jsonify(res)


@app.route('/user/viewprofile',methods=['POST'])
def fun5():
    data = json.loads(request.get_data(as_text=True))
    uid = data["id"]
    res = {}
    res["data"], flag = get_profile(uid)
    if not flag:
        res["msg"] = "error"
    else:
        res["msg"] = "success"
    return jsonify(res)


@app.route('/user/viewfollows',methods=['POST'])
def fun6():
    data = json.loads(request.get_data(as_text=True))
    uid = data["id"]
    res = {}
    res["data"], flag = get_followees(uid)
    if not flag:
        res["msg"] = "error"
    else:
        res["msg"] = "success"
    return jsonify(res)


@app.route('/user/viewfans',methods=['POST'])
def fun7():
    data = json.loads(request.get_data(as_text=True))
    uid = data["id"]
    res = {}
    res["data"], flag = get_followers(uid)
    if not flag:
        res["msg"] = "error"
    else:
        res["msg"] = "success"
    return jsonify(res)


@app.route('/user/viewposts',methods=['POST'])
def fun8():
    data = json.loads(request.get_data(as_text=True))
    uid = data["id"]
    res = {}
    res["data"], flag = get_posts(uid)
    if not flag:
        res["msg"] = "error"
    else:
        res["msg"] = "success"
    return jsonify(res)


if __name__ == "__main__":

    # TODO: Modify the data file path based on your own system
    data_dir_path = "/data/"
    relation_file_path = data_dir_path + "relation_test.txt"
    hdfs_relation_file_path = "hdfs://" + relation_file_path
    userprofile_file_path = data_dir_path + "userprofile.txt"
    weibo_file_path = data_dir_path + "weibo.txt"
    # You can modify this configuration if your main memory is large enough
    SparkContext.setSystemProperty("spark.executor.memory","512m")
    # The params include: after x iterations, the loop will stop; if the difference between current result and previous result is lower than y, stop loop; z is 'alpha' in formula of pagerank
    iter_num = 100
    stop_thres = 3
    stay_prob = 0.85
    conf = SparkConf()
    # If you want to use Spark cluster rather than local, to uncomment the line below
    if len(sys.argv) == 1 or sys.argv[1] == "1":
        conf.setMaster("spark://172.18.0.2:7077")
    conf.setAppName("PageRank")
    sc = SparkContext(conf=conf)
    # TODO: Modify this as the absolute path of this py file
    sc.addPyFile("/code/backend/backend.py")
    client = Client("http://node1:50070/",root="/",timeout=10000,session=False)
    ranks = None
    
    app.run("0.0.0.0", port=5000, debug=False)
