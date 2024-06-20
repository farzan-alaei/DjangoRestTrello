<!-- src/lib/Header.svelte -->
<script>
    import {goto} from '$app/navigation';
    import {isLoggedIn} from '../stores/authStore';
    import {onMount} from 'svelte';


    onMount(() => {
        isLoggedIn.set(document.cookie.includes('access') && document.cookie.includes('refresh'));
    });

    $: loggedIn = $isLoggedIn;

    async function logout() {
        const refreshToken = localStorage.getItem('refresh');

        const response = await fetch('/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                refresh: refreshToken
            })
        });

        if (response.ok) {
            document.cookie = 'access=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
            document.cookie = 'refresh=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
            isLoggedIn.set(false);
            await goto('/');
        } else {
            const errorData = await response.json();
            console.error('Failed to logout:', errorData);
        }
    }
</script>

<header>
    <nav>
        <a href="/" on:click|preventDefault={() => goto('/')}>Home</a>
        {#if loggedIn}
            <a href="/profile" on:click|preventDefault={() => goto('/profile')}>Profile</a>
            <button on:click={logout}>Logout</button>
        {:else}
            <a href="/login" on:click|preventDefault={() => goto('/login')}>Login</a>
            <a href="/register" on:click|preventDefault={() => goto('/register')}>Register</a>
        {/if}
    </nav>
</header>

<style>
    header {
        background-color: #2e353d;
        color: white;
        padding: 1rem;
    }

    nav {
        display: flex;
        gap: 10px;
    }

    a, button {
        color: white;
        text-decoration: none;
        background: none;
        border: none;
        cursor: pointer;
    }

    a:hover, button:hover {
        text-decoration: underline;
    }
</style>
