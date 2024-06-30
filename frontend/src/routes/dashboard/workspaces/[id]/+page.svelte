<script lang="ts">
    import {onMount} from 'svelte';
    import {page} from '$app/stores';
    import {goto} from '$app/navigation';
    import {Button, Input, Textarea, Label, Modal, Alert} from 'flowbite-svelte';
    import {InfoCircleSolid} from "flowbite-svelte-icons";

    /** @type {import('./$types').PageServerData} */
    export let data;
    console.log(data.workspace.membership);

    let editMode = false;
    let title = data.workspace.title;
    let description = data.workspace.description;
    let successMessage = '';
    let errorMessage = '';
    let defaultModal = false;


    let user = {
        id: '',
        email: '',
        mobile: ''
    };

    onMount(() => {
        const userData = localStorage.getItem('user');
        if (userData) {
            user = JSON.parse(userData);
        }
    });

    async function updateWorkspace() {
        successMessage = '';
        errorMessage = '';

        const response = await fetch(`/dashboard/workspaces/${data.workspace.id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({title, description})
        });

        if (response.ok) {
            const updatedWorkspace = await response.json();
            title = updatedWorkspace.title;
            description = updatedWorkspace.description;
            editMode = false;
            successMessage = 'Workspace updated successfully!';
        } else {
            const errorData = await response.json();
            console.error('Failed to update workspace:', errorData);
            errorMessage = 'Failed to update workspace. Please try again.';
        }
    }

    async function deleteWorkspace() {
        const response = await fetch(`/dashboard/workspaces/${data.workspace.id}/`, {
            method: 'DELETE'
        });

        if (response.ok) {
            successMessage = 'Workspace deleted successfully!';
            goto('/dashboard/workspaces');
        } else {
            const errorData = await response.json();
            console.error('Failed to delete workspace:', errorData);
            errorMessage = 'Failed to delete workspace. Please try again.';
        }
    }


    function isAdminOrOwner(workspace: any, user: any) {
        return user.id === workspace.owner.id ||
            workspace.membership.some(
                membership => membership.member.id === user.id && membership.access_level === 'admin'
            );
    }
</script>


<div class="container mx-auto p-8 bg-white dark:bg-gray-900 rounded-lg shadow-lg">
    {#if successMessage}
        <Alert border color="green" dismissable>
            <InfoCircleSolid slot="icon" class="w-5 h-5"/>
            <span class="font-medium">Success!</span>
            {successMessage}
        </Alert>
    {/if}

    {#if errorMessage}
        <Alert border color="red" dismissable>
            <InfoCircleSolid slot="icon" class="w-5 h-5"/>
            <span class="font-medium">Error!</span>
            {errorMessage}
        </Alert>
    {/if}
    <div class="p-6 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg shadow-lg">
        <div class="mb-8 text-center">
            {#if editMode}
                <Label class="space-y-2 text-white text-left">
                    <span>Workspace Title</span>
                    <Input type="text" bind:value={title}
                           class="border-gray-300 bg-primary-100 dark:bg-gray-800"/>
                </Label>
                <Label class="space-y-2 mt-2 text-white text-left">
                    <span>Description</span>
                    <Textarea bind:value={description}
                              class="mt-4 border-gray-300 bg-primary-100 dark:bg-gray-800"></Textarea>
                </Label>
                <div class="mt-4">
                    <Button on:click={updateWorkspace}
                            class="m-auto">Save
                    </Button>
                    <Button on:click={() => editMode = false}
                            class="bg-red-600 hover:bg-red-500 dark:bg-red-600 dark:hover:bg-red-500 m-auto">Cancel
                    </Button>
                </div>
            {:else}
                <h1 class="text-4xl font-extrabold text-white break-words">{title}</h1>
                <p class="text-xl text-white mt-4 break-words">{description}</p>
                <div class="mt-4">
                    {#if isAdminOrOwner(data.workspace, user)}
                        <Button on:click={() => editMode = true} class="m-auto">Edit
                        </Button>
                        <Button on:click={() => (defaultModal = true)}
                                class="bg-red-600 hover:bg-red-500 dark:bg-red-600 dark:hover:bg-red-500 m-auto">
                            Delete
                        </Button>
                        <Modal title="Delete Workspace" bind:open={defaultModal} autoclose>
                            <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">Are you sure you want
                                to delete this workspace?</p>
                            <svelte:fragment slot="footer">
                                <Button on:click={deleteWorkspace}>I accept</Button>
                                <Button color="alternative">Decline</Button>
                            </svelte:fragment>
                        </Modal>
                    {/if}
                </div>
            {/if}
        </div>
        <div class="mb-8 text-center">
            <h2 class="text-2xl font-bold text-white">Workspace Owner</h2>
            <p class="text-xl text-white mt-2 break-words">
                {#if data.workspace.owner.email}{data.workspace.owner.email}{:else if data.workspace.owner.mobile}{data.workspace.owner.mobile}{/if}
            </p>
        </div>
        {#if data.workspace.membership.length > 0}
            <div>
                <h2 class="text-3xl font-bold text-white mb-6 text-center">Members</h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                    {#each data.workspace.membership as membership}
                        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg overflow-hidden">
                            <div class="text-center">
                                <h3 class="text-xl font-bold text-gray-900 dark:text-white break-words">{membership.member.email}</h3>
                                <p class="text-md text-gray-600 dark:text-gray-300 mt-2 break-words">{membership.member.mobile}</p>
                                <p class="text-md text-gray-600 dark:text-gray-300 mt-2 break-words">Access
                                    Level: {membership.access_level}</p>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        {/if}
    </div>
</div>
