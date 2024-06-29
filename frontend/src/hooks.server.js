// src/hooks.server.js
import {get} from 'svelte/store';
import {isLoggedIn} from './stores/authStore';

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({event, resolve}) {
    const cookies = event.request.headers.get('cookie') || '';
    const cookiesObject = Object.fromEntries(
        cookies.split('; ').map(cookie => cookie.split('=').map(decodeURIComponent))
    );

    const accessToken = cookiesObject['access'];
    const refreshToken = cookiesObject['refresh'];

    if (accessToken && refreshToken) {
        isLoggedIn.set(true);
    } else {
        isLoggedIn.set(false);
    }

    const {route} = event;
    const loggedIn = get(isLoggedIn);

    if (loggedIn && (route.id === '/login' || route.id === '/register')) {
        return new Response(null, {
            status: 302,
            headers: {Location: '/dashboard'}
        });
    }

    return await resolve(event);
}
