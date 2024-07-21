export async function POST({request}) {
    const {email_or_mobile, password} = await request.json();

    const response = await fetch('http://backend:8000/api/auth/register/', {
        method: 'POST', headers: {
            'Content-Type': 'application/json'
        }, body: JSON.stringify({email_or_mobile, password})
    });

    if (!response.ok) {
        return new Response(JSON.stringify({error: 'Registration failed'}), {status: 401});
    }

    const data = await response.json();
    return new Response(JSON.stringify(data), {
        headers: {'Content-Type': 'application/json'}
    });
}
