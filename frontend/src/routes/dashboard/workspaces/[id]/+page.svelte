<script lang="ts">
    import {onMount} from 'svelte';
    import {goto} from '$app/navigation';
    import {Alert, Button, Input, Label, Modal, Select, Textarea} from 'flowbite-svelte';
    import {InfoCircleSolid} from "flowbite-svelte-icons";

    /** @type {import('./$types').PageServerData} */
    export let data;

    let editMode = false;
    let successMessage = '';
    let errorMessage = '';
    let defaultModal = false;
    let deleteMemberModal = false;
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

    let members = [];

    $: if (data) {
        if (data.workspace) {
            workspace = data.workspace;
        }
        if (data.members) {
            members = data.members;
        }
    }


    onMount(() => {
        const userData = localStorage.getItem('user');
        if (userData) {
            user = JSON.parse(userData);
        }
    });

    function isAdminOrOwner({workspace, user}: { workspace: any, user: any }) {
        if (user.id === workspace.owner.id) return true;
        return workspace.membership && workspace.membership.some(
            membership => membership.member.id === user.id && membership.access_level === 'admin'
        );
    }

    async function updateWorkspace(event) {
        event.preventDefault();
        successMessage = '';
        errorMessage = '';


        const response = await fetch(`/dashboard/workspaces/${data.workspace.id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({title: workspace.title, description: workspace.description})
        });


        if (response.ok) {
            const updatedWorkspace = await response.json();
            workspace = {...updatedWorkspace};
            editMode = false;
            successMessage = 'Workspace updated successfully!';
        } else {
            const errorData = await response.json();
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
            errorMessage = 'Failed to delete workspace. Please try again.';
        }
    }

    async function deleteMember(membershipId) {
        const response = await fetch(`/dashboard/workspaces/${workspace.id}/?membershipId=${membershipId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            successMessage = 'Member deleted successfully!';
            members = members.filter(member => member.id !== membershipId);
        } else {
            const errorData = await response.json();
            errorMessage = 'Failed to delete member. Please try again.';
        }
    }

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
                <Input id="title" name="title" bind:value={workspace.title} type="text" required/>
            </div>
            <div class="mb-4">
                <Label for="description" class="block text-sm font-medium text-gray-700">Description</Label>
                <Textarea id="description" name="description" bind:value={workspace.description} required/>
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

{#if members.length > 0}
    <h2 class="mt-8 text-2xl font-semibold">Members</h2>
    <ul class="mt-4 flex flex-wrap gap-4">
        {#each members as member}
            <li class="p-4 bg-gradient-to-r from-cyan-500 to-blue-500 shadow-md rounded-lg w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
                <div class="flex flex-col justify-between h-full">
                    <div>
                        <h3 class="text-xl text-white font-medium mb-2">{member.member.first_name} {member.member.last_name}</h3>
                        <p class="text-sm text-white">{member.member.email}</p>
                        <p class="text-sm text-white">{member.member.mobile}</p>
                        <p class="text-sm text-white">{member.access_level}</p>
                    </div>
                    {#if isAdminOrOwner({workspace, user}) && member.id !== workspace.owner.id}
                        <Button color="red" class="mt-2" on:click={() => (deleteMemberModal = true)}>Remove</Button>
                    {/if}
                </div>
            </li>
            <Modal autoclose={true} bind:open={deleteMemberModal} size="md">
                <h3 class="mb-4 text-lg font-medium text-gray-900 dark:text-white">Delete member</h3>
                <p class="mb-5 text-sm font-normal text-gray-500 dark:text-gray-400">Are you sure you want to delete
                    this member?
                    This action cannot be undone.</p>
                <div class="flex justify-end space-x-2">
                    <Button on:click={() => deleteMember(member.id)}>Delete</Button>
                    <Button color="light" on:click={() => (deleteMemberModal = false)}>Cancel</Button>
                </div>
            </Modal>
        {/each}
    </ul>

{/if}
