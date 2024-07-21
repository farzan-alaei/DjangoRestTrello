<script lang="ts">
    import {Button, Modal, Label, Input, Textarea, Alert} from 'flowbite-svelte';
    import {onMount} from 'svelte';
    import {page} from "$app/stores";
    import {getAccessToken} from '../../../stores/authStore.js';
    import {InfoCircleSolid} from "flowbite-svelte-icons";

    let formModal = false;
    let workspaceTitle = '';
    let workspaceDescription = '';
    let data = {workspaces: []};
    let successMessage = '';
    let errorMessage = '';

    onMount(async () => {
        try {
            const accessToken = getAccessToken();
            if (!accessToken) {
                throw new Error('Access token not found');
            }
            const response = await fetch('http://127.0.0.1:8000/api/workspaces/', {
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });

            if (response.ok) {
                const workspaces = await response.json();
                data.workspaces = workspaces || [];
            } else {
                throw new Error('Failed to load workspaces');
            }
        } catch (error) {
            console.error('Error loading workspaces:', error);
            errorMessage = 'Failed to load workspaces. Please try again.';
        }
    });

    async function createWorkspace() {
        successMessage = '';
        errorMessage = '';

        try {
            const accessToken = getAccessToken();
            if (!accessToken) {
                throw new Error('Access token not found');
            }

            const response = await fetch('http://127.0.0.1:8000/api/workspaces/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({title: workspaceTitle, description: workspaceDescription})
            });

            if (response.ok) {
                const newWorkspace = await response.json();
                data.workspaces = [...data.workspaces, newWorkspace];
                formModal = false;
                workspaceTitle = '';
                workspaceDescription = '';
                successMessage = 'Workspace created successfully!';
            } else {
                throw new Error('Failed to create workspace');
            }
        } catch (error) {
            console.error('Error:', error);
            errorMessage = 'Failed to create workspace. Please try again.';
        }
    }

    $: $page.url.pathname;
</script>

<div class="mt-4">
    <h1 class="text-3xl text-center font-bold dark:text-white">My Workspaces</h1>
</div>

<div class="flex justify-center mt-4">
    <Button on:click={() => (formModal = true)} class="flex">Add Workspace</Button>
</div>

<Modal bind:open={formModal} size="xs" autoclose={false} class="w-full">
    <form class="flex flex-col space-y-6" on:submit|preventDefault={createWorkspace}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Create a New Workspace</h3>
        <Label class="space-y-2">
            <span>Title</span>
            <Input type="text" bind:value={workspaceTitle} placeholder="Title" class="border" required/>
        </Label>
        <Label class="space-y-2">
            <span>Description</span>
            <Textarea type="text" bind:value={workspaceDescription} class="border" placeholder="Description" required/>
        </Label>
        <Button type="submit" class="w-full">Create Workspace</Button>
    </form>
</Modal>

{#if successMessage}
    <div class="mt-6">
        <Alert border color="green" dismissible>
            <InfoCircleSolid slot="icon" class="w-5 h-5"/>
            <span class="font-medium">Success!</span>
            {successMessage}
        </Alert>
    </div>
{/if}

{#if errorMessage}
    <div class="m-6">
        <Alert border color="red" dissmissible>
            <InfoCircleSolid slot="icon" class="w-5 h-5"/>
            <span class="font-medium">Error!</span>
            {errorMessage}
        </Alert>
    </div>
{/if}

<div class="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-2">
    {#if data.workspaces.length > 0}
        {#each data.workspaces as workspace}
            <div class="bg-gradient-to-r from-cyan-500 to-blue-500 p-6 rounded-lg shadow-lg">
                <h3 class="text-xl font-bold text-white">
                    <a href={`/dashboard/workspaces/${workspace.id}`}>{workspace.title}</a>
                </h3>
                <div class="mt-2 flex items-center border-t border-white pt-3">
                    <p class="text-md text-white mt-2">
                        {workspace.description}
                    </p>
                </div>
            </div>
        {/each}

    {:else}
        <p class="text-gray-500">No workspaces available.</p>
    {/if}
</div>
