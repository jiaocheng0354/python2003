import Vue from 'vue'

import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        // 购物车数据
        cart_length: 0,
        count_price: 0.
    },

    mutations: {
        add_cart(state, data) {
            state.cart_length = data;
        },
        money_cart(state, data) {
            state.count_price = data;
        }
    }
})
