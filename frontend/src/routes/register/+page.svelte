<script>
    import {goto} from '$app/navigation';
    import {isLoggedIn} from "../../stores/authStore.js";
    import {Button, Checkbox, Input, Label, Alert} from "flowbite-svelte";
    import {Register, Section} from "flowbite-svelte-blocks";

    let email_or_mobile = '';
    let password = '';
    let confirmPassword = '';
    let error = '';

    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;':"\\,.<>\/?]).{10,}$/;

    async function register(event) {
        event.preventDefault();
        if (password !== confirmPassword) {
            error = 'Passwords do not match';
            return;
        }

        if (!passwordRegex.test(password)) {
            error = "Password must be at least 10 characters" +
                " long and include at least one uppercase letter, " +
                "one lowercase letter, one number, and one special character";
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
            document.cookie = `access=${data.access}; path=/;`;
            document.cookie = `refresh=${data.refresh}; path=/;`;
            isLoggedIn.set(true);

            await goto('/profile');
        } catch (err) {
            error = err.message;
        }
    }


</script>


<Section name="register">
    <Register href="#">
        <svelte:fragment slot="top">
            DRF Trello
        </svelte:fragment>
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
            <form class="flex flex-col space-y-6" on:submit|preventDefault={register}>
                <h3 class="text-xl font-bold text-gray-900 dark:text-white p-0">Create an account</h3>
                <Label class="space-y-2">
                    <span>Email or Mobile</span>
                    <Input type="text" bind:value={email_or_mobile} placeholder="email@examle.com | 09121234567"
                           required/>
                </Label>
                <Label class="space-y-2">
                    <span>password</span>
                    <Input type="password" bind:value={password} placeholder="•••••" required/>
                </Label>
                <Label class="space-y-2">
                    <span>confirm password</span>
                    <Input type="password" bind:value={confirmPassword} placeholder="•••••" required/>
                </Label>
                <div class="flex items-start">
                    <Checkbox>Remember me</Checkbox>
                    <a href="/" class="ml-auto text-sm text-blue-700 hover:underline dark:text-blue-500">Forgot
                        password?</a>
                </div>
                {#if error}
                    <Alert color="red">
                        <span class="font-medium">{error}! </span>
                        please enter correct email, phone or password
                    </Alert>
                {/if}
                <Button type="submit" class="w-full1">Create an account</Button>
                <p class="text-sm font-light text-gray-500 dark:text-gray-400">
                    Already have an account? <a href="/login"
                                                class="font-medium text-primary-600 hover:underline dark:text-primary-500">login</a>
                </p>
            </form>
        </div>
    </Register>
</Section>