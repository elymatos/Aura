import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import store from '@/store'
import Login from '@/Login.vue'
import authStore from '@/store/auth'

Vue.use(ElementUI)

new Vue({
    el: '#app',
    store,
    render: h => h(Login, {
        props: { store: authStore }
    })
});

/*
async function a(){
    await auth.attemptLogin({
        username: "test",
        password: "test"
    });
    auth.dispatchHey()
}
a();
*/



//console.log(store.state.auth.username);
//console.log(auth)




