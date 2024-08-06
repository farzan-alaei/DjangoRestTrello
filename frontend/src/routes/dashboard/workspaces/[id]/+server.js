import {extractCookies} from "$lib/cookies.js";

import {json} from '@sveltejs/kit';

/** @type {import('@sveltejs/kit').RequestHandler} */
export async function PUT({fetch, params, request}) {
    const workspaceData = await request.json();
    const cookies = extractCookies(request);
    const accessToken = cookies?.access;

    if (!accessToken) {
        return new Response('Access token not found', {status: 401});
    }

    const response = await fetch(`http://backend:8000/api/workspaces/${params.id}/`, {
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
export async function DELETE({fetch, params, url, request}) {
    const cookies = extractCookies(request);
    const accessToken = cookies?.access;

    if (!accessToken) {
        return new Response('Access token not found', {status: 401});
    }

    const membershipId = url.searchParams.get('membershipId');
    const apiUrl = membershipId
        ? `http://backend:8000/api/workspaces/members/${membershipId}/`
        : `http://backend:8000/api/workspaces/${params.id}/`;

    const response = await fetch(apiUrl, {
        method: 'DELETE',
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });

    if (!response.ok) {
        const errorData = await response.json();
        return new Response(JSON.stringify(errorData), { status: response.status });
    }

    return new Response(null, { status: 204 });
}