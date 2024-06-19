export async function api(endpoint, method = 'GET', data = null) {
    const token = localStorage.getItem('access');
    const headers = { 'Content-Type': 'application/json' };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`http://backend:8000/api/${endpoint}`, {
        method,
        headers,
        body: data ? JSON.stringify(data) : null
    });

    if (response.status === 401) {
        // handle token refresh here
    }

    return response.json();
}
