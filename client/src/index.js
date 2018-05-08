import Vue from 'vue';
import store from '@/store';
import Counter from '@/Counter.vue';
console.log(store.getters.count);
new Vue({
    el: '#app',
    store: store,
    render: function (h) { return h(Counter); }
});
