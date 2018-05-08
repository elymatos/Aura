import axios, {AxiosError, AxiosResponse} from 'axios'
import auth from '@/store/auth'
import {SuccessfulRequest, UnsuccessfulRequest} from "@/api";

interface SuccessfulLoginRequest extends SuccessfulRequest {
    data: {
        access_token: string,
        refresh_token: string
    }
}

interface SuccessfulRegisterRequest extends SuccessfulRequest {
    data: {
        access_token: string
    }
}

export async function login(username: string, password: string){
    return await axios.post('/api/login',{
        username: username,
        password: password
    }).then((response: AxiosResponse<SuccessfulLoginRequest | UnsuccessfulRequest>) => {
        return response.data;
    }).catch((error: AxiosError) => {
        return {
            status: error.code || "",
            message: error.message
        };
    })
}

export async function register(username: string, password: string){
    return await axios.post('/api/create_user', {
        username: username,
        password: password
    }).then((response: AxiosResponse<SuccessfulRegisterRequest | UnsuccessfulRequest>) => {
        return response.data;
    }).catch((error: AxiosError) => {
        return {
            status: error.code || "",
            message: error.message
        };
    })
}

export function heey(){
    return axios.post('/api/heey', {}, auth.accessTokenHeader)
}