import {error} from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({request, params}) {
    const cookies = request.headers.get('cookie')?.split(';').reduce((cookies, cookie) => {
        const [name, value] = cookie.split('=').map(c => c.trim());
        cookies[name] = value;
        return cookies;
    }, {});
    const accessToken = cookies?.access;


    if (!accessToken) {
        throw error(401, 'Access token not found');
    }

    const response = await fetch(`http://backend:8000/api/workspaces/${params.id}/`, {
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
    });


    if (response.ok) {
        const workspace = await response.json();
        return {workspace};
    } else {
        throw error(response.status, 'Failed to load workspace details');
    }
}
