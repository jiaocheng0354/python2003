<template>
    <div class="course">
        <Header></Header>
        <div class="main">
            <!-- 筛选条件 -->
            <div class="condition">
                <ul class="cate-list">
                    <li class="title">课程分类:</li>
                    <li @click="cate(0)" :class="category===0?'this':''">全部</li>
                    <li v-for="(value,indes) in category_list" @click="cate(value.id)"
                        :class="category===value.id?'this':''">
                        {{ value.name }}
                    </li>
                </ul>

                <div class="ordering">
                    <ul>
                        <li class="title">筛&nbsp;  &nbsp;&nbsp;&nbsp;选:</li>
                        <li class="default " @click="order('id')" :class="this.filters.orders  ==='id'? 'this':''">默认
                        </li>
                        <li class="hot " @click="order('students')"
                            :class="this.filters.orders  ==='students'? 'this':''">人气
                        </li>
                        <li class="price " @click="order('price')" :class="this.filters.orders  ==='price'? 'this':''">
                            价格
                        </li>

                    </ul>
                    <p class="condition-result">共{{ count }}个课程</p>
                </div>

            </div>
            <!-- 课程列表 -->
            <div class="course-list">
                <div class="course-item" v-for="(value,index) in course_list" :key="index">
                    <div class="course-image">
                        <router-link :to="'/detail/'+value.id">
                        <img :src="value.course_img" alt="">
                        </router-link>
                    </div>
                    <div class="course-info">
                        <h3>
                            <router-link :to="'/detail/'+value.id">{{ value.name }}</router-link>
                            <span><img src="/static/image/avatar1.svg" alt="">{{ value.students }}人已加入学习</span>
                        </h3>
                        <p class="teather-info">{{ value.teacher["name"] }} {{ value.teacher["title"] }}
                            <span>共{{ value.lessons }}课时/{{ value.pub_lessons===value.lessons?'更新完成':'已更新'+value.pub_lessons+'课时' }}</span>
                        </p>
                        <ul class="lesson-list">
                            <li v-for="lesson in value.lesson_list"><span class="lesson-title">
                                {{ lesson["id"] }} | 第{{ lesson["id"] }}节：
                                {{ lesson["name"] }}</span> <span class="free" v-if="lesson['free_trail']">免费
                            </span></li>
                        </ul>
                        <div class="pay-box">
                            <span class="discount-type" v-if="value.discount_name">{{ value.discount_name }}</span>
                            <span class="discount-price">￥{{ value.real_price }}元</span>
                            <span class="original-price">原价：{{ value.price}}元</span>
                            <span class="buy-now" @click="buy(value.id)">立即购买</span>

                        </div>
                    </div>
                </div>
            </div>
        </div>
        <el-pagination
            background
            layout="prev, pager, next, sizes"
            :page-size="filters.page_size"
            :page-sizes="[2, 3, 5, 10]"
            @current-change="change_page"
            @size-change="size_change"
            :total="count">
        </el-pagination>
        <Fotter></Fotter>
    </div>
</template>

<script>
    import Header from "./Header";
    import Fotter from "./Fotter";

    export default {
        name: "Course",
        components: {
            "Header": Header,
            "Fotter": Fotter,
        },
        data() {
            return {
                category_list: [],
                course_list: [],
                category: 0,
                count: 0,
                token: "",
                filters: {
                    page: 1,
                    page_size: 2,
                    ordering: "id",
                    course_category: "",
                    orders: "id",
                    flag: 0,
                },
            }
        },
        created() {
            this.load_category_list();
            this.load_course_list();
        },
        methods: {
            load_category_list() {
                this.$axios.get(this.$settings.HOST + "course/category/").then(respones => {
                    this.category_list = respones.data;
                }).catch(error => {
                })
            },
            load_course_list() {
                console.log(this.filters);
                this.$axios.get(this.$settings.HOST + "course/list/", {
                    params: this.filters
                }).then(res => {
                    this.course_list = res.data["results"];
                    this.count = res.data["count"];
                }).catch(error => {
                })
            },
            order(str_order) {
                if (this.filters.flag === 0 && str_order === this.filters.orders) {
                    this.filters["flag"] = 1
                    this.filters["ordering"] = "-" + str_order;
                } else if (this.filters.flag === 1 && str_order === this.filters.orders) {
                    this.filters["flag"] = 0
                    this.filters["ordering"] = str_order;
                } else {
                    this.filters["ordering"] = str_order;
                }
                console.log(this.filters["ordering"]);
                this.filters.orders = str_order;
                this.load_course_list();
            },
            cate(id) {
                this.filters["course_category"] = (id == 0) ? "" : id;
                this.filters.page = 1;
                this.category = id;
                this.load_course_list();
            },
            change_page(page) {
                this.filters.page = page;
                this.load_course_list();
            },
            size_change(size) {
                this.filters.page_size = size;
                this.filters.page = 1;
                this.load_course_list();
            },
            is_login() {
                this.token = localStorage.token || sessionStorage.token;
                if (this.token) {
                    return false;
                } else {
                    this.$message("请先登陆后订购");
                }
            },
            buy(id) {
                this.is_login();
                console.log(this.token);
                let token = localStorage.token || sessionStorage.token;
                this.$axios({
                    url: this.$settings.HOST + "cart/list/",
                    method: "post",
                    data: {
                        course_id: id,
                    },
                    config: {
                        headers: {
                            "Authorization": "jwt " + token
                        }
                    }
                }).then(res => {
                    this.$router.push('/cart')
                }).catch(error => {
                    console.log(error.response);
                })
            },
        }
    }
</script>

<style scoped>
    .course {
        background: #f6f6f6;
    }

    .course .main {
        width: 1100px;
        margin: 35px auto 0;
    }

    .course .condition {
        margin-bottom: 35px;
        padding: 25px 30px 25px 20px;
        background: #fff;
        border-radius: 4px;
        box-shadow: 0 2px 4px 0 #f0f0f0;
    }

    .course .cate-list {
        border-bottom: 1px solid #333;
        border-bottom-color: rgba(51, 51, 51, .05);
        padding-bottom: 18px;
        margin-bottom: 17px;
    }

    .course .cate-list::after {
        content: "";
        display: block;
        clear: both;
    }

    .course .cate-list li {
        float: left;
        font-size: 16px;
        padding: 6px 15px;
        line-height: 16px;
        margin-left: 14px;
        position: relative;
        transition: all .3s ease;
        cursor: pointer;
        color: #4a4a4a;
        border: 1px solid transparent; /* transparent 透明 */
    }

    .course .cate-list .title {
        color: #888;
        margin-left: 0;
        letter-spacing: .36px;
        padding: 0;
        line-height: 28px;
    }

    .course .cate-list .this {
        color: #ffc210;
        border: 1px solid #ffc210 !important;
        border-radius: 30px;
    }

    .course .ordering::after {
        content: "";
        display: block;
        clear: both;
    }

    .course .ordering ul {
        float: left;
    }

    .course .ordering ul::after {
        content: "";
        display: block;
        clear: both;
    }

    .course .ordering .condition-result {
        float: right;
        font-size: 14px;
        color: #9b9b9b;
        line-height: 28px;
    }

    .course .ordering ul li {
        float: left;
        padding: 6px 15px;
        line-height: 16px;
        margin-left: 14px;
        position: relative;
        transition: all .3s ease;
        cursor: pointer;
        color: #4a4a4a;
    }

    .course .ordering .title {
        font-size: 16px;
        color: #888;
        letter-spacing: .36px;
        margin-left: 0;
        padding: 0;
        line-height: 28px;
    }

    .course .ordering .this {
        color: #ffc210;
    }

    .course .ordering .price {
        position: relative;
    }

    .course .ordering .price::before,
    .course .ordering .price::after {
        cursor: pointer;
        content: "";
        display: block;
        width: 0px;
        height: 0px;
        border: 5px solid transparent;
        position: absolute;
        right: 0;
    }

    .course .ordering .price::before {
        border-bottom: 5px solid #aaa;
        margin-bottom: 2px;
        top: 2px;
    }

    .course .ordering .price::after {
        border-top: 5px solid #aaa;
        bottom: 2px;
    }

    .course .course-item:hover {
        box-shadow: 4px 6px 16px rgba(0, 0, 0, .5);
    }

    .course .course-item {
        width: 1050px;
        background: #fff;
        padding: 20px 30px 20px 20px;
        margin-bottom: 35px;
        border-radius: 2px;
        cursor: pointer;
        box-shadow: 2px 3px 16px rgba(0, 0, 0, .1);
        /* css3.0 过渡动画 hover 事件操作 */
        transition: all .2s ease;
    }

    .course .course-item::after {
        content: "";
        display: block;
        clear: both;
    }

    /* 顶级元素 父级元素  当前元素{} */
    .course .course-item .course-image {
        float: left;
        width: 423px;
        height: 210px;
        margin-right: 30px;
    }

    .course .course-item .course-image img {
        width: 100%;
    }

    .course .course-item .course-info {
        float: left;
        width: 596px;
    }

    .course-item .course-info h3 {
        font-size: 26px;
        color: #333;
        font-weight: normal;
        margin-bottom: 8px;
    }

    .course-item .course-info h3 span {
        font-size: 14px;
        color: #9b9b9b;
        float: right;
        margin-top: 14px;
    }

    .course-item .course-info h3 span img {
        width: 11px;
        height: auto;
        margin-right: 7px;
    }

    .course-item .course-info .teather-info {
        font-size: 14px;
        color: #9b9b9b;
        margin-bottom: 14px;
        padding-bottom: 14px;
        border-bottom: 1px solid #333;
        border-bottom-color: rgba(51, 51, 51, .05);
    }

    .course-item .course-info .teather-info span {
        float: right;
    }

    .course-item .lesson-list::after {
        content: "";
        display: block;
        clear: both;
    }

    .course-item .lesson-list li {
        float: left;
        width: 44%;
        font-size: 14px;
        color: #666;
        padding-left: 22px;
        /* background: url("路径") 是否平铺 x轴位置 y轴位置 */
        background: url("/static/image/play-icon-gray.svg") no-repeat left 4px;
        margin-bottom: 15px;
    }

    .course-item .lesson-list li .lesson-title {
        /* 以下3句，文本内容过多，会自动隐藏，并显示省略符号 */
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        display: inline-block;
        max-width: 200px;
    }

    .course-item .lesson-list li:hover {
        background-image: url("/static/image/play-icon-yellow.svg");
        color: #ffc210;
    }

    .course-item .lesson-list li .free {
        width: 34px;
        height: 20px;
        color: #fd7b4d;
        vertical-align: super;
        margin-left: 10px;
        border: 1px solid #fd7b4d;
        border-radius: 2px;
        text-align: center;
        font-size: 13px;
        white-space: nowrap;
    }

    .course-item .lesson-list li:hover .free {
        color: #ffc210;
        border-color: #ffc210;
    }

    .course-item .pay-box::after {
        content: "";
        display: block;
        clear: both;
    }

    .course-item .pay-box .discount-type {
        padding: 6px 10px;
        font-size: 16px;
        color: #fff;
        text-align: center;
        margin-right: 8px;
        background: #fa6240;
        border: 1px solid #fa6240;
        border-radius: 10px 0 10px 0;
        float: left;
    }

    .course-item .pay-box .discount-price {
        font-size: 24px;
        color: #fa6240;
        float: left;
    }

    .course-item .pay-box .original-price {
        text-decoration: line-through;
        font-size: 14px;
        color: #9b9b9b;
        margin-left: 10px;
        float: left;
        margin-top: 10px;
    }

    .course-item .pay-box .buy-now {
        width: 120px;
        height: 38px;
        background: transparent;
        color: #fa6240;
        font-size: 16px;
        border: 1px solid #fd7b4d;
        border-radius: 3px;
        transition: all .2s ease-in-out;
        float: right;
        text-align: center;
        line-height: 38px;
    }

    .course-item .pay-box .buy-now:hover {
        color: #fff;
        background: #ffc210;
        border: 1px solid #ffc210;
    }

    .el-pagination {
        text-align: center;
        padding-top: 20px;
        padding-bottom: 50px;
    }
</style>
