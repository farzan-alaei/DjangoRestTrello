import {extractCookies} from "$lib/cookies.js";

import {error} from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({request}) {
    const cookies = extractCookies(request);
    const accessToken = cookies?.access;

    if (!accessToken) {
        throw error(401, 'Access token not found');
    }

    try {
        const response = await fetch('http://backend:8000/api/workspaces/', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (response.ok) {
            const workspaces = await response.json();
            return {workspaces: workspaces || []};
        } else {
            throw new Error('Failed to load workspaces');
        }
    } catch (error) {
        console.error('Error loading workspaces:', error);
        return {workspaces: [], errorMessage: 'Failed to load workspaces. Please try again.'};
    }
}
