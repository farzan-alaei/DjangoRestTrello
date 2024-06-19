<script>
    import {goto} from '$app/navigation';

    let email_or_mobile = '';
    let password = '';
    let error = '';

    async function login(event) {
        event.preventDefault();
        error = '';

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({email_or_mobile, password})
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            localStorage.setItem('access', data.access);
            localStorage.setItem('refresh', data.refresh);

            goto('/profile');
        } catch (err) {
            error = err.message;
        }
    }
</script>

<h1>Login Page</h1>
<form on:submit={login}>
    {#if error}
        <p style="color: red;">{error}</p>
    {/if}
    <label>Email or Mobile:</label>
    <input type="text" bind:value={email_or_mobile} required/>
    <label>Password:</label>
    <input type="password" bind:value={password} required/>
    <button type="submit">Login</button>
</form>
