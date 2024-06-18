// src/stores/auth.js
import {writable} from 'svelte/store';

export const email = writable('');
export const password = writable('');

export async function login() {
    const response = await fetch('http://localhost:8000/api/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: $email,
            password: $password
        })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access', data.access);
        localStorage.setItem('refresh', data.refresh);
        // Handle successful login (e.g., redirect to home)
    } else {
        // Handle error
    }
}
