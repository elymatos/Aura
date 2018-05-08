import Vue from 'vue'
import Vuex, {Store} from 'vuex'
import {getStoreBuilder} from "vuex-typex";
import {AuthenticationState} from "@/store/auth";
import '@/store/auth'

export interface RootState {
    auth: AuthenticationState
}

Vue.use(Vuex);
const store: Store<RootState> = getStoreBuilder<RootState>().vuexStore();
export default store;