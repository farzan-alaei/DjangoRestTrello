<script lang="ts">
    /** @type {import('./$types').PageServerData} */
    export let data;
</script>


<div class="mt-12">
    <h1 class="text-3xl text-center font-bold dark:text-white">My Workspaces</h1>
</div>
<div class="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-2">
    {#if data.workspaces.length > 0}
        {#each data.workspaces as workspace}
            <div class="p-6 bg-primary-300 dark:bg-gray-800 rounded-lg shadow-md">
                <h3 class="text-2xl font-bold leading-tight text-gray-900 dark:text-white">
                    <a href="/profile/workspaces/{workspace.id}">{workspace.title}</a>
                </h3>
                <div class="mt-2 flex items-center border-t border-primary-700 pt-3 dark:bg-gray-800">
                    <p class="text-lg font-normal text-gray-500 dark:text-gray-300">
                        {workspace.description}
                    </p>
                </div>
            </div>
        {/each}

    {:else}
        <p class="text-gray-500">No workspaces available.</p>
    {/if}
</div>
