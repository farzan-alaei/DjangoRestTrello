<script lang="ts">
    /** @type {import('./$types').PageServerData} */
    import {Button, Modal, Label, Input} from 'flowbite-svelte';
    import {page} from "$app/stores";

    let formModal = false;
    let workspaceTitle = '';
    let workspaceDescription = '';
    export let data;


    async function createWorkspace() {
        try {
            const response = await fetch('/dashboard/workspaces/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({title: workspaceTitle, description: workspaceDescription}),
            });

            if (response.ok) {
                const newWorkspace = await response.json();
                data.workspaces = [...data.workspaces, newWorkspace];


                formModal = false;
                workspaceTitle = '';
                workspaceDescription = '';
            } else {
                console.error('Failed to create workspace');
            }
        } catch (error) {
            console.error('Error:', error);
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
            <Input type="text" bind:value={workspaceTitle} placeholder="Title" required/>
        </Label>
        <Label class="space-y-2">
            <span>Description</span>
            <Input type="text" bind:value={workspaceDescription} placeholder="Description" required/>
        </Label>
        <Button type="submit" class="w-full">Create Workspace</Button>
    </form>
</Modal>


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


