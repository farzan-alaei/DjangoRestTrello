<!-- src/pages/Login.svelte -->
<script>
    import { email, password, login } from '../stores/auth';

    async function handleLogin() {
        await login();
    }
</script>

<main>
    <h1>Login</h1>
    <form on:submit|preventDefault={handleLogin}>
        <label>Email:</label>
        <input type="email" bind:value={email} required />
        <label>Password:</label>
        <input type="password" bind:value={password} required />
        <button type="submit">Login</button>
    </form>
</main>
