<script>
    import {goto} from '$app/navigation';
</script>

<header>
    <nav>
        <a href="/" on:click|preventDefault={() => goto('/')}>Home</a>
        <a href="/login" on:click|preventDefault={() => goto('/login')}>Login</a>
        <a href="/register" on:click|preventDefault={() => goto('/register')}>Register</a>
        <a href="/profile" on:click|preventDefault={() => goto('/profile')}>Profile</a>
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

    a {
        color: white;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }
</style>
