<script lang="ts">
    import {Alert, Button, Input, Label, Modal, Select, Textarea} from 'flowbite-svelte';
    import {InfoCircleSolid} from "flowbite-svelte-icons";


    /** @type {import('./$types').PageData} */
    export let data;
    let formModal = false;
    let boardTitle = '';
    let boardDescription = '';
    let selectedWorkspace = '';
    let accessToken = '';
    let successMessage = '';
    let errorMessage = '';

    async function createBoard() {
        try {
            const workspace = JSON.parse(selectedWorkspace);
            const body = {
                title: boardTitle,
                description: boardDescription,
                workspace: {
                    id: workspace.id,
                    title: workspace.title
                }
            };


            const response = await fetch('/dashboard/boards', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify(body)
            });

            if (response.ok) {
                const newBoard = await response.json();
                data.boards = [...data.boards, newBoard];
                formModal = false;
                boardTitle = '';
                boardDescription = '';
                selectedWorkspace = '';
                successMessage = 'Board created successfully!';
            } else {
                const errorData = await response.json();
                throw new Error(errorData.message);
            }
        } catch (error) {
            console.error('Error creating board:', error);
            errorMessage = 'Failed to create board. Please try again.';
        }
    }
</script>

<div class="mt-4">
    <h1 class="text-3xl text-center font-bold dark:text-white">My boards</h1>
</div>

<div class="flex justify-center mt-4">
    <Button class="flex" on:click={() => (formModal = true)}>Add boards</Button>
</div>

<Modal autoclose={false} bind:open={formModal} class="w-full" size="xs">
    <form class="flex flex-col space-y-6" on:submit|preventDefault={createBoard}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Create a New Board</h3>
        <Label class="space-y-2">
            <span>Title</span>
            <Input bind:value={boardTitle} class="border" placeholder="Title" required type="text"/>
        </Label>
        <Label class="space-y-2">
            <span>Description</span>
            <Textarea bind:value={boardDescription} class="border" placeholder="Description" required type="text"/>
        </Label>
        <Label class="space-y-2">
            <span>Workspace</span>
            <Select bind:value={selectedWorkspace} class="border" required>
                <option disabled value="">Select a Workspace</option>
                {#each data.workspaces as workspace}
                    <option value={JSON.stringify(workspace)}>{workspace.title}</option>
                {/each}
            </Select>
        </Label>
        <Button class="w-full" type="submit">Create Board</Button>
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

<div class="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
    {#if data.boards && data.boards.length > 0}
        {#each data.boards as board}
            <div class="bg-gradient-to-r from-cyan-500 to-blue-500 p-6 rounded-lg shadow-lg transform transition-all hover:scale-105">
                <h2 class="text-2xl font-bold text-white mb-2">
                    <a href={`/dashboard/boards/${board.id}`} class="hover:underline">{board.title}</a>
                </h2>
                <h3 class="text-lg font-bold text-white mb-2">
                    workspace name: {board.workspace.title}
                </h3>
            </div>
        {/each}
    {:else}
        <p class="text-gray-500 col-span-full text-center">No boards available.</p>
    {/if}
</div>
