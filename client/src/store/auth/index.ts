import {RootState} from "@/store";
import {getStoreBuilder} from "vuex-typex";
import {ATTEMPT_LOGIN, ATTEMPT_HEY, ATTEMPT_REGISTER} from "@/store/auth/actions";
import {
    mutateAccessToken,
    LoginSuccessMutation,
    mutateRefreshToken,
    LoginFailureMutation,
    RegisterFailureMutation
} from "@/store/auth/mutations";

export interface AuthenticationStore {
    state: () => AuthenticationState,
    attemptLogin: (payload: {username: string,password: string}) => Promise<null>
    attemptRegister: (payload: {username: string,password: string}) => Promise<null>
    accessTokenHeader: string
    refreshTokenHeader: string
    username: string
    lastFailureMessage: string
}

export interface AuthenticationState {
    username: string,
    accessToken: string
    refreshToken: string
    loginAttempts: number
    lastFailureMessage: string
}

const initial: AuthenticationState = {
    username: "",
    accessToken: "",
    refreshToken: "",
    lastFailureMessage: "",
    loginAttempts: 0
};

const builder = getStoreBuilder<RootState>().module("auth", initial);

/** Mutations **/
export const commitLoginSuccess = builder.commit(LoginSuccessMutation)
export const commitLoginFailure = builder.commit(LoginFailureMutation)
export const commitRegisterFailure = builder.commit(RegisterFailureMutation)
export const commitRefreshToken = builder.commit(mutateRefreshToken);
export const commitAccessToken = builder.commit(mutateAccessToken);

/** Getters **/
const getAccessTokenHeader = builder.read<object>(function getAccessTokenHeader(state) {
    return {headers: {'Authorization': `Bearer ${state.accessToken}`}}
});
const getRefreshTokenHeader = builder.read<object>(function getRefreshTokenHeader(state) {
    return {headers: {'Authorization': `Bearer ${state.refreshToken}`}}
});
const getUsername = builder.read<string>(function getUsername(state) {
    return state.username
});
const getLastFailureMessage = builder.read<string>(function getLastFailureMessage(state){
    return state.lastFailureMessage
})

/** Exposed operations **/
export default {

    get state() {
        return builder.state()
    },

    attemptLogin: builder.dispatch(ATTEMPT_LOGIN),
    attemptRegister: builder.dispatch(ATTEMPT_REGISTER),
    dispatchHey: builder.dispatch(ATTEMPT_HEY),

    //Getters
    get accessTokenHeader() {
        return getAccessTokenHeader()
    },
    get refreshTokenHeader() {
        return getRefreshTokenHeader()
    },
    get username() {
        return getUsername()
    },
    get lastFailureMessage(){
        return getLastFailureMessage()
    }

};