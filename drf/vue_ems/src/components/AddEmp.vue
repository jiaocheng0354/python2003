<template>
    <div id="wrap">
        <div id="top_content">
            <div id="header">
                <div id="rightheader">
                    <p>2009/11/20<br/></p>
                </div>
                <div id="topheader">
                    <h1 id="title"><a href="#">Main</a></h1>
                </div>
                <div id="navigation"></div>
            </div>
            <div id="content">
                <p id="whereami"></p>
                <h1>add Emp info:</h1>
                <table cellpadding="0" cellspacing="0" border="0"
                       class="form_table">
                    <tr>
                        <td valign="middle" align="right">name:</td>
                        <td valign="middle" align="left">
                            <input type="text" class="inputgri" name="name" v-model="name"/>
                        </td>
                    </tr>
                    <tr>
                        <td valign="middle" align="right">photo:</td>
                        <td valign="middle" align="left">
                            <input type="file" accept="image/png, image/jpeg, image/gif" name="photo" ref="photo"/>
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
                    <el-button type="warning" size="medium" round @click="add">填加</el-button>
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
        name: "AddEmp",
        data: function () {
            return {
                name: "",
                photo: "",
                salary: "",
                age: "",
            }
        },
        created() {
            let is_login = localStorage.getItem("username")
            if (!is_login) {
                this.$router.push('/login')
            }
        },
        methods: {
            add() {
                if (this.name == "") {
                    this.$message.error('姓名不能为空');
                    return true
                }
                console.log(this.$refs.photo.files[0]);
                let formData = new FormData();
                formData.append("name", this.name);
                formData.append("photo", this.$refs.photo.files[0]);
                formData.append("salary", this.salary);
                formData.append("age", this.age);
                this.$axios({
                    url: "http://127.0.0.1:8000/emp/",
                    method: "post",
                    data: formData,
                    headers: {
                        'content-type': 'multipart/form-data'
                    },
                }).then(res => {
                    if (res.data["message"]) {
                        this.$message('填加成功');
                        this.$router.push('/emplist')
                    } else {
                        this.$message('填加失败');
                    }
                }).catch(error => {
                    this.$message.error('填加失败');
                })
            }
        }
    }
</script>

<style scoped>

</style>
