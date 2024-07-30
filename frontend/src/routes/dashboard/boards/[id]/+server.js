import {json} from '@sveltejs/kit';


/** @type {import('@sveltejs/kit').RequestHandler} */
export async function DELETE({fetch, params, url, request}) {
    const cookies = request.headers.get('cookie')?.split(';').reduce((cookies, cookie) => {
        const [name, value] = cookie.split('=').map(c => c.trim());
        cookies[name] = value;
        return cookies;
    }, {});
    const accessToken = cookies?.access;

    if (!accessToken) {
        return new Response('Access token not found', {status: 401});
    }

    const boardId = url.searchParams.get('boardId');
    const apiUrl = boardId
        ? `http://backend:8000/api/boards/board/${boardId}/`
        : `http://backend:8000/api/boards/board/${params.id}/`;

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