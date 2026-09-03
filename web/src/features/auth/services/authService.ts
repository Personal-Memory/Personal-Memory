import { apiRequest } from "../../../lib/api";

export interface RegisterRequest {
    username: string;
    email: string;
    password: string;
    first_name: string;
    last_name: string;
}

export interface RegisterResponse {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
}

export async function register(request: RegisterRequest): Promise<RegisterResponse> {
    return apiRequest<RegisterResponse>(
        "/auth/register",
        {
            method: "POST",
            body: JSON.stringify(request),
        }
    );
}