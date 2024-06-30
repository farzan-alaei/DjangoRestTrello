import { json } from '@sveltejs/kit';

/** @type {import('@sveltejs/kit').RequestHandler} */
export async function PUT({ request }) {
    const userData = await request.json();
    const cookieHeader = request.headers.get('cookie');
    const cookies = cookieHeader
        ? cookieHeader.split('; ').reduce((acc, cookie) => {
            const [key, value] = cookie.split('=');
            acc[key] = value;
            return acc;
        }, {})
        : {};

    const accessToken = cookies.access;

    if (!accessToken) {
        return new Response('Access token not found', { status: 401 });
    }
    const [response] = await Promise.all([fetch('http://backend:8000/api/auth/profile/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(userData)
    })]);

    if (!response.ok) {
        const errorData = await response.json();
        return new Response(JSON.stringify(errorData), { status: response.status });
    }

    const updatedUser = await response.json();
    return json(updatedUser, { status: 200 });
}
