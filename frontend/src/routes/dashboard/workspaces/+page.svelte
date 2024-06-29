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
