import {extractCookies} from "$lib/cookies.js";

/** @type {import('./$types').PageServerLoad} */
export async function POST({request}) {
    const {email, mobile, first_name, last_name} = await request.json();

    // cookies
    const cookies = extractCookies(request);
    const accessToken = cookies?.access; // get token from cookies

    if (!accessToken) {
        return new Response(JSON.stringify({error: 'Access token not found'}), {status: 401});
    }

    const response = await fetch('http://backend:8000/api/auth/profile/', {
        method: 'PUT', headers: {
            'Content-Type': 'application/json', 'Authorization': `Bearer ${accessToken}`
        }, body: JSON.stringify({email, mobile, first_name, last_name})
    });

    if (response.ok) {
        const updatedUser = await response.json();
        return new Response(JSON.stringify(updatedUser), {
            headers: {'Content-Type': 'application/json'}
        });
    } else {
        const errorData = await response.json();
        return new Response(JSON.stringify(errorData), {status: 400});
    }
}
