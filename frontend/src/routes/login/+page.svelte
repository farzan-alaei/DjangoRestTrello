<script>
    import {goto} from '$app/navigation';
    import {isLoggedIn} from "../../stores/authStore.js";
    import {Section, Register} from "flowbite-svelte-blocks";
    import {Button, Checkbox, Label, Input, Alert} from 'flowbite-svelte';

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
            document.cookie = `access=${data.access}; path=/;`;
            document.cookie = `refresh=${data.refresh}; path=/;`;
            isLoggedIn.set(true);

            await goto('/profile');
        } catch (err) {
            error = err.message;
        }
    }
</script>


<Section name="login">
    <Register href="#">
        <svelte:fragment slot="top">
            DRF Trello
        </svelte:fragment>
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
            <form class="flex flex-col space-y-6" on:submit={login}>
                <h3 class="text-xl font-medium text-gray-900 dark:text-white p-0">Login</h3>
                <Label class="space-y-2">
                    <span>Your email</span>
                    <Input type="text" bind:value={email_or_mobile} placeholder="email@examle.com | 09121234567"
                           required/>
                </Label>
                <Label class="space-y-2">
                    <span>Your password</span>
                    <Input type="password" bind:value={password} placeholder="•••••" required/>
                </Label>
                <div class="flex items-start">
                    <Checkbox>Remember me</Checkbox>
                    <a href="/" class="ml-auto text-sm text-blue-700 hover:underline dark:text-blue-500">Forgot
                        password?</a>
                </div>
                {#if error}
                    <Alert color="red">
                        <span class="font-medium">{error}! </span>
                        please enter correct email or password
                    </Alert>
                {/if}
                <Button type="submit" class="w-full1">Sign in</Button>
                <p class="text-sm font-light text-gray-500 dark:text-gray-400">
                    Don’t have an account yet? <a href="/register"
                                                  class="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign
                    up</a>
                </p>
            </form>
        </div>
    </Register>
</Section>