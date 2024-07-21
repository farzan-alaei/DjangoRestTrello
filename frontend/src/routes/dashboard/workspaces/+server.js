/** @type {import('./$types').RequestHandler} */
export async function POST({request}) {
    const {title, description} = await request.json();

    // Extract access token from cookies
    const cookies = request.headers.get('cookie')?.split(';').reduce((cookies, cookie) => {
        const [name, value] = cookie.split('=').map(c => c.trim());
        cookies[name] = value;
        return cookies;
    }, {});
    const accessToken = cookies?.access;

    if (!accessToken) {
        return new Response(JSON.stringify({error: 'Access token not found'}), {status: 401});
    }

    try {
        const response = await fetch('http://backend:8000/api/workspaces/', {
            method: 'POST', headers: {
                'Content-Type': 'application/json', 'Authorization': `Bearer ${accessToken}`
            }, body: JSON.stringify({title, description})
        });

        if (response.ok) {
            const newWorkspace = await response.json();
            return new Response(JSON.stringify(newWorkspace), {headers: {'Content-Type': 'application/json'}});
        } else {
            throw new Error('Failed to create workspace');
        }
    } catch (error) {
        console.error('Error creating workspace:', error);
        return new Response(JSON.stringify({error: 'Failed to create workspace. Please try again.'}), {status: 400});
    }
}
