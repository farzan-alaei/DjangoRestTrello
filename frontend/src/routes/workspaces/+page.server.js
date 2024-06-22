import {json, error} from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({fetch}) {
    const response = await fetch('http://backend:8000/api/workspaces/');
    if (!response.ok) {
        throw error(response.status, 'Failed to load workspaces');
    }
    const workspaces = await response.json();
    return {
        workspaces
    };
}