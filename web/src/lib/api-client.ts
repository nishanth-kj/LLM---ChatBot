class ApiClient {
    private baseURL: string;

    constructor(baseURL: string = "http://localhost:8000/api") {
        this.baseURL = baseURL;
    }

    /**
     * Sanitizes and formats the combination of baseURL and path.
     */
    private formatURL(url: string): string {
        const base = this.baseURL.endsWith("/") ? this.baseURL.slice(0, -1) : this.baseURL;
        const path = url.startsWith("/") ? url : `/${url}`;
        return `${base}${path}`;
    }

    /**
     * Generic GET HTTP method wrapper using native fetch.
     * Takes url and payload (query params) in the inputs.
     */
    async get<T>(url: string, data: any = {}, options: RequestInit = {}): Promise<T> {
        let finalURL = this.formatURL(url);
        if (data && Object.keys(data).length > 0) {
            const searchParams = new URLSearchParams(data);
            finalURL += `?${searchParams.toString()}`;
        }
        
        const response = await fetch(finalURL, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
            ...options,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json() as Promise<T>;
    }

    /**
     * Generic POST HTTP method wrapper using native fetch.
     * Takes url and payload in the inputs.
     */
    async post<T>(url: string, data: any = {}, options: RequestInit = {}): Promise<T> {
        const response = await fetch(this.formatURL(url), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
            body: JSON.stringify(data),
            ...options,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json() as Promise<T>;
    }

    /**
     * Generic PUT HTTP method wrapper using native fetch.
     * Takes url and payload in the inputs.
     */
    async put<T>(url: string, data: any = {}, options: RequestInit = {}): Promise<T> {
        const response = await fetch(this.formatURL(url), {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
            body: JSON.stringify(data),
            ...options,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json() as Promise<T>;
    }

    /**
     * Generic DELETE HTTP method wrapper using native fetch.
     * Takes url and payload (query params) in the inputs.
     */
    async delete<T>(url: string, data: any = {}, options: RequestInit = {}): Promise<T> {
        let finalURL = this.formatURL(url);
        if (data && Object.keys(data).length > 0) {
            const searchParams = new URLSearchParams(data);
            finalURL += `?${searchParams.toString()}`;
        }

        const response = await fetch(finalURL, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
            ...options,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json() as Promise<T>;
    }
}

// Export a singleton instance pointing to the Python FastAPI server
export const apiClient = new ApiClient();
