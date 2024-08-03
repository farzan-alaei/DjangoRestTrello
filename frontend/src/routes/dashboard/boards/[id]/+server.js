import {json} from '@sveltejs/kit';

/** @type {import('@sveltejs/kit').RequestHandler} */
export async function PUT({fetch, params, request, url}) {
    const requestData = await request.json();
    const cookies = request.headers.get('cookie')?.split(';').reduce((cookies, cookie) => {
        const [name, value] = cookie.split('=').map(c => c.trim());
        cookies[name] = value;
        return cookies;
    }, {});
    const accessToken = cookies?.access;

    if (!accessToken) {
        return new Response('Access token not found', {status: 401});
    }

    const listId = url.searchParams.get('listId');
    const taskId = url.searchParams.get('taskId');
    const taskListId = url.searchParams.get('taskListId');
    let apiUrl;

    if (taskId && taskListId) {
        apiUrl = `http://backend:8000/api/boards/task/${taskId}/?list_id=${taskListId}`;
    } else if (listId) {
        apiUrl = `http://backend:8000/api/boards/list/${listId}/?board_id=${params.id}`;
    } else {
        apiUrl = `http://backend:8000/api/boards/board/${params.id}/`;
    }

    const response = await fetch(apiUrl, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(requestData)
    });

    if (!response.ok) {
        const errorData = await response.json();
        return new Response(JSON.stringify(errorData), {status: response.status});
    }

    const updatedData = await response.json();
    return json(updatedData, {status: 200});
}


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

    const listId = url.searchParams.get('listId');
    const taskId = url.searchParams.get('taskId');
    let apiUrl;

    if (taskId) {
        apiUrl = `http://backend:8000/api/boards/task/${taskId}/`;
    } else if (listId) {
        apiUrl = `http://backend:8000/api/boards/list/${listId}/?board_id=${params.id}`;
    } else {
        apiUrl = `http://backend:8000/api/boards/board/${params.id}/`;
    }

    const response = await fetch(apiUrl, {
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


/** @type {import('@sveltejs/kit').RequestHandler} */
export async function POST({params, request, url}) {
    const requestData = await request.json();

    const cookies = request.headers.get('cookie')?.split(';').reduce((cookies, cookie) => {
        const [name, value] = cookie.split('=').map(c => c.trim());
        cookies[name] = value;
        return cookies;
    }, {});
    const accessToken = cookies?.access;

    if (!accessToken) {
        return json({error: 'Access token not found'}, {status: 401});
    }

    const tasklistId = url.searchParams.get('list_id');
    const apiUrl = tasklistId
        ? `http://backend:8000/api/boards/task/?list_id=${tasklistId}`
        : `http://backend:8000/api/boards/list/`;


    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            return new Response(JSON.stringify(errorData), {status: response.status});
        }

        const data = await response.json();
        return json(data, {status: 201});
    } catch (error) {
        console.error('Error:', error);
        return json({error: 'Internal Server Error'}, {status: 500});
    }
}


/** @type {import('@sveltejs/kit').RequestHandler} */
export async function PATCH({request, url}) {
    const cookies = request.headers.get('cookie')?.split(';').reduce((cookies, cookie) => {
        const [name, value] = cookie.split('=').map(c => c.trim());
        cookies[name] = value;
        return cookies;
    }, {});
    const accessToken = cookies?.access;

    if (!accessToken) {
        return json({error: 'Access token not found'}, {status: 401});
    }

    const listId = url.searchParams.get('listId');
    const taskId = url.searchParams.get('taskId');

    const response = await fetch(`http://backend:8000/api/boards/task/${taskId}/?list_id=${listId}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        },
    });

    if (!response.ok) {
        const errorData = await response.json();
        return new Response(JSON.stringify(errorData), {status: response.status});
    }

    const data = await response.json();
    return json(data, {status: 200});
}
