import {BareActionContext} from "vuex-typex";
import {RootState} from "@/store";
import {isSuccessfulRequest, REQUEST_STATUS_ERROR, REQUEST_STATUS_FAILED} from "@/api"
import {heey, login, register} from "@/store/auth/api";
import {AuthenticationState, commitLoginFailure, commitLoginSuccess, commitRegisterFailure} from "@/store/auth/index";

/** Actions **/
export async function ATTEMPT_LOGIN(
    context: BareActionContext<AuthenticationState, RootState>,
    payload: {
        username: string,
        password: string
    }) {
    const result = await login(payload.username, payload.password);
    if (isSuccessfulRequest(result)) {
        const data = {
            'accessToken': result.data.access_token,
            'refreshToken': result.data.refresh_token,
            'username': payload.username
        }
        commitLoginSuccess(data)
        console.log("Login success");
    }
    else if (result.status == REQUEST_STATUS_FAILED || result.status == REQUEST_STATUS_ERROR) {
        commitLoginFailure(result)
    } else { // Exception thrown by Axios
        commitLoginFailure(result)
    }
}

export async function ATTEMPT_REGISTER(
    context: BareActionContext<AuthenticationState, RootState>,
    payload: {
        username: string,
        password: string
    }){
    const result = (await register(payload.username, payload.password))
    if(isSuccessfulRequest(result)){
        const data = {
            'accessToken': result.data.access_token,
            'refreshToken': "",
            'username': payload.username
        }
        commitLoginSuccess(data)
        console.log("Register success");
    }
    else if (result.status == REQUEST_STATUS_FAILED || result.status == REQUEST_STATUS_ERROR) {
        commitRegisterFailure(result)
    } else { // Exception thrown by Axios
        commitRegisterFailure(result)
    }
}


export async function ATTEMPT_HEY(context: BareActionContext<AuthenticationState, RootState>) {
    let result = await heey();
    console.log("Heey success?")
    console.log(result.data)
}
