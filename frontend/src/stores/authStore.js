import {writable} from "svelte/store";

export const isLoggedIn = writable(false)


export function getAccessToken() {
    if (typeof document !== 'undefined') {
        // client side
        const cookies = document.cookie.split(';').reduce((cookies, cookie) => {
            const [name, value] = cookie.split('=').map(c => c.trim());
            cookies[name] = value;
            return cookies;
        }, {});
        return cookies['access'] || null;
    } else {
        // server side
        return null; // or other method in server side to get access token
    }
}