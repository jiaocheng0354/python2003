<template>
    <div class="cart_item" v-show="is_show">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox" @change="change_select()" v-model="course.selected"></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img :src="course.course_img" alt="">
            <span><router-link :to="'/detail/'+ course.id">{{ course.name }}</router-link></span>
        </div>
        <div class="cart_column column_3">
            <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                <el-option v-for="(value,index) in course.expire_list" :label="value.expire_text" :value="value.id"
                           :key="index"></el-option>
            </el-select>
        </div>
        <div class="cart_column column_4">¥{{course.real_price}}</div>
        <div class="cart_column column_4"><a href="javascript:void(0)" @click="del(course.id)">删除</a></div>
    </div>
</template>

<script>
    export default {
        name: "cart",
        props: ["course"],
        data() {
            return {
                expire: "",
                is_show: true,
                token: localStorage.token || sessionStorage.token,
            }
        },
        watch: {
            'course.expire_id'() {
                this.change_expire();
            }
        },
        methods: {
            change_expire(id) {
                this.$axios({
                    url: this.$settings.HOST + 'cart/list/',
                    method: "put",
                    data: {
                        course_id: this.course.id,
                        expire_id: this.course.expire_id
                    },
                    config: {
                        "Authorization": "auth " + this.token
                    }
                }).then(res => {
                    console.log(res);
                    this.course.real_price = res.data["real_price"]
                    this.$store.commit("money_cart", res.data["count_price"])
                }).catch(error => {
                })
            },
            change_select() {
                this.$axios({
                    url: this.$settings.HOST + 'cart/list/',
                    method: "patch",
                    data: {
                        course_id: this.course.id,
                        select: this.course.selected
                    },
                    config: {
                        "Authorization": "auth " + this.token
                    }
                }).then(res => {
                    this.$store.commit("money_cart", res.data[1])
                }).catch(error => {
                })
            },
            del(id) {
                this.$axios({
                    url: this.$settings.HOST + 'cart/list/',
                    method: "delete",
                    data: {
                        course_id: id,
                    },
                    config: {
                        "Authorization": "auth " + this.token
                    }
                }).then(res => {
                    this.is_show = false
                    this.$store.commit("add_cart", res.data[0].cart_length)
                    this.$store.commit("money_cart", res.data[1])
                    // console.log(res.data.cart_length);
                }).catch(error => {
                })
            }
        }
    }
</script>

<style scoped>
    .cart_item::after {
        content: "";
        display: block;
        clear: both;
    }

    .cart_column {
        float: left;
        height: 170px;
    }

    .cart_item .column_1 {
        width: 88px;
        position: relative;
    }

    .my_el_checkbox {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        top: 0;
        margin: auto;
        width: 16px;
        height: 16px;
    }

    .cart_item .column_2 {
        padding: 37px 10px;
        width: 520px;
        height: 96px;
    }

    .cart_item .column_2 img {
        width: 175px;
        height: 95px;
        margin-right: 35px;
        vertical-align: middle;
    }

    .cart_item .column_3 {
        width: 197px;
        position: relative;
    }

    .my_el_select {
        width: 117px;
        height: 28px;
        position: absolute;
        top: -14px;
        bottom: 0;
        margin: auto;
        color: #333333;
        border: #b4b4b4 1px solid;
    }

    .cart_item .column_4 {
        padding: 37px 10px;
        height: 96px;
        width: 142px;
        line-height: 76px;
    }

</style>
