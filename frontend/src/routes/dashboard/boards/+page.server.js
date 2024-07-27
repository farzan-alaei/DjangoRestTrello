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
        const response = await fetch('http://backend:8000/api/boards/board/', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (response.ok) {
            const boards = await response.json();
            return {boards: boards || []};
        } else {
            throw new Error('Failed to load boards');
        }
    } catch (error) {
        console.error('Error loading boards:', error);
        return {boards: [], errorMessage: 'Failed to load boards. Please try again.'};
    }
}