<script lang="ts">
    import {onMount} from 'svelte';
    import {goto, invalidate} from '$app/navigation';
    import {Alert, Button, Input, Label, Modal, Select, Textarea} from 'flowbite-svelte';
    import {InfoCircleSolid} from "flowbite-svelte-icons";


    /** @type {import('./$types').PageServerData} */
    export let data;

    let editMode = false;
    let title = '';
    let description = '';
    let successMessage = '';
    let errorMessage = '';
    let defaultModal = false;
    let memberModal = false;
    let accessLevel = 'member';
    let newMemberEmail = '';
    let newMemberMobile = '';
    let workspace = {
        id: "",
        title: "",
        description: "",
        owner: {
            email: "",
            id: "",
            last_name: "",
            mobile: "",
        },
    };
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
        if (data.workspace) {
            workspace = data.workspace;
            title = workspace.title;
            description = workspace.description;
        }
    });

    console.log(data.workspace)

    function isAdminOrOwner({workspace, user}: { workspace: any, user: any }) {
        return user.id === workspace.owner.id ||
            workspace.membership.some(
                membership => membership.member.id === user.id && membership.access_level === 'admin'
            );
    }

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
            workspace = {...updatedWorkspace};
            editMode = false;
            successMessage = 'Workspace updated successfully!';
            await invalidate();
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

    // async function inviteMember(event) {
    //     event.preventDefault();
    //     const form = event.target;
    //     const formData = new FormData(form);
    //     const response = await fetch('/dashboard/workspaces/[id]', {
    //         method: 'POST',
    //         body: formData
    //     });
    //
    //     if (response.ok) {
    //         successMessage = 'Member invited successfully!';
    //         await invalidate();
    //         memberModal = false;
    //     } else {
    //         const errorData = await response.json();
    //         errorMessage = 'Failed to invite member. Please try again.';
    //     }
    // }
</script>

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
    <div class="mt-6">
        <Alert border color="red" dismissible>
            <InfoCircleSolid slot="icon" class="w-5 h-5"/>
            <span class="font-medium">Error!</span>
            {errorMessage}
        </Alert>
    </div>
{/if}

<div class="bg-gradient-to-r from-cyan-500 to-blue-500 p-6 rounded-lg shadow-lg">
    <h1 class="text-3xl font-bold text-white">{workspace.title}</h1>
    <p class="text-md text-white mt-4">{workspace.description}</p>

    {#if isAdminOrOwner({workspace, user})}
        <div class="mt-4 flex space-x-4">
            <Button class="flex" on:click={() => (editMode = true)}>Edit</Button>
            <Button color="red" class="flex" on:click={() => (defaultModal = true)}>Delete</Button>
        </div>
    {/if}
</div>

{#if editMode}
    <div class="mt-4 p-6 rounded-lg shadow-lg bg-white">
        <form on:submit={updateWorkspace}>
            <div class="mb-4">
                <Label for="title" class="block text-sm font-medium text-gray-700">Title</Label>
                <Input id="title" name="title" bind:value={title} type="text" required/>
            </div>
            <div class="mb-4">
                <Label for="description" class="block text-sm font-medium text-gray-700">Description</Label>
                <Textarea id="description" name="description" bind:value={description} required/>
            </div>
            <Button type="submit" class="w-full">Save</Button>
            <Button color="light" class="mt-2 w-full" on:click={() => (editMode = false)}>Cancel</Button>
        </form>
    </div>
{/if}

<Modal autoclose={false} bind:open={defaultModal} size="md">
    <h3 class="mb-4 text-lg font-medium text-gray-900 dark:text-white">Delete Workspace</h3>
    <p class="mb-5 text-sm font-normal text-gray-500 dark:text-gray-400">Are you sure you want to delete this workspace?
        This action cannot be undone.</p>
    <div class="flex justify-end space-x-2">
        <Button on:click={deleteWorkspace}>Delete</Button>
        <Button color="light" on:click={() => (defaultModal = false)}>Cancel</Button>
    </div>
</Modal>

{#if isAdminOrOwner({workspace, user})}
    <div class="mt-6 flex justify-center">
        <Button on:click={() => (memberModal = true)} class="flex">Invite Member</Button>
    </div>

    <Modal bind:open={memberModal} size="xs" autoclose={false} class="w-full">
        <form class="flex flex-col space-y-6">
            <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Invite New Member</h3>
            <Label class="space-y-2">
                <span>Email</span>
                <Input type="email" name="email" bind:value={newMemberEmail} placeholder="Email" class="border"
                       required/>
            </Label>
            <Label class="space-y-2">
                <span>Mobile</span>
                <Input type="tel" name="mobile" bind:value={newMemberMobile} placeholder="Mobile" class="border"/>
            </Label>
            <Label class="space-y-2">
                <span>Access Level</span>
                <Select name="access_level" bind:value={accessLevel} required>
                    <option value="member">Member</option>
                    <option value="admin">Admin</option>
                </Select>
            </Label>
            <Button type="submit" class="w-full">Invite</Button>
        </form>
    </Modal>
{/if}
