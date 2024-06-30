<script>
    import {onMount} from 'svelte';
    import {Label, Alert, Input, GradientButton} from 'flowbite-svelte';
    import {InfoCircleSolid} from "flowbite-svelte-icons";

    let user = {
        email: '',
        mobile: '',
        first_name: '',
        last_name: ''
    };
    let editMode = false;
    let successMessage = '';
    let errorMessage = '';

    onMount(() => {
        const userData = localStorage.getItem('user');
        if (userData) {
            user = JSON.parse(userData);
        }
    });

    async function updateProfile() {
        successMessage = '';
        errorMessage = '';

        const response = await fetch('/dashboard', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });

        if (response.ok) {
            const updatedUser = await response.json();
            user = updatedUser;
            editMode = false;
            localStorage.setItem('user', JSON.stringify(user));
            successMessage = 'Profile updated successfully!';
        } else {
            const errorData = await response.json();
            console.error('Failed to update profile:', errorData);
            errorMessage = 'Failed to update profile. Please try again.';
        }
    }
</script>

<div class="mt-12">
    <h1 class="text-3xl text-center font-bold dark:text-white">
        Hello
        {#if user.first_name} {user.first_name} {user.last_name}{:else if user.mobile}{user.mobile}{:else if user.email}{user.email}{/if}
        !
    </h1>
    <p class="text-xl text-center mt-3 font-bold dark:text-white">Welcome to your dashboard</p>
</div>

<div class="mt-6 max-w-2xl mx-auto">
    <form on:submit|preventDefault={updateProfile}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Profile Information</h3>

        {#if successMessage}
            <Alert border color="green">
                <InfoCircleSolid slot="icon" class="w-5 h-5"/>
                <span class="font-medium">Success!</span>
                {successMessage}
            </Alert>
        {/if}

        {#if errorMessage}
            <Alert border color="red">
                <InfoCircleSolid slot="icon" class="w-5 h-5"/>
                <span class="font-medium">Error!</span>
                {errorMessage}
            </Alert>
        {/if}

        <Label class="space-y-2">
            <span>Email</span>
            <Input type="text" value={user.email} class="border" readonly disabled/>
        </Label>
        <Label class="mt-4">
            <span>Mobile</span>
            <Input type="text" value={user.mobile} class="border" readonly disabled/>
        </Label>
        <Label class="mt-4">
            <span>First Name</span>
            <Input type="text" bind:value={user.first_name} class="border"/>
        </Label>
        <Label class="mt-4">
            <span>Last Name</span>
            <Input type="text" bind:value={user.last_name} class="border"/>
        </Label>
        <GradientButton size="xl" type="submit" class="mt-6" shadow color="cyanToBlue">Update Profile</GradientButton>
    </form>
</div>
