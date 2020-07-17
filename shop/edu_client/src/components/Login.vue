<template>
    <div class="login box">
        <img src="../../static/image/1111.jpg" alt="">
        <div class="login">
            <!--<div class="login-title">-->
            <!--&lt;!&ndash;<img src="../../static/image/logo.png" alt="">&ndash;&gt;-->
            <!--<p>百知教育给你最优质的学习体验!</p>-->
            <!--</div>-->
            <div class="login_box">
                <div :class="title">
                    <span @click="login_choose(true)">密码登录</span>
                    <span @click="login_choose(false)">短信登录</span>
                </div>
                <div class="inp" v-if="choose">
                    <input type="text" placeholder="用户名 / 手机号码" class="user" v-model="username">
                    <input type="password" name="" class="pwd" placeholder="密码" v-model="password">
                    <div id="geetest2"></div>
                    <div class="rember">
                        <p>
                            <input type="checkbox" v-model="forget" class="no"/>
                            <span>记住密码</span>
                        </p>
                        <p>忘记密码</p>
                    </div>
                    <div id="popup-captcha"></div>
                    <button class="login_btn btn btn-primary" @click="login">登录</button>
                    <!--<button class="login_btn btn btn-primary" @click="login_captcha">登录</button>-->
                    <p class="go_login">没有账号
                        <router-link to="/user/register">立即注册</router-link>
                    </p>
                </div>
                <div class="inp" v-else>
                    <input type="text" placeholder="手机号码" v-model="phone" class="user">
                    <!--<input type="text" class="pwd" placeholder="短信验证码">-->
                    <!--<button id="get_code" class="btn btn-primary">获取验证码</button>-->
                    <div class="sms-box">
                        <input v-model="code" type="text" maxlength="4" placeholder="输入验证码" class="user">
                        <div class="sms-btn"><input type="button" @click="get_code" :disabled="flag"
                                                    :value="mag"></input></div>
                    </div>
                    <button class="login_btn" @click="sms_login">登录</button>
                    <span class="go_login">没有账号
                    <router-link to="/user/register/">立即注册</router-link> </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Login",
        data() {
            return {
                username: "",
                phone: "",
                password: "",
                code: "",
                forget: false,
                choose: true,
                title: "title",
                flag: false,
                mag: "获取验证码"
            }
        },
        methods: {
            get_code() {
                this.flag = true;
                //判断手机号格式
                if (!/1[356789]\d{9}/.test(this.phone)) {
                    this.$message.error("手机号格式有误", "警告");
                    this.phone = "";
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
                    }
                }).catch(error => {
                    this.$message.error("手机号没注册。请先注册，再登陆")
                    this.flag = false;

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
            },
            login_choose(flag1) {
                this.choose = flag1
                if (flag1) {
                    this.title = "title"
                } else {
                    this.title = "title1"
                }
            },
            login_captcha() {
                this.$axios({
                    url: this.$settings.HOST + "user/captcha/",
                    method: 'get',
                    params: {
                        username: this.username,
                    }
                }).then(res => {
                    console.log(res.data);
                    // let data = JSON.parse(res.data["results"]);
                    let data = JSON.parse(res.data);
                    console.log(data.gt);
                    initGeetest({
                        gt: data.gt,
                        challenge: data.challenge,
                        product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                        width: "100%",
                        offline: !data.success, // 表示用户后台检测极验服务器是否宕机，一般不需要关注
                        new_captcha: data.new_captcha
                    }, this.handlerPopup);

                }).catch(error => {
                    console.log(error);
                    this.$message.error("用户名或密码错误");
                })
            },
            handlerPopup(captchaObj) {
                captchaObj.onSuccess(function () {
                    let _self = this;
                    console.log(captchaObj);
                    let validate = captchaObj.getValidate();
                    console.log("1111111",validate);
                    _self.$axios({
                        url: "http://api.shop.com:9000/user/captcha/",
                        method: "post",
                        data: {
                            geetest_challenge: validate.geetest_challenge,
                            geetest_validate: validate.geetest_validate,
                            geetest_seccode: validate.geetest_seccode
                        }
                    }).then(response => {
                        console.log(response.data);
                        if (response.data.results === "true") {
                            // 验证码验证成功  登录
                            self.user_login()
                        }
                    }).catch(error => {
                        console.log(error);
                    });
                    // _self.$axios({
                    //     url: "http://api.shop.com:9000/user/captcha/",
                    //     method:"post"
                    // }).then(res=>{
                    //
                    // }).catch(error=>{
                    //
                    // })
                });
                document.getElementById("geetest2").innerHTML = "";
                captchaObj.appendTo("#geetest2");
            },

            login() {
                if (this.username === "") {
                    this.$message.error("用户名不能为空", "警告");
                    return true
                }
                if (this.password === "") {
                    this.$message.error("密码不能为空", "警告");
                    return true
                }
                this.$axios({
                    url: this.$settings.HOST + "user/login/",
                    method: "post",
                    data: {
                        username: this.username,
                        password: this.password,
                    }
                }).then(res => {
                    console.log(res.data);
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
                    this.$router.push('home')
                }).catch(error => {
                    this.$message.error("用户名或密码错误");
                    console.log(error);
                })
            },
            sms_login() {
                if (this.phone === "") {
                    this.$message.error("手机号码不能为空", "警告");
                    return true
                }
                if (this.code === "") {
                    this.$message.error("短信验证码不能为空", "警告");
                    return true
                }
                this.$axios({
                    url: this.$settings.HOST + "user/login/",
                    method: "post",
                    data: {
                        username: this.phone,
                        password: this.code,
                    }
                }).then(res => {
                    console.log(res.data);
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
                    this.$router.push('home')
                }).catch(error => {
                    this.$message.error("登陆失败");
                    console.log(error.response);
                })
            },
        }
    }
</script>

<style scoped>
    /** {*/
    /*touch-action: pan-y;*/
    /*}*/

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

    .box .login {
        position: absolute;
        width: 500px;
        height: 400px;
        top: -70px;
        left: 0;
        margin: auto;
        right: 0;
        bottom: 0;
    }

    .login .login-title {
        width: 100%;
        text-align: center;
    }

    .login-title img {
        width: 190px;
        height: auto;
    }

    .login-title p {
        font-size: 18px;
        color: #fff;
        letter-spacing: .29px;
        padding-top: 10px;
        padding-bottom: 50px;
    }

    .login_box {
        width: 400px;
        height: auto;
        background: #fff;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
        border-radius: 4px;
        margin: 0 auto;
        padding-bottom: 40px;
    }

    .login_box .title, .login_box .title1 {
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

    .login_box .title span:nth-of-type(1) {
        color: #4a4a4a;
        border-bottom: 2px solid #84cc39;
    }

    .login_box .title1 span:nth-of-type(2) {
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
        margin-top: 15px;
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
        height: 25px;
        border-radius: 4px;
        border: 1px solid #d9d9d9;
        text-indent: 20px;
        font-size: 14px;
        background: #fff !important;
        margin-right: 10px;
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

    .login_btn {
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
