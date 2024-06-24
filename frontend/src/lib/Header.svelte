<!-- src/lib/Header.svelte -->
<script>
    import {page} from '$app/stores';
    import {goto} from '$app/navigation';
    import {isLoggedIn} from '../stores/authStore';
    import {onMount} from 'svelte';
    import {Navbar, NavBrand, NavLi, NavUl, NavHamburger, Button} from 'flowbite-svelte';
    import {DarkMode} from "flowbite-svelte";

    $: activeUrl = $page.url.pathname;
    let activeClass = 'text-white bg-green-700 md:bg-transparent md:text-green-700 md:dark:text-white dark:bg-green-600 md:dark:bg-transparent';
    let nonActiveClass = 'text-gray-700 hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-green-700 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent';


    onMount(() => {
        isLoggedIn.set(document.cookie.includes('access') && document.cookie.includes('refresh'));
    });

    $: loggedIn = $isLoggedIn;

    async function logout() {
        const refreshToken = localStorage.getItem('refresh');

        const response = await fetch('/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                refresh: refreshToken
            })
        });

        if (response.ok) {
            document.cookie = 'access=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
            document.cookie = 'refresh=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
            isLoggedIn.set(false);
            await goto('/');
        } else {
            const errorData = await response.json();
            console.error('Failed to logout:', errorData);
        }
    }

</script>


<Navbar>
    <NavBrand href="/">
        <img src="/django-icon-svgrepo-com%20(1).svg" class="me-2 h-4 sm:h-6" alt="django Logo"/>
        <span class="self-center whitespace-nowrap text-lg font-semibold dark:text-white">DRF Trello</span>
    </NavBrand>
    <div class="flex items-center md:order-1 space-x-1">
        {#if loggedIn}
            <Button size="xs" color="none"></Button>
            <Button size="xs" href="/" on:click={logout}>logout</Button>
        {:else}
            <Button size="xs" color="none" class="border dark:border-gray-800" href="/login">login</Button>
            <Button size="xs" href="/register">signup</Button>
        {/if}
        <DarkMode class="text-primary-500 dark:text-primary-600 border dark:border-gray-800 p-1.5 text-sm"/>
        <NavHamburger />
    </div>
    <NavUl {activeUrl} {activeClass} {nonActiveClass}>
        <NavLi href="/"> Home</NavLi>
        {#if loggedIn}
            <NavLi href="/profile">Profile</NavLi>
        {/if}
        <NavLi href="/about">About</NavLi>
        <NavLi href="/contact">Contact</NavLi>
    </NavUl>
</Navbar>