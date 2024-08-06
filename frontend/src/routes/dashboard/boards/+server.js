import {extractCookies} from "$lib/cookies.js";

/** @type {import('@sveltejs/kit').RequestHandler} */
export async function POST({ request }) {
    const cookies = extractCookies(request);
    const accessToken = cookies?.access;

    if (!accessToken) {
        return new Response('Access token not found', { status: 401 });
    }

    try {
        const body = await request.json();

        const response = await fetch('http://backend:8000/api/boards/board/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(body)
        });

        if (response.ok) {
            const newBoard = await response.json();
            return new Response(JSON.stringify(newBoard), { status: 201 });
        } else {
            const errorText = await response.text(); // Get the response as text
            try {
                const errorData = JSON.parse(errorText); // Try to parse it as JSON
                return new Response(JSON.stringify(errorData), { status: response.status });
            } catch (e) {
                // If parsing fails, return the text response
                return new Response(errorText, { status: response.status });
            }
        }
    } catch (error) {
        console.error('Error creating board:', error);
        return new Response('Error creating board', { status: 500 });
    }
}
