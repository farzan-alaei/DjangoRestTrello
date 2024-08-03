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
    let addTaskModal = false;
    let editListModal = false;  // New state for edit list modal
    let editTaskModal = false;  // New state for edit task modal
    let deleteTaskModal = false;
    let board = data.board;
    let lists = data.lists;
    let successMessage = '';
    let errorMessage = '';
    let newListTitle = '';
    let newTaskTitle = '';
    let user = {
        id: '',
        email: '',
        mobile: ''
    };
    let listToDelete = null;
    let taskListId = null;
    let taskId = null;
    let editingList = null;
    let updatedListTitle = '';
    let updatedTaskTitle = '';
    let isHandlingDnd = false;

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

    async function handleDndEvent(event, listId) {

        const {items} = event.detail;
        lists = lists.map(list => list.id === listId ? {...list, tasks: items} : list);
        dndLists = lists.map(list => ({...list, items: list.tasks}));
        console.log('Dnd Event:', items);

        for (const item of items) {
            await saveTaskOrder(listId, item.id);
        }

    }

    async function saveTaskOrder(listId, taskId) {
        const response = await fetch(`/dashboard/boards/${board.id}/?listId=${listId}&taskId=${taskId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            console.error('Error saving task order');
        }
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
                lists = [newList, ...lists];
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
                deleteListModal = false;
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

    async function addTask(event) {
        event.preventDefault();
        successMessage = '';
        errorMessage = '';

        try {
            const response = await fetch(`/dashboard/boards/${board.id}/?list_id=${taskListId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({title: newTaskTitle})
            });

            if (response.ok) {
                const newTask = await response.json();
                lists = lists.map(list => {
                    if (list.id === taskListId) {
                        return {...list, tasks: [...list.tasks, newTask]};
                    } else {
                        return list;
                    }
                });
                dndLists = lists.map(list => ({...list, items: list.tasks}));
                addTaskModal = false;
                newTaskTitle = '';
                successMessage = 'Task added successfully!';
            } else {
                const errorData = await response.json();
                errorMessage = 'Failed to add task. Please try again.';
                console.error('Failed to add task:', errorData);
            }
        } catch (error) {
            errorMessage = 'An error occurred. Please try again.';
            console.error('Error:', error);
        }
    }


    async function updateList(event) {
        event.preventDefault();
        successMessage = '';
        errorMessage = '';

        if (!editingList) return;

        try {
            const response = await fetch(`/dashboard/boards/${board.id}/?listId=${editingList.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({title: updatedListTitle})
            });

            if (response.ok) {
                const updatedList = await response.json();
                lists = lists.map(list => list.id === editingList.id ? updatedList : list);
                dndLists = lists.map(list => ({...list, items: list.tasks}));
                editListModal = false;
                editingList = null;
                updatedListTitle = '';
                successMessage = 'List updated successfully!';
            } else {
                const errorData = await response.json();
                errorMessage = 'Failed to update list. Please try again.';
                console.error('Failed to update list:', errorData);
            }
        } catch (error) {
            errorMessage = 'An error occurred. Please try again.';
            console.error('Error:', error);
        }
    }


    async function updateTask(event) {
        event.preventDefault();
        successMessage = '';
        errorMessage = '';

        try {
            const response = await fetch(`/dashboard/boards/${board.id}/?taskListId=${taskListId}&taskId=${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({title: updatedTaskTitle})
            });


            if (response.ok) {
                const updatedTask = await response.json();
                lists = lists.map(list => {
                    if (list.id === taskListId) {
                        return {
                            ...list,
                            tasks: list.tasks.map(task => task.id === updatedTask.id ? updatedTask : task)
                        };
                    } else {
                        return list;
                    }
                });
                dndLists = lists.map(list => ({...list, items: list.tasks}));
                editTaskModal = false;
                editingList = null;
                updatedTaskTitle = '';
                successMessage = 'Task updated successfully!';
            } else {
                const errorData = await response.json();
                errorMessage = 'Failed to update task. Please try again.';
                console.error('Failed to update task:', errorData);
            }
        } catch (error) {
            errorMessage = 'An error occurred. Please try again.';
            console.error('Error:', error);
        }
    }


    async function deleteTask(taskId) {
        successMessage = '';
        errorMessage = '';

        try {
            const response = await fetch(`/dashboard/boards/${board.id}/?taskId=${taskId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                lists = lists.map(list => {
                    return {
                        ...list,
                        tasks: list.tasks.filter(task => task.id !== taskId)
                    };
                });
                dndLists = lists.map(list => ({...list, items: list.tasks}));
                deleteTaskModal = false;
                successMessage = 'Task deleted successfully!';
            } else {
                const errorData = await response.json();
                errorMessage = 'Failed to delete task. Please try again.';
                console.error('Failed to delete task:', errorData);
            }
        } catch (error) {
            errorMessage = 'An error occurred. Please try again.';
            console.error('Error:', error);
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


<Modal autoclose={false} bind:open={createListModal} class="w-full" size="xs">
    <form class="flex flex-col space-y-6" on:submit={createList}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Create a New Task</h3>
        <Label class="space-y-2">
            <span>Title</span>
            <Input bind:value={newListTitle} class="border" name="title" placeholder="Title" required type="text"/>
        </Label>
        <Button class="w-full" type="submit">Create</Button>
    </form>
</Modal>

{#if dndLists.length > 0}
    <div class="mt-6 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {#each dndLists as list}
            <div class="p-4 rounded-lg shadow-lg bg-gray-200 flex-shrink-0 relative">
                <Button class="absolute top-0 right-0 m-2 text-red-500 cursor-pointer bg-gray-200 hover:bg-gray-300
                 dark:bg-gray-200 dark:hover:bg-gray-300"
                        on:click={() => { listToDelete = list.id; deleteListModal = true; }}>×
                </Button>
                <Button class="absolute top-0 right-12 m-2 text-red-500 cursor-pointer bg-gray-200 hover:bg-gray-300
                 dark:bg-gray-200 dark:hover:bg-gray-300"
                        on:click={() => { taskListId = list.id; addTaskModal = true; }}>+
                </Button>
                <Button class="text-lg text-gray-700 font-bold mb-2 cursor-pointer bg-gray-200 hover:bg-gray-300
                 dark:bg-gray-200 dark:hover:bg-gray-300"
                        on:click={() => { editingList = list; updatedListTitle = list.title; editListModal = true; }}>
                    {list.title}
                </Button>
                <div class="task-list"
                     use:dndzone={{items: list.items, flipDurationMs: 0}}
                     on:consider={event => handleDndEvent(event,list.id)}
                     on:finalize={event => handleDndEvent(event, list.id)}>
                    {#each list.items as task (task.id)}
                        <div class="task bg-gray-100 mb-2 p-2 rounded-md" data-id={task.id}>
                            <h3 class="text-md font-medium">{task.title}</h3>

                            <Button class="p-2 text-primary-400 cursor-pointer bg-gray-200 hover:bg-gray-300
                             dark:bg-gray-200 dark:hover:bg-gray-300"
                                    on:click={() => { taskListId = list.id; taskId = task.id;
                                        updatedTaskTitle = task.title; editTaskModal = true; }}>
                                Edit
                            </Button>
                            <Button class="p-2 text-red-500 cursor-pointer bg-gray-200 hover:bg-gray-300
                             dark:bg-gray-200 dark:hover:bg-gray-300"
                                    on:click={() => { taskId = task.id; deleteTaskModal = true; }}>×
                            </Button>

                        </div>
                    {/each}
                </div>
            </div>
        {/each}
    </div>
{/if}

<Modal autoclose={false} bind:open={deleteListModal} size="md">
    <form on:submit|preventDefault={deleteList}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Delete List</h3>
        <p class="mb-5 text-sm font-normal text-gray-500 dark:text-gray-400">Are you sure you want to delete this List?
            This
            action cannot be undone.</p>
        <div class="flex justify-end space-x-2">
            <Button on:click={() => deleteList(listToDelete)}>Delete</Button>
            <Button color="light" on:click={() => (deleteListModal = false)}>Cancel</Button>
        </div>
    </form>
</Modal>

<Modal autoclose={false} bind:open={deleteTaskModal} size="md">
    <form on:submit|preventDefault={deleteTask}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Delete Task</h3>
        <p class="mb-5 text-sm font-normal text-gray-500 dark:text-gray-400">Are you sure you want to delete this Task?
            This
            action cannot be undone.</p>
        <div class="flex justify-end space-x-2">
            <Button on:click={() => deleteTask(taskId)}>Delete</Button>
            <Button color="light" on:click={() => (deleteTaskModal = false)}>Cancel</Button>
        </div>
    </form>
</Modal>

<Modal autoclose={false} bind:open={addTaskModal} class="w-full" size="xs">
    <form class="flex flex-col space-y-6" on:submit={addTask}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Create a New Task</h3>
        <Label class="space-y-2">
            <span>Title</span>
            <Input bind:value={newTaskTitle} class="border" name="title" placeholder="Title" required type="text"/>
        </Label>
        <Button class="w-full" type="submit">Create</Button>
        <Button color="light" on:click={() => (addTaskModal = false)}>Cancel</Button>
    </form>
</Modal>


<Modal autoclose={false} bind:open={editListModal} size="md">
    <form class="flex flex-col space-y-6" on:submit|preventDefault={updateList}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Edit List</h3>
        <Label class="space-y-2">Title</Label>
        <Input bind:value={updatedListTitle} class="border" name="title" required type="text"/>
        <Button type="submit">Update</Button>
        <Button color="light" on:click={() => (editListModal = false)}>Cancel</Button>
    </form>
</Modal>

<Modal autoclose={false} bind:open={editTaskModal} class="w-full" size="xs">
    <form class="flex flex-col space-y-6" on:submit|preventDefault={updateTask}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Update Task</h3>
        <Label class="space-y-2">
            <span>Title</span>
            <Input bind:value={updatedTaskTitle} class="border" name="title" required type="text"/>
        </Label>
        <Button class="w-full" type="submit">Update</Button>
        <Button color="light" on:click={() => (editTaskModal = false)}>Cancel</Button>
    </form>
</Modal>

<style>
    .task-list {
        min-height: 100px;
    }

    .task {
        cursor: grab;
    }
</style>