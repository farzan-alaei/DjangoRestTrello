<script lang="ts">
    import {onMount} from 'svelte';
    import {goto} from '$app/navigation';
    import {Alert, Button, Input, Label, Modal, Select, Textarea} from 'flowbite-svelte';
    import {InfoCircleSolid} from "flowbite-svelte-icons";

    /** @type {import('./$types').PageServerData} */
    export let data;
    console.log(data);
    let editMode = false;
    let defaultModal = false;
    let board = data.board;
    let lists = data.lists;
    console.log(lists)
</script>

<div class="bg-gradient-to-r from-cyan-500 to-blue-500 p-6 rounded-lg shadow-lg">
    <h1 class="text-3xl font-bold text-white">{board.title}</h1>
    <p class="text-md text-white mt-4">{board.description}</p>


        <div class="mt-4 flex space-x-4">
            <Button class="flex" on:click={() => (editMode = true)}>Edit</Button>
            <Button color="red" class="flex" on:click={() => (defaultModal = true)}>Delete</Button>
        </div>

</div>

{#if editMode}
    <div class="mt-4 p-6 rounded-lg shadow-lg bg-white">
        <form >
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

{#if lists}
    {#each lists as list}
        <div class="mt-4 p-6 rounded-lg shadow-lg bg-white">
            <h1 class="text-3xl font-bold text-gray-700">{list.title}</h1>
            <p class="text-md text-gray-500 mt-4">{list.description}</p>
        </div>
    {/each}
{/if}