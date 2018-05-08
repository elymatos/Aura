<template>
    <div>
        <el-button @click="dialog_visible = true">Click me</el-button>
        <el-dialog :visible.sync="dialog_visible" title="Login or Register">
            <el-input label="Username" v-model="username"></el-input>
            <el-input label="Password" v-model="password" type="password"></el-input>
            <el-button @click="login()">Login</el-button>
            <el-button @click="register()" type="primary">Register</el-button>
            <div v-if="message_visible">
                <div v-if="store.lastFailureMessage">
                    <el-alert :title="`Failure! Message: ${store.lastFailureMessage}`" type="error"></el-alert>
                </div>
                <div v-else>
                    <el-alert :title="`Success! Username: ${store.username}`" type="success"></el-alert>
                </div>
            </div>
        </el-dialog>
    </div>
</template>
<script lang="ts">
    import Vue from 'vue'
    import {Component, Prop} from 'vue-property-decorator'
    import {AuthenticationStore} from "./store/auth";

    @Component
    export default class App extends Vue {
        @Prop()
        store!: AuthenticationStore

        username: string = ""
        password: string = ""
        dialog_visible: boolean = false
        message_visible: boolean = false

        login() {
            /** Using global $store **/ /*
            this.$store.dispatch('auth/ATTEMPT_LOGIN', {
                username: this.username,
                password: this.password
            });*/
            /** Using typesafe "exposed store operations" object **/
            this.store.attemptLogin({
                username: this.username,
                password: this.password
            }).then(() => {
                this.message_visible = true
            })
        }

        register() {
            this.store.attemptRegister({
                username: this.username,
                password: this.password
            }).then(() => {
                this.message_visible = true
            })
        }
    }
</script>