<script>
    import {GradientButton} from "flowbite-svelte";
    import {onMount} from "svelte";
    import {isLoggedIn} from "../../stores/authStore.js";

    let user = {};

    onMount(() => {
        const userData = localStorage.getItem('user');
        if (userData) {
            user = JSON.parse(userData);
        }
    });
</script>

<div class="mt-12">
    <h1 class="text-3xl text-center font-bold dark:text-white">Hello
        {#if user.first_name}{user.first_name} {user.last_name}{:else if user.mobile}{user.mobile}{:else if user.email}{user.email}{/if}
        !</h1>
    <p class="text-xl text-center mt-3 font-bold dark:text-white">Welcome to your dashboard</p>
</div>

<div class="mt-6">
    <h2 class="text-2xl text-center font-bold dark:text-white">Welcome to your profile page <small>(DRF Trello)</small>
    </h2>
</div>


<div class="flex justify-center mt-8">
    <GradientButton size="xl" shadow color="cyanToBlue" href="/dashboard/workspaces">Go to Workspaces</GradientButton>
</div>



