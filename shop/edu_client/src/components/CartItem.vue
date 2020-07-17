<template>
    <div class="cart_item" v-show="is_show">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox"  v-model="course.selected"></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img :src="course.course_img" alt="">
            <span><router-link :to="'/course/detail/'+ course.id">{{ course.name }}</router-link></span>
        </div>
        <div class="cart_column column_3">
            <el-select v-model="expire" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                <el-option label="1个月有效" value="30" key="30"></el-option>
                <el-option label="2个月有效" value="60" key="60"></el-option>
                <el-option label="3个月有效" value="90" key="90"></el-option>
                <el-option label="永久有效" value="10000" key="10000"></el-option>
            </el-select>
        </div>
        <div class="cart_column column_4">¥{{course.price}}</div>
        <div class="cart_column column_4" @click="del(course.id)">删除</div>
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
            'course.selected'() {
                this.change_select()
            }
        },
        methods: {
            change_select() {
                this.$axios({
                    url: this.$settings.HOST + 'cart/list/',
                    method: "patch",
                    data:{
                        course_id: this.course.id,
                        select: this.course.selected
                    },
                    config:{
                        "Authorization": "auth " + this.token
                    }
                }).then(res=>{
                }).catch(error=>{})
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
                    this.$store.commit("add_cart", res.data.cart_length)
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
        padding-left: 10px;
    }

    .my_el_select {
        width: 117px;
        height: 28px;
        position: absolute;
        top: 0;
        bottom: 0;
        margin: auto;
    }

    .cart_item .column_4 {
        padding: 37px 10px;
        height: 96px;
        width: 142px;
        line-height: 76px;
    }

</style>
