<script>
    import {goto} from '$app/navigation';

    let email_or_mobile = '';
    let password = '';
    let confirmPassword = '';
    let error = '';


    async function register(event) {
        event.preventDefault();
        if (password !== confirmPassword) {
            error = 'Passwords do not match';
            return;
        }
        error = '';
        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({email_or_mobile, password})
            });
            if (!response.ok) {
                throw new Error('Registration failed');
            }
            const data = await response.json();
            localStorage.setItem('access', data.access);
            localStorage.setItem('refresh', data.refresh);

            await goto('/profile');
        } catch (err) {
            error = err.message;
        }
    }


</script>


<h1>Register Page</h1>
<form on:submit|preventDefault={register}>
    <label>
        Email or Mobile:
        <input type="text" bind:value={email_or_mobile} required/>
    </label>
    <label>
        Password:
        <input type="password" bind:value={password} required/>
    </label>
    <label>
        Confirm Password:
        <input type="password" bind:value={confirmPassword} required/>
    </label>
    {#if error}
        <p style="color: red;">{error}</p>
    {/if}
    <button type="submit">Register</button>
</form>
