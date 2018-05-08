export interface SuccessfulRequest {
    status: string,
    data: {}
}

export interface UnsuccessfulRequest {
    status: string,
    message: string
}

export function isSuccessfulRequest(response: any): response is SuccessfulRequest{
    return (<SuccessfulRequest>response).status == REQUEST_STATUS_SUCCESS
}

export const REQUEST_STATUS_SUCCESS = "success"
export const REQUEST_STATUS_FAILED = "fail"
export const REQUEST_STATUS_ERROR = "error"