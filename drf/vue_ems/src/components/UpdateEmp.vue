<template>
    <div id="wrap">
        <div id="top_content">
            <div id="header">
                <div id="rightheader">
                    <p>
                        2009/11/20
                        <br/>
                    </p>
                </div>
                <div id="topheader">
                    <h1 id="title">
                        <a href="#">Main</a>
                    </h1>
                </div>
                <div id="navigation">
                </div>
            </div>
            <div id="content">
                <p id="whereami">
                </p>
                <h1>
                    update Emp info:
                </h1>
                <table cellpadding="0" cellspacing="0" border="0" class="form_table">
                    <tr>
                        <td valign="middle" align="right">id:</td>
                        <td valign="middle" align="left">
                            {{ id }}
                        </td>
                    </tr>
                    <tr>
                        <td valign="middle" align="right">name:</td>
                        <td valign="middle" align="left">
                            <input type="text" class="inputgri" name="name" v-model="name"/>
                        </td>
                    </tr>
                    <tr>
                        <td valign="middle" align="right">photo:</td>
                        <td valign="middle" align="left">
                            <input type="file" name="photo" accept="image/png, image/jpeg, image/gif" ref="photo"/><img :src="photo" alt="" width="35"
                                                                              height="35">
                        </td>
                    </tr>
                    <tr>
                        <td valign="middle" align="right">salary:</td>
                        <td valign="middle" align="left">
                            <input type="number" class="inputgri" name="salary"
                                   v-model="salary"/>
                        </td>
                    </tr>
                    <tr>
                        <td valign="middle" align="right">age:</td>
                        <td valign="middle" align="left">
                            <input type="number" class="inputgri" name="age"  v-model="age"/>
                        </td>
                    </tr>
                </table>
                <p>
                    <el-button type="primary" size="medium" @click="edit_emp" round>编辑</el-button>
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
        name: "UpdateEmp",
        data: function () {
            return {
                id: "",
                name: "",
                photo: "",
                salary: "",
                age: "",
                emp: [],
            }
        },
        created() {
            let is_login = localStorage.getItem("username")
            if (!is_login) {
                this.$router.push('/login')
            }
            let emp_url = "http://127.0.0.1:8000/emp/" + this.$route.params.id + "/"
            console.log(emp_url);
            this.$axios({
                url: emp_url,
                method: "get",
            }).then(res => {
                if (res.data["message"]) {
                    console.log(res);
                    this.emp = res.data["results"]
                    this.id = this.emp["id"]
                    this.name = this.emp["name"]
                    this.photo = this.emp["photo"]
                    this.salary = this.emp["salary"]
                    this.age = this.emp["age"]
                } else {
                    this.$message('修改记录不存在');
                }
            }).catch(error => {
                this.$message.error('修改记录不存在');
            })
        },
        methods: {
            edit_emp() {
                if (this.name == "") {
                    this.$message.error('姓名不能为空');
                    return true
                }
                console.log(this.$refs.photo.files[0]);
                let formData = new FormData();
                if (typeof (this.$refs.photo.files[0]) != "undefined") {
                    formData.append("photo", this.$refs.photo.files[0]);
                }
                formData.append("name", this.name);
                formData.append("salary", this.salary);
                formData.append("age", this.age);
                this.$axios({
                    url: "http://127.0.0.1:8000/emp/" + this.$route.params.id + "/",
                    method: "patch",
                    data: formData,
                    headers: {
                        'content-type': 'multipart/form-data'
                    },
                }).then(res => {
                    if (res.data["message"]) {
                        this.$message('修改成功');
                        this.$router.push('/emplist')
                    } else {
                        this.$message('修改失败');
                    }
                }).catch(error => {
                    this.$message.error('修改失败');
                })
            }
        }
    }
</script>

<style scoped>

</style>
