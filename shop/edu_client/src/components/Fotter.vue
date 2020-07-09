<template>
    <div class="footer">
        <ul>
            <li v-for="(value,index) in footerlist" :key="index"><span v-if="value.position==2">{{ value.title }}</span></li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: "Fotter",
        data() {
            return {
                footerlist: []
            }
        },
        created() {
            this.fotter()
        },
        methods: {
            fotter() {
                this.$axios({
                    url: this.$settings.HOST + "home/nav/",
                    method: "get"
                }).then(res => {
                    this.footerlist = res.data["results"]
                    console.log(res.data)
                }).catch(error => {
                    console.log(error)
                })
            }
        }
    }
</script>

<style scoped>
    .footer {
        width: 100%;
        height: 128px;
        background: #25292e;
        color: #fff;
    }

    .footer ul {
        margin: 0 auto 16px;
        padding-top: 38px;
        width: 810px;
    }

    .footer ul li {
        float: left;
        width: 110px;
        margin: 0 10px;
        text-align: center;
        font-size: 14px;
    }


    .footer li span {
        padding-bottom: 16px;
        padding-left: 5px;
        padding-right: 5px;
    }

    .footer li span a {
        display: inline-block;
    }
    .footer ul::after {
        content: "";
        display: block;
        clear: both;
    }

    .footer p {
        text-align: center;
        font-size: 12px;
    }
</style>
