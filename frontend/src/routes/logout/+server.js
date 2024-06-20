// src/routes/logout/+server.js
import {json} from '@sveltejs/kit';

export async function POST({request}) {
    const {refresh} = await request.json();

    const response = await fetch('http://backend:8000/auth/api/logout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({refresh: refresh})
    });

    if (response.ok) {
        return json({message: 'Logged out successfully'}, {status: 200});
    } else {
        const errorText = await response.text();
        return json({error: 'Failed to logout', details: errorText}, {status: 400});
    }
}
