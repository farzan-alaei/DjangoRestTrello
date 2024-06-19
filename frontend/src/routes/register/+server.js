import {json, error} from '@sveltejs/kit';

export async function POST({request}) {
    const {email_or_mobile, password} = await request.json();


    const response = await fetch('http://backend:8000/auth/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email_or_mobile, password})
    });

    if (!response.ok) {
        const errData = await response.json();
        return error(response.status, errData.message || 'Registration failed');
    }

    const data = await response.json();
    return json(data);
}
