<script lang="ts">
    import {Alert, Button, Input, Label, Modal, Textarea} from 'flowbite-svelte';
    import {InfoCircleSolid} from "flowbite-svelte-icons";

    let formModal = false;
    let workspaceTitle = '';
    let workspaceDescription = '';
    let successMessage = '';
    let errorMessage = '';

    /** @type {import('./$types').PageData} */
    export let data;
    async function createWorkspace() {
        successMessage = '';
        errorMessage = '';

        try {
            const response = await fetch('/dashboard/workspaces', { // Adjust path as needed
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
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
</script>

<div class="mt-4">
    <h1 class="text-3xl text-center font-bold dark:text-white">My Workspaces</h1>
</div>

<div class="flex justify-center mt-4">
    <Button class="flex" on:click={() => (formModal = true)}>Add Workspace</Button>
</div>

<Modal autoclose={false} bind:open={formModal} class="w-full" size="xs">
    <form class="flex flex-col space-y-6" on:submit|preventDefault={createWorkspace}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Create a New Workspace</h3>
        <Label class="space-y-2">
            <span>Title</span>
            <Input bind:value={workspaceTitle} class="border" placeholder="Title" required type="text"/>
        </Label>
        <Label class="space-y-2">
            <span>Description</span>
            <Textarea bind:value={workspaceDescription} class="border" placeholder="Description" required type="text"/>
        </Label>
        <Button class="w-full" type="submit">Create Workspace</Button>
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
        <Alert border color="red" dismissible>
            <InfoCircleSolid slot="icon" class="w-5 h-5"/>
            <span class="font-medium">Error!</span>
            {errorMessage}
        </Alert>
    </div>
{/if}

<div class="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-2">
    {#if data.workspaces && data.workspaces.length > 0}
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
