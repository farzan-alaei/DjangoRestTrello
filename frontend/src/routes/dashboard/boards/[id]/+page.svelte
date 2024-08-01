<script lang="ts">
    import {goto} from '$app/navigation';
    import {Alert, Button, Input, Label, Modal, Textarea} from 'flowbite-svelte';
    import {InfoCircleSolid} from "flowbite-svelte-icons";
    import {dndzone} from 'svelte-dnd-action';
    import {onMount} from "svelte";

    /** @type {import('./$types').PageServerData} */
    export let data;
    let editMode = false;
    let defaultModal = false;
    let createListModal = false;
    let deleteListModal = false;
    let board = data.board;
    let lists = data.lists;
    let successMessage = '';
    let errorMessage = '';
    let newListTitle = '';
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


    function isAdminOrOwner({board, user}: { board: any, user: any }) {
        if (user.id === board.owner) return true;
    }

    let dndLists = lists.map(lists => ({...lists, items: lists.tasks}));


    function handleDndEvent(event) {
        const {items} = event.detail;
        dndLists = items;
        console.log('Dnd Event:', items);
    }

    async function deleteBoard() {
        try {
            const response = await fetch(`/dashboard/boards/${board.id}/`, {
                method: 'DELETE'
            });

            if (response.ok) {
                successMessage = 'Board deleted successfully!';
                goto('/dashboard/boards');
            } else {
                const errorData = await response.json();
                errorMessage = 'Failed to delete board. Please try again.';
                console.error('Failed to delete board:', errorData);
            }
        } catch (error) {
            errorMessage = 'An error occurred. Please try again.';
            console.error('Error:', error);
        }
    }


    async function updateBoard(event) {
        event.preventDefault();
        successMessage = '';
        errorMessage = '';

        const response = await fetch(`/dashboard/boards/${board.id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({title: board.title, description: board.description})
        });

        if (response.ok) {
            const updatedBoard = await response.json();
            board = {...updatedBoard};
            editMode = false;
            successMessage = 'Board updated successfully!';
        } else {
            const errorData = await response.json();
            errorMessage = 'Failed to update board. Please try again.';
        }
    }

    async function createList(event) {
        event.preventDefault();
        successMessage = '';
        errorMessage = '';

        try {
            const response = await fetch(`/dashboard/boards/${board.id}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({title: newListTitle, board: board.id})
            });

            if (response.ok) {
                const newList = await response.json();
                lists = [...lists, newList];
                dndLists = lists.map(list => ({...list, items: list.tasks}));
                createListModal = false;
                newListTitle = '';
                successMessage = 'List created successfully!';
            } else {
                const errorData = await response.json();
                errorMessage = 'Failed to create list. Please try again.';
                console.error('Failed to create list:', errorData);
            }
        } catch (error) {
            errorMessage = 'An error occurred. Please try again.';
            console.error('Error:', error);
        }
    }


    async function deleteList(listId) {
        try {
            const response = await fetch(`/dashboard/boards/${board.id}/?listId=${listId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                successMessage = 'List deleted successfully!';
                lists = lists.filter(list => list.id !== listId);
                dndLists = lists.map(list => ({...list, items: list.tasks}));
            } else {
                const errorData = await response.json();
                errorMessage = 'Failed to delete list. Please try again.';
                console.error('Failed to delete list:', errorData);
            }
        } catch (error) {
            errorMessage = 'An error occurred. Please try again.';
            console.error('Error:', error);
        }
    }


</script>

<style>
    .list-container {
        display: flex;
        overflow-x: auto;
    }

    .list {
        margin: 0 1rem;
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        min-width: 200px;
    }

    .task {
        background-color: #f0f0f0;
        margin-bottom: 0.5rem;
        padding: 0.5rem;
        border-radius: 0.25rem;
    }
</style>

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
    <h1 class="text-3xl font-bold text-white">{board.title}</h1>
    <p class="text-md text-white mt-4">{board.description}</p>
    {#if isAdminOrOwner({board, user})}
        <div class="mt-4 flex space-x-4">
            <Button class="flex" on:click={() => (editMode = true)}>Edit</Button>
            <Button class="flex" color="red" on:click={() => (defaultModal = true)}>Delete</Button>
            <Button class="flex" color="green" on:click={() => (createListModal = true)}>Add List</Button>
        </div>
    {/if}
</div>

{#if editMode}
    <div class="mt-4 p-6 rounded-lg shadow-lg bg-white">
        <form on:submit={updateBoard}>
            <div class="mb-4">
                <Label for="title" class="block text-sm font-medium text-gray-700">Title</Label>
                <Input id="title" name="title" bind:value={board.title} type="text" required/>
            </div>
            <div class="mb-4">
                <Label for="description" class="block text-sm font-medium text-gray-700">Description</Label>
                <Textarea id="description" name="description" bind:value={board.description} required/>
            </div>
            <Button type="submit" class="w-full">Save</Button>
            <Button color="light" class="mt-2 w-full" on:click={() => (editMode = false)}>Cancel</Button>
        </form>
    </div>
{/if}

<Modal autoclose={false} bind:open={defaultModal} size="md">
    <h3 class="mb-4 text-lg font-medium text-gray-900 dark:text-white">Delete Board</h3>
    <p class="mb-5 text-sm font-normal text-gray-500 dark:text-gray-400">Are you sure you want to delete this Board?
        This action cannot be undone.</p>
    <div class="flex justify-end space-x-2">
        <Button on:click={deleteBoard}>Delete</Button>
        <Button color="light" on:click={() => (defaultModal = false)}>Cancel</Button>
    </div>
</Modal>

<Modal autoclose={false} bind:open={createListModal} size="md">
    <h3 class="mb-4 text-lg font-medium text-gray-900 dark:text-white">Create New List</h3>
    <form on:submit={createList}>
        <div class="mb-4">
            <Label class="block text-sm font-medium text-gray-700" for="newListTitle">Title</Label>
            <Input bind:value={newListTitle} id="newListTitle" name="title" required type="text"/>
        </div>
        <div class="flex justify-end space-x-2">
            <Button type="submit">Create</Button>
            <Button color="light" on:click={() => (createListModal = false)}>Cancel</Button>
        </div>
    </form>
</Modal>

{#if dndLists.length > 0}
    <div class="list-container">
        {#each dndLists as list (list.id)}
            <div class="list">
                <h2 class="text-xl font-bold">{list.title}</h2>
                <div use:dndzone={{items: list.items, flipDurationMs: 300}} on:consider={handleDndEvent}
                     on:finalize={handleDndEvent}>
                    <div class="flex justify-end space-x-2">
                        <Button on:click={() => (deleteListModal = true)}>Delete</Button>
                    </div>
                    <Modal autoclose={true} bind:open={deleteListModal} size="md">
                        <h3 class="mb-4 text-lg font-medium text-gray-900 dark:text-white">Delete List</h3>
                        <p class="mb-5 text-sm font-normal text-gray-500 dark:text-gray-400">Are you sure you want to
                            delete this List?
                            This action cannot be undone.</p>
                        <div class="flex justify-end space-x-2">
                            <Button on:click={() => deleteList(list.id)}>Delete</Button>
                            <Button color="light" on:click={() => (deleteListModal = false)}>Cancel</Button>
                        </div>
                    </Modal>
                    {#each list.items as task (task.id)}
                        <div class="task" data-id={task.id}>
                            <h3 class="text-md font-medium">{task.title}</h3>
                            <p class="text-sm">{task.description}</p>
                        </div>
                    {/each}
                </div>
            </div>
        {/each}
    </div>
{/if}

