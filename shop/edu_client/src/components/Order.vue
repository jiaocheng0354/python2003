<template>
    <div class="cart">
        <Header/>
        <div class="cart-info">
            <h3 class="cart-top">购物车结算 <span>共{{ order_list.length }}门课程</span></h3>
            <div class="cart-title">
                <el-row>
                    <el-col :span="2">&nbsp;</el-col>
                    <el-col :span="10">课程</el-col>
                    <el-col :span="8">有效期</el-col>
                    <el-col :span="4">价格</el-col>
                </el-row>
            </div>
            <div class="cart-item" v-for="(value,index) in order_list" :key="index">
                <el-row>
                    <el-col :span="2" class="checkbox">&nbsp;&nbsp;</el-col>
                    <el-col :span="10" class="course-info">
                        <img :src="value.course_img" alt="">
                        <span>{{ value.name }}<br>
                        <u class="sale-type" v-show="value.discount_name">{{ value.discount_name }}</u></span>
                    </el-col>
                    <el-col :span="8" v-for=" (item,index) in value.expire_list" :key="index"
                            v-if="value.expire_id===item.id"><span>{{ item.expire_text }}</span></el-col>
                    <el-col :span="4" class="course-price">¥{{ value.real_price }}<br>原价{{ value.price }}</el-col>
                </el-row>
            </div>
            <div class="calc">
                <el-row class="pay-row">
                    <el-col :span="4" class="pay-col"><span class="pay-text">支付方式：</span></el-col>
                    <el-col :span="8">
                        <span class="alipay"><img src="../../static/image/alipay2.png" alt=""></span>
                        <!--<span class="alipay wechat"><img src="../../static/image/wechat.png" alt=""></span>-->
                    </el-col>
                    <el-col :span="8" class="count">实付款： <span>¥{{ total_price }}</span></el-col>
                    <el-col :span="4" class="cart-pay"><span @click="creat_order">支付宝支付</span></el-col>
                </el-row>
            </div>
        </div>
        <Fotter/>
    </div>
</template>

<script>
    import Header from './Header'
    import Fotter from './Fotter'

    export default {
        name: "Order",
        components: {
            Header, Fotter
        },
        data() {
            return {
                total_price: 0,
                alipay: 1,
                order_list: {expire_list: {},},
            }
        },
        methods: {
            is_login() {
                this.token = localStorage.token || sessionStorage.token;
                if (this.token) {
                    return false;
                } else {
                    this.$message("请先登陆后订购");
                    this.$router.push('/home')
                }
            },
            order() {
                this.is_login();
                this.$axios.get(this.$settings.HOST + "cart/list/order/", {
                    headers: {
                        "Authorization": "jwt " + this.token,
                    }
                }).then(res => {
                    console.log(res);
                    this.order_list = res.data["order"]
                    this.total_price = res.data["count_price"]
                }).catch(error => {
                })
            },
            creat_order() {
                this.$axios({
                    url: this.$settings.HOST + 'order/creat/',
                    method: 'post',
                    data: {
                        pay_type: 1,
                    },
                    config: {
                        headers: {
                            "Authorization": "jwt " + this.token,
                        },
                    }
                }).then(res => {
                    this.$message.success("定单成功生成");
                    console.log(res.data["order_number"]);
                    // this.order_list = ""
                    // this.total_price = "0.00"
                    this.$axios({
                        url: this.$settings.HOST + 'payments/pay/',
                        method: 'get',
                        params: {
                            order_number: res.data["order_number"],
                        },
                        config: {
                            headers: {
                                "Authorization": "jwt " + this.token,
                            },
                        }
                    }).then(res=>{
                        location.href = res.data
                    }).catch(error=>{
                        console.log(error);
                    })
                }).catch(error => {
                })
            }
        },
        created() {
            this.order();
        }
    }

</script>

<style scoped>
    .cart {
        margin-top: 80px;
    }

    .cart-info {
        overflow: hidden;
        width: 1200px;
        margin: auto;
        min-height: 500px;
    }

    .cart-top {
        font-size: 18px;
        color: #666;
        margin: 25px 0;
        font-weight: normal;
    }

    .cart-top span {
        font-size: 12px;
        color: #d0d0d0;
        display: inline-block;
    }

    .cart-title {
        background: #F7F7F7;
        height: 50px;
        line-height: 50px;
    }

    .sale-type {
        padding: 4px 10px;
        height: 16px;
        line-height: 16px;
        font-size: 10px;
        color: #fff;
        text-align: center;
        margin-right: 8px;
        background: #fa6240;
        border: 1px solid #fa6240;
        border-radius: 10px 0 10px 0;
        float: left;
    }

    .calc {
        margin-top: 25px;
        margin-bottom: 40px;
    }

    .calc .count {
        text-align: right;
        margin-right: 10px;
        vertical-align: middle;
    }

    .calc .count span {
        font-size: 36px;
        color: #333;
    }

    .calc .cart-pay {
        margin-top: 5px;
        width: 110px;
        height: 38px;
        outline: none;
        border: none;
        color: #fff;
        line-height: 38px;
        background: #ffc210;
        border-radius: 4px;
        font-size: 16px;
        text-align: center;
        cursor: pointer;
    }

    .cart-item {
        height: 120px;
        line-height: 120px;
        margin-bottom: 30px;
    }

    .course-info img {
        display: inline-block;
        width: 175px;
        height: 115px;
        margin-right: 20px;
        vertical-align: middle;
    }

    .course-info span {
        display: inline-block;
        padding: 36px 0;
        width: 175px;
        height: 75px;
        line-height: 30px;
        margin-right: 35px;
        vertical-align: middle;
    }

    .alipay {
        display: inline-block;
        height: 48px;
    }

    .alipay img {
        height: 100%;
        width: auto;
    }

    .pay-text {
        display: block;
        text-align: right;
        width: 160px;
        height: 100%;
        line-height: 100%;
        vertical-align: middle;
        margin-top: 20px;
    }

    .course_name, .real_price, .original_price {
        display: inline-block;
        line-height: 140%;
    }

    .course_name .discount {
        color: #ffc210;
    }

    .original_price {
        color: #9b9b9b;
    }

    .course-price {
        padding: 36px 0;
        line-height: 24px;
    }

    /*优惠券相关的样式*/
    .coupon-box {
        text-align: left;
        padding-bottom: 22px;
        padding-left: 30px;
        border-bottom: 1px solid #e8e8e8;
    }

    .coupon-box::after {
        content: "";
        display: block;
        clear: both;
    }

    .icon-box {
        float: left;
    }

    .icon-box .select-coupon {
        float: left;
        color: #666;
        font-size: 16px;
    }

    .icon-box::after {
        content: "";
        clear: both;
        display: block;
    }

    .select-icon {
        width: 20px;
        height: 20px;
        float: left;
    }

    .select-icon img {
        max-height: 100%;
        max-width: 100%;
        margin-top: 2px;
        transform: rotate(-90deg);
        transition: transform .5s;
    }

    .is_show_select {
        transform: rotate(0deg) !important;
    }

    .coupon-num {
        height: 22px;
        line-height: 22px;
        padding: 0 5px;
        text-align: center;
        font-size: 12px;
        float: left;
        color: #fff;
        letter-spacing: .27px;
        background: #fa6240;
        border-radius: 2px;
        margin-left: 20px;
    }

    .sum-price-wrap {
        float: right;
        font-size: 16px;
        color: #4a4a4a;
        margin-right: 45px;
    }

    .sum-price-wrap .sum-price {
        font-size: 18px;
        color: #fa6240;
    }

    .no-coupon {
        text-align: center;
        width: 100%;
        padding: 50px 0px;
        align-items: center;
        justify-content: center; /* 文本两端对其 */
        border-bottom: 1px solid rgb(232, 232, 232);
    }

    .no-coupon-tips {
        font-size: 16px;
        color: #9b9b9b;
    }

    .credit-box {
        height: 30px;
        margin-top: 40px;
        display: flex;
        align-items: center;
        justify-content: flex-end
    }

    .my_el_check_box {
        position: relative;
    }

    .my_el_checkbox {
        margin-right: 10px;
        width: 16px;
        height: 16px;
    }

    .discount {
        overflow: hidden;
    }

    .discount-num1 {
        color: #9b9b9b;
        font-size: 16px;
        margin-right: 45px;
    }

    .discount-num2 {
        margin-right: 45px;
        font-size: 16px;
        color: #4a4a4a;
    }

    .sun-coupon-num {
        margin-right: 45px;
        margin-bottom: 43px;
        margin-top: 40px;
        font-size: 16px;
        color: #4a4a4a;
        display: inline-block;
        float: right;
    }

    .sun-coupon-num span {
        font-size: 18px;
        color: #fa6240;
    }

    .coupon-list {
        margin: 20px 0;
    }

    .coupon-list::after {
        display: block;
        content: "";
        clear: both;
    }

    .coupon-item {
        float: left;
        margin: 15px 8px;
        width: 190px;
        height: 100px;
        padding: 5px;
        background-color: #fa3030;
        cursor: pointer;
    }

    .coupon-list .active {
        background-color: #fa9000;
    }

    .coupon-list .disable {
        cursor: not-allowed;
        background-color: #fa6060;
    }

    .coupon-condition {
        font-size: 12px;
        text-align: center;
        color: #fff;
    }

    .coupon-name {
        color: #fff;
        font-size: 24px;
        text-align: center;
    }

    .coupon-time {
        text-align: left;
        color: #fff;
        font-size: 12px;
    }

    .unselect {
        margin-left: 0px;
        transform: rotate(-90deg);
    }

    .is_selected {
        transform: rotate(-1turn) !important;
    }

</style>
