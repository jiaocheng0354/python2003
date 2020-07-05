<template>
    <div id="wrap">
        <div id="top_content">
            <div id="header">
                <div id="rightheader">
                    <p> 2009/11/20<br/></p>
                </div>
                <div id="topheader">
                    <h1 id="title">
                        <a href="#">main</a>
                    </h1>
                </div>
                <div id="navigation">
                </div>
            </div>
            <div id="content">
                <p id="whereami"></p>
                <h1> login </h1>
                <table cellpadding="0" cellspacing="0" border="0" class="form_table">
                    <tr>
                        <td valign="middle" align="right"> username:
                        </td>
                        <td valign="middle" align="left">
                            <input type="text" class="inputgri" name="name" v-model.trim="username"/>
                        </td>
                    </tr>
                    <tr>
                        <td valign="middle" align="right"> password:
                        </td>
                        <td valign="middle" align="left">
                            <input type="password" class="inputgri" name="pwd" v-model.trim="password"/>
                        </td>
                    </tr>
                </table>
                <p>&nbsp;&nbsp;
                    <el-button type="warning" size="medium" round @click="login">登陆</el-button>
                    &nbsp;&nbsp;
                    <router-link to="/register"><el-button round size="small">注册</el-button></router-link>
                </p>
            </div>
        </div>
        <div id="footer">
            <div id="footer_bg">
                ABC@126.com
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "login",
        data: function () {
            return {
                username: "",
                password: "",
            }
        },
        methods: {
            login() {
                if (this.username == "") {
                    this.$message.error('用户名不能为空');
                    return true
                }
                if (this.password == "") {
                    this.$message.error('蜜码不能为空');
                    return true
                }
                this.$axios({
                    url: "http://127.0.0.1:8000/user/login/",
                    method: "post",
                    data: {
                        username: this.username,
                        password: this.password,
                    }
                }).then(res => {
                    console.log(res.data["results"])
                    if (res.data["message"]) {
                        localStorage["username"] = this.username
                        this.$message('登陆成功');
                        this.$router.push("/emplist")
                    } else {
                        this.$message.error('用户名或密码错误');
                    }
                }).catch(error => {
                    console.log(error);
                })
            },
        }
    }
</script>

<style scoped>

</style>
