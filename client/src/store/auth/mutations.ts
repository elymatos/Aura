import {AuthenticationState} from "@/store/auth/index";
import {REQUEST_STATUS_FAILED} from "@/api";

/** Mutations **/
export function mutateAccessToken(state: AuthenticationState, payload: { access_token: string }) {
    state.accessToken = payload.access_token
}

export function RegisterFailureMutation(state: AuthenticationState, payload: {status: string, message: string}){
    state.lastFailureMessage = payload.message
}

export function LoginSuccessMutation(state: AuthenticationState, payload: { username: string, accessToken: string, refreshToken: string }) {
    state.username = payload.username;
    state.accessToken = payload.accessToken;
    state.refreshToken = payload.refreshToken;
    state.lastFailureMessage = ""
}

export function mutateRefreshToken(state: AuthenticationState, payload: { refresh_token: string }) {
    state.refreshToken = payload.refresh_token
}

export function LoginFailureMutation(state: AuthenticationState, payload: {status: string, message: string}){
    if(status == REQUEST_STATUS_FAILED){
        state.loginAttempts++
    }
    state.lastFailureMessage = payload.message
}