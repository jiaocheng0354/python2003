<template>
    <div id="wrap">
        <div id="top_content">
            <div id="header">
                <div id="rightheader">
                    <p>2009/11/20<br/></p>
                </div>
                <div id="topheader">
                    <h1 id="title"><a href="#">main</a></h1>
                </div>
                <div id="navigation"></div>
            </div>
            <div id="content">
                <p id="whereami"></p>
                <h1>注册</h1>
                <table cellpadding="0" cellspacing="0" border="0" class="form_table">
                    <tr>
                        <td valign="middle" align="right">用户名:</td>
                        <td valign="middle" align="left">
                            <input type="text" class="inputgri" name="username" v-model.trim="username"/>
                        </td>
                    </tr>
                    <tr>
                        <td valign="middle" align="right">真实姓名:</td>
                        <td valign="middle" align="left">
                            <input type="text" class="inputgri" name="name" v-model="name"/>
                        </td>
                    </tr>
                    <tr>
                        <td valign="middle" align="right">密码:</td>
                        <td valign="middle" align="left">
                            <input type="password" class="inputgri" name="pwd" v-model.trim="password"/>
                        </td>
                    </tr>
                    <tr>
                        <td valign="middle" align="right">性别:</td>
                        <td valign="middle" align="left">
                            男<input type="radio" class="inputgri" name="sex" v-model="sex" value="1" checked="checked" />
                            女<input type="radio" class="inputgri" name="sex" v-model="sex" value="0"/>
                        </td>
                    </tr>
                </table>
                <p><el-button type="warning" size="medium" round @click="register">注册</el-button></p>
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
        name: "Register",
        data: function () {
            return {
                username: "",
                name: "",
                password: "",
                sex: 1,
            }
        },
        methods: {
            register() {
                if (this.username == "") {
                    this.$message.error('用户名不能为空');
                    return true
                }
                if (this.name == "") {
                    this.$message.error('姓名不能为空');
                    return true
                }
                if (this.password == "") {
                    this.$message.error('密码不能为空');
                    return true
                }
                // 检测用户是否注册
                this.$axios({
                    url: "http://127.0.0.1:8000/user/" + this.username + "/",
                    method: "get",
                }).then(res => {
                    console.log(res.data["message"])
                    console.log(res.data["results"])
                    if (res.data["message"]) {
                        this.$message.error('用户名已存在');
                    } else {
                        //注册用户
                        this.$axios({
                            url: "http://127.0.0.1:8000/user/",
                            method: "post",
                            data: {
                                username: this.username,
                                name: this.name,
                                password: this.name,
                                sex: this.sex
                            }
                        }).then(response => {
                            if (response.data["message"]) {
                                this.$message('注册成功');
                                this.$router.push('/login')
                            } else {
                                this.$message('注册失败');
                            }
                        }).catch(error => {
                            this.$message('注册信息有误');
                            console.log(error);
                        })
                    }
                }).catch(error => {
                    console.log(error);
                })
            }
        }
    }
</script>

<style scoped>

</style>
