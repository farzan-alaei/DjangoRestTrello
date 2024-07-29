import {error} from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({request}) {
    const cookies = request.headers.get('cookie')?.split(';').reduce((cookies, cookie) => {
        const [name, value] = cookie.split('=').map(c => c.trim());
        cookies[name] = value;
        return cookies;
    }, {});
    const accessToken = cookies?.access;

    if (!accessToken) {
        throw error(401, 'Access token not found');
    }

    try {
        const boardsResponse = await fetch('http://backend:8000/api/boards/board/', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const workspacesResponse = await fetch('http://backend:8000/api/workspaces/', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (boardsResponse.ok && workspacesResponse.ok) {
            const boards = await boardsResponse.json();
            const workspaces = await workspacesResponse.json();
            return {
                boards: boards || [],
                workspaces: workspaces || []
            };
        } else {
            throw new Error('Failed to load boards or workspaces');
        }
    } catch (error) {
        console.error('Error loading boards or workspaces:', error);
        return {
            boards: [],
            workspaces: [],
            errorMessage: 'Failed to load boards and workspaces. Please try again.'
        };
    }
}
