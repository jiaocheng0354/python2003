import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Register from "../components/Register";
import UpdateEmp from "../components/UpdateEmp";
import EmpList from "../components/EmpList";
import AddEmp from "../components/AddEmp";
import Test from "../components/Test";

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {path: '/', component: Login},
        {path: '/login', component: Login},
        {path: '/register', component: Register},
        {path: '/updatte/:id', component: UpdateEmp},
        {path: '/emplist', component: EmpList},
        {path: '/addemp', component: AddEmp},
        {path: '/test', component: Test},

    ]
})
