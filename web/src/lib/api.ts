const API_URL = import.meta.env.VITE_API_URL;

export async function apiRequest<T>(
    endpoint: string,
    options: RequestInit = {},
): Promise<T> {
    let response: Response;
    try {
        response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
        });
    } catch {
        throw new Error(
            "Unable to connect to the server. Please try again.",
        );
    }

    const data = await response.json().catch(() => null);

    if (!response.ok) {
        throw new Error(
            data?.detail || "Something went wrong. Please try again.",
        );
    }

    return data;
}

export async function apiRequestWithAuth<T>(
    endpoint: string,
    options: RequestInit = {},
): Promise<T> {

    const token = localStorage.getItem("access_token");

    let response: Response;

    try {
        response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
                ...options.headers,
            },
        });
    } catch {
        throw new Error(
            "Unable to connect to the server. Please try again.",
        );
    }

    const data = await response.json().catch(() => null);

    if (!response.ok) {
        throw new Error(
            data?.detail || "Something went wrong. Please try again.",
        );
    }

    return data;
}