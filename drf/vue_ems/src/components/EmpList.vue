<template>
    <div id="wrap">
        <div id="top_content">
            <div id="header">
                <div id="rightheader">
                    <p>
                        2009/11/20<br/>
                        <a href="javascript:;" @click="out">安全退出</a>&nbsp;
                    </p>
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
                <p id="whereami">
                </p>
                <h1>
                    Welcome! {{ username }}
                </h1>
                <table class="table">
                    <tr class="table_header">
                        <td width="8%">ID</td>
                        <td>Name</td>
                        <td>Photo</td>
                        <td>Salary</td>
                        <td>Age</td>
                        <td width="10%">Operation</td>
                    </tr>
                    <tr class="row1" v-for="value,index in emp" :key="value.id">
                        <td>{{ value.id }}</td>
                        <td>{{ value.name }}</td>
                        <td><img :src="value.photo" alt="" width="35" height="35"></td>
                        <td>{{ value.salary }}</td>
                        <td>{{ value.age }}</td>
                        <td>
                            <router-link :to="'/updatte/'+value.id ">
                                <el-button type="primary" icon="el-icon-edit" size="mini" circle></el-button>
                            </router-link>
                            <el-button type="danger" icon="el-icon-delete" size="mini" circle
                                       @click="del_emp(value.id)">
                            </el-button>
                        </td>
                    </tr>
                </table>
                <p>
                    <RouterLink to="/addemp">
                        <el-button size="mini" type="warning">填加</el-button>
                    </RouterLink>
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
        name: "EmpList",
        data: function () {
            return {
                emp: [],
                username: "",
            }
        },
        created() {
            let is_login = localStorage.getItem("username")
            if (!is_login) {
                this.$router.push('/login')
            }
            this.username = is_login
            this.$axios({
                url: "http://127.0.0.1:8000/emp/",
                method: "get",
            }).then(res => {
                console.log(res.data);
                this.emp = res.data["results"]
            }).catch(error => {
                this.$message.error('无记录');
            })
        },
        methods: {
            del_emp(id) {
                this.$axios({
                    url: "http://127.0.0.1:8000/emp/" + id + "/",
                    method: "delete",
                    data: {
                        // photo: "",
                        salary: this.salary,
                        age: this.age,
                    },
                }).then(res => {
                    if (res.data["message"]) {
                        this.emp = res.data["results"]
                        this.$message('删除成功');
                    } else {
                        this.$message('删除失败');
                    }
                }).catch(error => {
                    this.$message.error('删除失败');
                })
            },
            out() {
                localStorage.removeItem("username");
                this.$router.push('/login')
            }
        }
    }
</script>

<style scoped>

</style>
