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

    const workspaceResponse = await fetch(`http://backend:8000/api/workspaces/${params.id}/`, {
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
    });

    if (!workspaceResponse.ok) {
        throw error(workspaceResponse.status, 'Failed to load workspace details');
    }

    const workspace = await workspaceResponse.json();

    const membersResponse = await fetch(`http://backend:8000/api/workspaces/${params.id}/members/`, {
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
    });

    if (!membersResponse.ok) {
        throw error(membersResponse.status, 'Failed to load workspace members');
    }

    const members = await membersResponse.json();

    return {workspace, members};
}
