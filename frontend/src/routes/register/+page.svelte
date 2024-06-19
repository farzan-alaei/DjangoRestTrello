<script>
    import {goto} from '$app/navigation';

    let email = '';
    let password = '';
    let error = '';

    async function register(event) {
        event.preventDefault();
        error = '';

        try {
            const response = await fetch('http://localhost:8000/api/register/', {  // فرض می‌کنیم endpoint ثبت‌نام شما این است
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({email, password})
            });

            if (!response.ok) {
                throw new Error('Registration failed');
            }

            const data = await response.json();
            goto('/login');  // بعد از ثبت‌نام موفق، کاربر را به صفحه لاگین هدایت می‌کنیم
        } catch (err) {
            error = err.message;
        }
    }
</script>

<h1>Register Page</h1>
<form on:submit={register}>
    {#if error}
        <p style="color: red;">{error}</p>
    {/if}
    <label>Email:</label>
    <input type="email" bind:value={email} required/>
    <label>Password:</label>
    <input type="password" bind:value={password} required/>
    <button type="submit">Register</button>
</form>
