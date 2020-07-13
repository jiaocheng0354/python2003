<template>
    <div class="box">
        <img src="../../static/image/1111.jpg" alt="">
        <div class="register">
            <div class="register_box">
                <div class="register-title">百知教育在线平台注册</div>
                <div class="inp">
                    <input v-model="phone" type="text" placeholder="手机号码" class="user">
                    <input v-model="password" type="password" placeholder="登录密码" class="user">
                    <div id="geetest"></div>
                    <div class="sms-box">
                        <input v-model="code" type="text" maxlength="4" placeholder="输入验证码" class="user">
                        <div class="sms-btn"><input type="button" @click="get_code" :disabled="flag"
                                                    :value="mag"></input></div>
                    </div>
                    <button class="register_btn" @click="register">注册</button>
                    <p class="go_login">已有账号
                        <!--                        <router-link to="/login">直接登录</router-link>-->
                        <router-link to="/login">直接登录</router-link>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "register",
        data() {
            return {
                phone: "",
                password: "",
                code: "",
                flag: false,
                mag: "发送验证码"
            }
        },
        methods: {
            register() {
                if (!/1[356789]\d{9}/.test(this.phone)) {
                    this.$message.error("手机号格式有误", "警告");
                    this.phone = ""
                    return true
                }
                if (this.password === "") {
                    this.$message.error("密码不能为空", "警告");
                    return true
                }
                if (!/[0-9]{4}/.test(this.code)) {
                    this.$message.error("验证码是4位小数", "警告");
                    this.code = ""
                    return true
                }
                this.$axios({
                    url: this.$settings.HOST + "user/register/",
                    method: "post",
                    data: {
                        phone: this.phone,
                        password: this.password,
                        code: this.code,
                    }
                }).then(res => {
                    console.log(res.data);
                    if (res.data["token"]) {
                        if (this.forget) {
                            localStorage["username"] = res.data.username
                            localStorage["token"] = res.data.token
                            localStorage["user_id"] = res.data.user_id
                            sessionStorage.removeItem("username")
                            sessionStorage.removeItem("token")
                            sessionStorage.removeItem("user_id")
                        } else {
                            sessionStorage["username"] = res.data.username
                            sessionStorage["token"] = res.data.token
                            sessionStorage["user_id"] = res.data.user_id
                            localStorage.removeItem("username")
                            localStorage.removeItem("token")
                            localStorage.removeItem("user_id")
                        }
                        this.$message("注册成功")
                        this.$router.push('/home')
                    }
                }).catch(error => {
                    this.$message.error(error.response.data["non_field_errors"][0]);
                    // console.log(error);
                })
            },
            get_code() {
                this.flag = true;
                //判断手机号格式
                if (!/1[356789]\d{9}/.test(this.phone)) {
                    this.$message.error("手机号格式有误", "警告");
                    this.phone = ""
                    this.flag = false;
                    return true
                }
                // 判断手机号是否注册
                this.$axios({
                    url: this.$settings.HOST + `user/verify/${this.phone}/`,
                    method: "get",
                }).then(res => {
                    console.log(res.data);
                    if (res.data["message"] == true) {
                        this.$message.error("手机号已注册")
                        this.flag = false;
                    }
                }).catch(error => {
                    // 发送间隔限制
                    let second = 60;
                    this.mag = `${second}后可以点击发送`;
                    let timer = setInterval(() => {
                        if (second <= 1) {
                            clearInterval(timer);
                            this.flag = false;
                            this.mag = `点击发送短信`
                        } else {
                            second--;
                            this.mag = `${second}后可以点击发送`;
                        }
                    }, 1000);
                    console.log("发送短信");
                    //请求发送短信
                    this.send_sms()
                })
                console.log("end ");
            },
            send_sms() {
                this.$axios({
                    url: this.$settings.HOST + `user/sms/${this.phone}/`,
                    method: "get",
                }).then(response => {
                    console.log(response.data);
                    this.$message(response.data["results"])
                    this.flag = false;
                }).catch(error => {
                    console.log(error);
                    this.$message.error("当前手机号已经发送过短信")
                })
            }
        }
    }
</script>

<style scoped>
    .box {
        width: 100%;
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .box img {
        width: 100%;
        min-height: 100%;
    }

    .box .register {
        position: absolute;
        width: 500px;
        height: 400px;
        top: -70px;
        left: 0;
        margin: auto;
        right: 0;
        bottom: 0;
    }

    .register .register-title {
        width: 100%;
        font-size: 24px;
        text-align: center;
        padding-top: 30px;
        padding-bottom: 30px;
        color: #4a4a4a;
        letter-spacing: .39px;
    }

    .register-title img {
        width: 190px;
        height: auto;
    }

    .register-title p {
        font-size: 18px;
        color: #fff;
        letter-spacing: .29px;
        padding-top: 10px;
        padding-bottom: 50px;
    }

    .register_box {
        width: 400px;
        height: auto;
        background: #fff;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
        border-radius: 4px;
        margin: 0 auto;
        padding-bottom: 40px;
    }

    .register_box .title {
        font-size: 20px;
        color: #9b9b9b;
        letter-spacing: .32px;
        border-bottom: 1px solid #e6e6e6;
        display: flex;
        justify-content: space-around;
        padding: 50px 60px 0 60px;
        margin-bottom: 20px;
        cursor: pointer;
    }

    .register_box .title span:nth-of-type(1) {
        color: #4a4a4a;
        border-bottom: 2px solid #84cc39;
    }

    .inp {
        width: 350px;
        margin: 0 auto;
    }

    .inp input {
        outline: 0;
        width: 100%;
        height: 45px;
        border-radius: 4px;
        border: 1px solid #d9d9d9;
        text-indent: 20px;
        font-size: 14px;
        background: #fff !important;
    }

    .inp input.user {
        margin-bottom: 16px;
    }

    .inp .rember {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        margin-top: 10px;
    }

    .inp .rember p:first-of-type {
        font-size: 12px;
        color: #4a4a4a;
        letter-spacing: .19px;
        margin-left: 22px;
        display: -ms-flexbox;
        display: flex;
        -ms-flex-align: center;
        align-items: center;
        /*position: relative;*/
    }

    .inp .rember p:nth-of-type(2) {
        font-size: 14px;
        color: #9b9b9b;
        letter-spacing: .19px;
        cursor: pointer;
    }

    .inp .rember input {
        outline: 0;
        width: 30px;
        height: 45px;
        border-radius: 4px;
        border: 1px solid #d9d9d9;
        text-indent: 20px;
        font-size: 14px;
        background: #fff !important;
    }

    .inp .rember p span {
        display: inline-block;
        font-size: 12px;
        width: 100px;
        /*position: absolute;*/
        /*left: 20px;*/

    }

    #geetest {
        margin-top: 20px;
    }

    .register_btn {
        width: 100%;
        height: 45px;
        background: #84cc39;
        border-radius: 5px;
        font-size: 16px;
        color: #fff;
        letter-spacing: .26px;
        margin-top: 30px;
    }

    .inp .go_login {
        text-align: center;
        font-size: 14px;
        color: #9b9b9b;
        letter-spacing: .26px;
        padding-top: 20px;
    }

    .inp .go_login span {
        color: #84cc39;
        cursor: pointer;
    }

    .sms-box {
        position: relative;
    }

    .sms-box .sms-btn input {
        width: 100%;
        border: 0px;
        height: 25px;
        font-size: 14px;
        color: #ffc210;
    }

    .sms-btn {
        letter-spacing: .26px;
        position: absolute;
        right: 16px;
        top: 10px;
        cursor: pointer;
        overflow: hidden;
        background: #fff;
        border-left: 1px solid #484848;
        /*padding-left: 16px;*/
        /*padding-bottom: 4px;*/
    }
</style>
