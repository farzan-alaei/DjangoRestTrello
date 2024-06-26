<script>
    import {GradientButton} from "flowbite-svelte";
    import {isLoggedIn} from "../stores/authStore.js";
    import {onMount} from "svelte";

    onMount(() => {
        isLoggedIn.set(document.cookie.includes('access') && document.cookie.includes('refresh'));
    });

    $: loggedIn = $isLoggedIn;
</script>
<section class="bg-white dark:bg-gray-900 antialiased">
    <div class="max-w-screen-xl px-4 py-8 mx-auto lg:px-6 sm:py-16 lg:py-24">
        <div class="max-w mx-auto text-center">
            <h2 class="text-3xl font-extrabold leading-tight tracking-tight text-primary-600 sm:text-4xl dark:text-white">
                HomePage <small><small>(DRF Trello)</small></small>
            </h2>
            <p class="mt-4 text-justify text-gray-500 sm:text-xl dark:text-gray-400">
                I've crafted this project akin to Trello, serving as a comprehensive exercise to enhance my backend
                development skills and create a standout portfolio for career prospects and interviews. Leveraging
                Django and Django REST framework, I've meticulously designed robust server-side APIs that drive the
                project's functionality. From concept to completion, I've handled every aspect, emphasizing my backend
                proficiency while also delving into frontend development using SvelteKit, Tailwind CSS, and Flowbite
                Svelte for UI components.
            </p>
            <p class="mt-4 text-justify text-gray-500 sm:text-xl dark:text-gray-400">
                This project represents my dedication to mastering full-stack development practices, showcasing my
                ability to independently conceive, design, and implement a scalable web application. While my primary
                expertise lies in backend development, I've strived to create a cohesive and professional frontend
                experience, acknowledging that frontend development is an area I'm actively refining.
            </p>
        </div>

        <!-- Decorative elements -->
        <div class="mt-8 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-2">
            <!-- Example decorative elements -->
            <div class="p-6 bg-primary-200 dark:bg-gray-800 rounded-lg shadow-md">
                <h3 class="text-xl font-semibold text-primary-700 dark:text-white mb-2">Achievements</h3>
                <p class="text-gray-700 dark:text-gray-300">
                    Overcame technical challenges with Django REST framework and mastered frontend integration with
                    SvelteKit.
                </p>
            </div>
            <div class="p-6 bg-primary-200 dark:bg-gray-800 rounded-lg shadow-md">
                <h3 class="text-xl font-semibold text-primary-700 dark:text-white mb-2">Technologies Used</h3>
                <ul class="list-disc text-gray-700 dark:text-gray-300 pl-4">
                    <li>Django</li>
                    <li>Django REST framework</li>
                    <li>Tailwind CSS</li>
                    <li>SvelteKit</li>
                    <li>Flowbite Svelte</li>
                </ul>
            </div>
        </div>
        {#if !loggedIn}
            <div class="flex justify-center mt-8">
                <GradientButton shadow color="cyanToBlue" href="/register">Get Started</GradientButton>
            </div>
        {/if}
    </div>
</section>
