import {error} from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({fetch, params, request}) {
    const {id} = params;
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
        throw error(401, 'Access token not found');
    }

    const response = await fetch(`http://backend:8000/api/workspaces/${id}/`, {
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });

    if (!response.ok) {
        throw error(response.status, 'Failed to load workspace details');
    }

    const workspace = await response.json();
    return {
        workspace
    };
}
