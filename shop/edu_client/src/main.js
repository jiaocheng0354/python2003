// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'


Vue.config.productionTip = false

import axios from "axios"

Vue.prototype.$axios = axios
import store from './store/index'
import ElementUI from 'element-ui'
import "element-ui/lib/theme-chalk/index.css"

Vue.use(ElementUI)

import settings from "./settings";

Vue.prototype.$settings = settings;
import "../static/css/global.css"
import "../static/js/gt.js"

// 视频组件
require('video.js/dist/video-js.css');
require('vue-video-player/src/custom-theme.css');
import VideoPlayer from 'vue-video-player'

Vue.use(VideoPlayer);

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    components: {App},
    template: '<App/>'
})
