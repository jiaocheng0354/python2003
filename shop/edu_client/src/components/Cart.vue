<template>
    <div class="cart">
        <Header></Header>
        <div class="cart_info">
            <div class="cart_title">
                <span class="text">我的购物车</span>
                <span class="total">共{{ cart_list.length }}门课程</span>
            </div>
            <div class="cart_table">
                <div class="cart_head_row">
                    <span class="doing_row"></span>
                    <span class="course_row">课程</span>
                    <span class="expire_row">有效期</span>
                    <span class="price_row">单价</span>
                    <span class="do_more">操作</span>
                </div>
                <div class="cart_course_list">
                    <CartItem v-for="(course,index) in cart_list" :key="index" :course="course"></CartItem>
                </div>
                <div class="cart_footer_row">
                    <span class="cart_select">
                        <el-checkbox @change="all_check()" v-model="checked"></el-checkbox>
                       </span><span class="all_select">全选</span>
                    <span class="cart_delete"><i class="el-icon-delete"></i> <span
                        @click="select_del()">删除</span></span>
                    <router-link to="/order"><span class="goto_pay">去结算</span></router-link>
                    <span class="cart_total">总计：¥{{ $store.state.count_price }}</span>
                </div>
            </div>
        </div>
        <Fotter></Fotter>
    </div>
</template>

<script>
    import Header from "./Header";
    import Fotter from "./Fotter";
    import CartItem from "./CartItem";

    export default {
        name: "Cart",
        components: {
            CartItem, Header, Fotter
        },
        data() {
            return {
                cart_list: [],
                checked: true,
            }
        },
        watch: {
            'cart_list'() {
                this.check_sync();
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
            cart() {
                this.is_login();
                console.log(this.token);
                this.$axios.get(this.$settings.HOST + "cart/list/", {
                    config: {
                        headers: {
                            "Authorization": "jwt " + this.token,
                        },
                    }
                }).then(res => {
                    this.cart_list = res.data[0]
                    this.$store.commit("add_cart", this.cart_list.length)
                    this.$store.commit("money_cart", res.data[1])
                }).catch(error => {
                })
            },
            check_sync() {
                let obj = this.cart_list;
                for (let val of Object.keys(obj)) {
                    if (!obj[val]["selected"]) {
                        this.checked = false;
                    }
                }
            },
            all_check() {
                this.$axios({
                    url: this.$settings.HOST + 'cart/list/',
                    method: "patch",
                    data: {
                        course_id: 0,
                        select: this.checked,
                    },
                    config: {
                        headers: {
                            "Authorization": "jwt " + this.token,
                        },
                    }
                }).then(res => {
                    this.cart_list = res.data[0]
                    this.$store.commit("money_cart", res.data[1])
                }).catch(error => {
                })
            },
            select_del() {
                this.$axios({
                    url: this.$settings.HOST + 'cart/list/',
                    method: "delete",
                    data: {
                        course_id: 0,
                    },
                    config: {
                        headers: {
                            "Authorization": "jwt " + this.token,
                        },
                    }
                }).then(res => {
                    this.cart_list = res.data[0]
                    this.$store.commit("add_cart", res.data[0].length)
                    this.$store.commit("money_cart", res.data[1])
                }).catch(error => {
                })
            }
        },
        created() {
            this.cart();
        }

    }
</script>

<style scoped>
    .cart_info {
        width: 1200px;
        margin: 0 auto 200px;
    }

    .cart_title {
        margin: 25px 0;
    }

    .cart_title .text {
        font-size: 18px;
        color: #666;
    }

    .cart_title .total {
        font-size: 12px;
        color: #d0d0d0;
    }

    .cart_table {
        width: 1170px;
    }

    .cart_table .cart_head_row {
        background: #F7F7F7;
        width: 100%;
        height: 80px;
        line-height: 80px;
        padding-right: 30px;
    }

    .cart_table .cart_head_row::after {
        content: "";
        display: block;
        clear: both;
    }

    .cart_table .cart_head_row .doing_row,
    .cart_table .cart_head_row .course_row,
    .cart_table .cart_head_row .expire_row,
    .cart_table .cart_head_row .price_row,
    .cart_table .cart_head_row .do_more {
        padding-left: 10px;
        height: 80px;
        float: left;
    }

    .cart_table .cart_head_row .doing_row {
        width: 78px;
    }

    .cart_table .cart_head_row .course_row {
        width: 530px;
    }

    .cart_table .cart_head_row .expire_row {
        width: 188px;
    }

    .cart_table .cart_head_row .price_row {
        width: 162px;
    }

    .cart_table .cart_head_row .do_more {
        width: 162px;
    }

    .cart_footer_row {
        padding-left: 30px;
        background: #F7F7F7;
        width: 100%;
        height: 80px;
        line-height: 80px;
    }

    .cart_footer_row .cart_select span {
        margin-left: -7px;
        font-size: 18px;
        color: #666;
    }

    .cart_footer_row .cart_delete {
        margin-left: 58px;
    }

    .all_select {
        margin-left: 16px;
    }

    .cart_delete .el-icon-delete {
        font-size: 18px;
    }

    .cart_delete span {
        margin-left: 15px;
        cursor: pointer;
        font-size: 18px;
        color: #666;
    }

    .cart_total {
        float: right;
        margin-right: 62px;
        font-size: 18px;
        color: #666;
    }

    .goto_pay {
        float: right;
        width: 159px;
        height: 80px;
        outline: none;
        border: none;
        background: #ffc210;
        font-size: 18px;
        color: #fff;
        text-align: center;
        cursor: pointer;
    }
</style>
