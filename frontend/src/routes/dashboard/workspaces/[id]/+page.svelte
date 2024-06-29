<script lang="ts">
    /** @type {import('./$types').PageServerData} */
    export let data;
    console.log(data);
</script>

<div class="container mx-auto p-8 bg-white dark:bg-gray-900 rounded-lg shadow-lg">
    <!-- Overall Wrapper -->
    <div class="p-6 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg shadow-lg">
        <!-- Title and Description -->
        <div class="mb-8 text-center">
            <h1 class="text-4xl font-extrabold text-white break-words">{data.workspace.title}</h1>
            <p class="text-xl text-white mt-4 break-words">{data.workspace.description}</p>
        </div>

        <!-- Workspace Owner -->
        <div class="mb-8 text-center">
            <h2 class="text-2xl font-bold text-white">Workspace Owner</h2>
            <p class="text-xl text-white mt-2 break-words">{data.workspace.owner.email}</p>
        </div>

        <!-- Members -->
        <div>
            <h2 class="text-3xl font-bold text-white mb-6 text-center">Members</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                {#each data.workspace.membership as membership}
                    <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg overflow-hidden">
                        <div class="text-center">
                            <h3 class="text-xl font-bold text-gray-900 dark:text-white break-words">{membership.member.email}</h3>
                            <p class="text-md text-gray-600 dark:text-gray-300 mt-2 break-words">{membership.member.mobile}</p>
                            <p class="text-md text-gray-600 dark:text-gray-300 mt-2 break-words">Access Level: {membership.access_level}</p>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>
