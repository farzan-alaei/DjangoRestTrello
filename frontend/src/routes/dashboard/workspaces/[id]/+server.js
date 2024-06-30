import {error, json} from '@sveltejs/kit';

/** @type {import('@sveltejs/kit').RequestHandler} */
export async function PUT({fetch, params, request}) {
    const {id} = params;
    const workspaceData = await request.json();
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
        return new Response('Access token not found', {status: 401});
    }

    const response = await fetch(`http://backend:8000/api/workspaces/${id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(workspaceData)
    });

    if (!response.ok) {
        const errorData = await response.json();
        return new Response(JSON.stringify(errorData), {status: response.status});
    }

    const updatedWorkspace = await response.json();
    return json(updatedWorkspace, {status: 200});
}

/** @type {import('@sveltejs/kit').RequestHandler} */
export async function DELETE({fetch, params, request}) {
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
        return new Response('Access token not found', {status: 401});
    }

    const response = await fetch(`http://backend:8000/api/workspaces/${id}/`, {
        method: 'DELETE',
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });

    if (!response.ok) {
        const errorData = await response.json();
        return new Response(JSON.stringify(errorData), {status: response.status});
    }

    return new Response(null, {status: 204});
}
