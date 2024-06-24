<script>
    import {goto} from '$app/navigation';
    import {isLoggedIn} from "../../stores/authStore.js";

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


<section class="bg-gray-50 dark:bg-gray-900">
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
        <p class="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
            Django Rest Trello
        </p>
        <div class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
            <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                    Create an account
                </h1>
                <form class="space-y-4 md:space-y-6" on:submit|preventDefault={register}>
                    <div>
                        <label for="email or mobile"
                               class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Email or
                            Mobile</label>
                        <input type="text" bind:value={email_or_mobile}
                               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                               placeholder="email@examle.com | 09121234567" required="">
                    </div>
                    <div>
                        <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
                        <input type="password" bind:value={password} placeholder="••••••••"
                               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                               required="">
                    </div>
                    <div>
                        <label for="confirm-password"
                               class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Confirm
                            password</label>
                        <input type="password" bind:value={confirmPassword}
                               placeholder="••••••••"
                               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                               required="">
                    </div>
                    <div class="flex items-start">
                        <div class="flex items-center h-5">
                            <input id="terms" aria-describedby="terms" type="checkbox"
                                   class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800"
                                   required="">
                        </div>
                        <div class="ml-3 text-sm">
                            <label for="terms" class="font-light text-gray-500 dark:text-gray-300">I accept the <a
                                    class="font-medium text-primary-600 hover:underline dark:text-primary-500" href="/">Terms
                                and Conditions</a></label>
                        </div>
                    </div>
                    {#if error}
                        <p class="text-red-500 text-xl italic">{error}</p>
                    {/if}
                    <button type="submit"
                            class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">
                        Create an account
                    </button>
                    <p class="text-sm font-light text-gray-500 dark:text-gray-400">
                        Already have an account? <a href="/login"
                                                    class="font-medium text-primary-600 hover:underline dark:text-primary-500">Login
                        here</a>
                    </p>
                </form>
            </div>
        </div>
    </div>
</section>