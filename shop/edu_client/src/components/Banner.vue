<template>
    <el-carousel height="720px" :interval="3000" arrow="always" >
        <el-carousel-item v-for="(value,index) in list" :key="index">
            <img :src="value.img" alt="">
        </el-carousel-item>

    </el-carousel>
</template>

<script>
    export default {
        name: "Banner",
        data() {
            return {
                list: []
            }
        },
        created() {
            this.banner()
        },
        methods: {
            banner() {
                this.$axios({
                    url: this.$settings.HOST + "home/banner/",
                    method: "get"
                }).then(res=>{
                    this.list = res.data["results"]
                    console.log(res.data)
                }).catch(error=>{
                    console.log(error)
                })
            }
        }

    }
</script>

<style scoped>
    .el-carousel__item h3 {
        color: #475669;
        font-size: 18px;
        opacity: 0.75;
        line-height: 300px;
        margin: 0;
    }

    .el-carousel__item:nth-child(2n) {
        background-color: #99a9bf;
    }

    .el-carousel__item:nth-child(2n+1) {
        background-color: #d3dce6;
    }
</style>
