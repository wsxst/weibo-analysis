<template>
  <div class="hello">
    <img src="../assets/weibo.jpg" alt="">
    <h1>微博“红人”识别平台</h1>
    <el-row style="margin-top:10px;">
        <el-button type="primary" @click="actStaticAnalyze">静态分析</el-button>
    </el-row>
    <el-row style="margin-top:10px;">
      <el-button @click="actAddUser">
        新增一个用户
      </el-button>
    </el-row>
    <el-row :gutter="20" type="flex" justify="center" style="margin-top:10px;">
      <el-col :span="3" class="demo-input-suffix">
        <el-input v-model="user1_input" placeholder="请输入用户1的ID"></el-input>
      </el-col>
      <el-col :span="2.5">
        <el-button type="danger" @click="actRemoveUser">删除这个用户</el-button>
      </el-col>
    </el-row>
    <el-row  :gutter="20" type="flex" justify="center" style="margin-top:10px;">
      <el-col :span="2.5">
        <el-button @click="actViewFollows">查看ta关注了谁</el-button>
      </el-col>
      <el-col :span="2.5">
        <el-button @click="actViewFuns">查看ta的粉丝</el-button>
      </el-col>
      <el-col :span="2.5">
        <el-button @click="actViewProfile">查看ta的个人信息</el-button>
      </el-col>
      <el-col :span="2.5">
        <el-button @click="actViewPosts">查看ta发过的微博</el-button>
      </el-col>
    </el-row>
    <el-row type="flex" justify="center" :gutter="20" style="margin-top:10px;">
      <el-col :span="3">
        <el-input v-model="user2_input" placeholder="请输入用户2的ID"></el-input>
      </el-col>
      <el-col :span="2.5">
        <el-button @click="actFollow" type="primary">关注</el-button>
      </el-col>
      <el-col :span="2.5">
        <el-button type="danger" @click="actCancelFollow">取消关注</el-button>
      </el-col>
    </el-row>
    <div class="tablewrapper">
    <el-table
            stripe
            :data="tableData"
            style="width: 100%"
            >
      <el-table-column
              prop="rank"
              label="排名"
              min-width="33%">
      </el-table-column>
      <el-table-column
              prop="id"
              label="用户ID"
              min-width="33%">
      </el-table-column>
      <el-table-column
              prop="score"
              label="得分（PR值）"
              min-width="33%">
      </el-table-column>
    </el-table>
    <el-table
          stripe
          :data="tableData2"
          style="width: 100%">
    <el-table-column
            prop="type"
            label="信息类型"
            min-width="50%">
    </el-table-column>
    <el-table-column
            prop="value"
            label="信息内容"
            min-width="50%">
    </el-table-column>
  </el-table>
    <el-table
            stripe
            :data="tableData4"
            style="width: 100%">
      <el-table-column
              prop="id"
              label="微博信息ID"
              width="180">
      </el-table-column>
      <el-table-column
              prop="post_user_id"
              label="发布微博的用户ID"
              width="180">
      </el-table-column>
      <el-table-column
              prop="forward"
              label="转发数"
              width="180">
      </el-table-column>
      <el-table-column
              prop="comment"
              label="评论数"
              width="180">
      </el-table-column>
      <el-table-column
              prop="post_time"
              label="发布时间"
              width="180">
      </el-table-column>
      <el-table-column
              prop="content"
              label="发布内容">
      </el-table-column>
    </el-table>
    <el-table
            stripe
            :data="tableData3"
            style="width: 100%">
      <el-table-column
              prop="id"
              :label="tableLabel"
              width="180">
      </el-table-column>
    </el-table>
    </div>
  </div>
</template>

<script>
import {follow, cancelFollow, addUser, removeUser, viewFollows, viewFans, viewProfile, staticAnalyze} from "../api/user";

export default {
  name: 'HelloWorld',
  data() {
    return {
      user1_input: '',
      user2_input: '',
      tableData: [],
      userProfileDict: {
        "用户ID":"id",
        "省份":"province",
        "市县":"city",
        "注册时间":"register_time",
        "最近一次登录时间":"last_login_time",
        "性别":"gender",
        "关注数":"follows",
        "粉丝数":"fans",
        "发布微博数":"posts",
        "新浪博客地址":"homepage",
        "个人简介":"desc"
      },
      tableData2: [{
        "type":"用户ID",
        "value":""
      },{
        "type":"省份",
        "value":""
      },{
        "type":"市县",
        "value":""
      },{
        "type":"注册时间",
        "value":""
      },{
        "type":"最近一次登录时间",
        "value":""
      },{
        "type":"性别",
        "value":""
      },{
        "type":"关注数",
        "value":""
      },{
        "type":"粉丝数",
        "value":""
      },{
        "type":"发布微博数",
        "value":""
      },{
        "type":"新浪博客地址",
        "value":""
      },{
        "type":"个人简介",
        "value":""
      }],
      tableData3:[],
      tableData4:[],
      tableLabel:""
    }
  },
  methods: {
    actFollow() {
      if(this.user1_input === "" || this.user2_input === "") {
        alert("用户1ID和用户2ID不能为空！");
        return;
      }
      const data = {
        "id1": this.user1_input,
        "id2": this.user2_input,
      };
      follow(data)
      // eslint-disable-next-line no-unused-vars
              .then(res => {
                if(res.data.msg === "error") {
                  alert("用户1或用户2不存在，请重新输入正确的用户ID！");
                } else {
                  alert("关注成功！\n" +
                          this.user1_input + "的得分由" + res.data["u1_old"] + "变为" + res.data["u1_new"] + "\n" +
                          this.user2_input + "的得分由" + res.data["u2_old"] + "变为" + res.data["u2_new"] + "\n");
                  let list = [];
                  for(let i in res.data.data){
                    list.push(res.data.data[i]);
                  }
                  this.tableData = list;
                }
              }).catch (err => {
                alert(err)
      })
    },
    actCancelFollow() {
      if(this.user1_input === "" || this.user2_input === "") {
        alert("用户1ID和用户2ID不能为空！");
        return;
      }
      const data = {
        "id1": this.user1_input,
        "id2": this.user2_input
      };
      cancelFollow(data)
      // eslint-disable-next-line no-unused-vars
              .then(res => {
                if(res.data.msg === "error") {
                  alert("用户1或用户2不存在，请重新输入正确的用户ID！");
                } else {
                  alert("取关成功！\n" +
                          this.user1_input + "的得分由" + res.data["u1_old"] + "变为" + res.data["u1_new"] + "\n" +
                          this.user2_input + "的得分由" + res.data["u2_old"] + "变为" + res.data["u2_new"] + "\n");
                  let list = [];
                  for(let i in res.data.data){
                    list.push(res.data.data[i]);
                  }
                  this.tableData = list;
                }
              }).catch (err => {
        alert(err)
      })

    },
    actAddUser() {
      addUser()
      // eslint-disable-next-line no-unused-vars
              .then(res => {
                alert("该功能尚未开放，敬请期待~");
              }).catch (err => {
                alert(err)
              })
    },
    actRemoveUser() {
      if(this.user1_input === "") {
        alert("用户1ID不能为空！");
        return;
      }
      const data = {
        "id": this.user1_input
      };
      removeUser(data)
      // eslint-disable-next-line no-unused-vars
              .then(res => {
                if(res.data.msg === "error") {
                  alert("该用户不存在！请重新输入正确的用户ID！");
                } else {
                  alert("删除用户成功！");
                  let list = [];
                  for(let i in res.data.data){
                    list.push(res.data.data[i]);
                  }
                  this.tableData = list;
                }
              }).catch (err => {
        alert(err)
      })
    },
    actViewFollows() {
      if(this.user1_input === "") {
        alert("用户1ID不能为空！");
        return;
      }
      const data = {
        "id": this.user1_input
      };
      viewFollows(data)
      // eslint-disable-next-line no-unused-vars
              .then(res => {
                if(res.data.msg === "error") {
                  alert("该用户不存在！请重新输入正确的用户ID！");
                } else {
                  this.tableLabel = "ta关注的人";
                  this.tableData3 = [];
                  for(let i in res.data.data){
                    this.tableData3.push({"id":res.data.data[i]});
                  }
                }
              }).catch (err => {
        alert(err)
      })
    },
    actViewFuns() {
      if(this.user1_input === "") {
        alert("用户1ID不能为空！");
        return;
      }
      const data = {
        "id": this.user1_input
      };
      viewFans(data)
      // eslint-disable-next-line no-unused-vars
              .then(res => {
                if(res.data.msg === "error") {
                  alert("该用户不存在！请重新输入正确的用户ID！");
                } else {
                  this.tableLabel = "ta的粉丝";
                  this.tableData3 = [];
                  for(let i in res.data.data){
                    this.tableData3.push({"id":res.data.data[i]});
                  }
                }
              }).catch (err => {
        alert(err)
      })
    },
    actViewProfile() {
      if(this.user1_input === "") {
        alert("用户1ID不能为空！");
        return;
      }
      const data = {
        "id": this.user1_input
      };
      viewProfile(data)
      // eslint-disable-next-line no-unused-vars
              .then(res => {
                if(res.data.msg === "error") {
                  alert("该用户不存在！请重新输入正确的用户ID！");
                } else {
                  for(let i in this.tableData2){
                    this.tableData2[i].value = res.data.data[this.userProfileDict[this.tableData2[i].type]];
                  }
                }
              }).catch (err => {
        alert(err)
      })
    },
    actViewPosts() {
      alert("该功能尚未开放，敬请期待~");
      // const data = {
      //   "id": this.user1_input
      // };
      // viewPosts(data)
      // // eslint-disable-next-line no-unused-vars
      //         .then(res => {
      //           let list = [];
      //           for(let i in res.data.data){
      //             list.push(res.data.data[i]);
      //           }
      //           this.tableData4 = list[0];
      //         }).catch (err => {
      //   alert(err)
      // })
    },
    actStaticAnalyze() {
      staticAnalyze()
      // eslint-disable-next-line no-unused-vars
              .then(res=>{
                alert("静态分析完成！");
                let list = [];
                for(let i in res.data){
                  list.push(res.data[i]);
                }
                this.tableData = list[0];
              }).catch (err => {
                alert(err)
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.tablewrapper{
  /* text-align: center; */
  margin-top: 100px;
  margin-left:200px;
  margin-right:200px;
  /* background-color: red; */
}
</style>
