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

    const boardResponse = await fetch(`http://backend:8000/api/boards/board/${params.id}/`, {
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
    });

    if (!boardResponse.ok) {
        throw error(boardResponse.status, 'Failed to load board details');
    }

    const board = await boardResponse.json();

    const listResponse = await fetch(`http://backend:8000/api/boards/list/?board_id=${params.id}`, {
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
    });

    if (!listResponse.ok) {
        throw error(listResponse.status, 'Failed to load lists of board');
    }

    const lists = await listResponse.json();

    return {board, lists};
}
