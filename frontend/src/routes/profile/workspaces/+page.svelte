<script>
    /** @type {import('./$types').PageServerData} */
    export let data;
</script>

<main>
    <h1>Workspaces</h1>
    {#if data.workspaces.length > 0}
        <ul>
            {#each data.workspaces as workspace}
                <li>
                    <h2>{workspace.title}</h2>
                    <p><strong>Description:</strong> {workspace.description}</p>
                    <div class="workspace-owner">
                        <p><strong>Owner:</strong> {workspace.owner.email}</p>
                    </div>
                    <div class="workspace-membership">
                        <h3>Members</h3>

                        {#each workspace.membership as membership}
                            <div class="workspace-membership-nested">
                                <p><strong>Email:</strong> {membership.member.email}</p>
                                <p><strong>Mobile:</strong> {membership.member.mobile}</p>
                                <p><strong>Access Level:</strong> {membership.access_level}</p>
                            </div>
                        {/each}

                    </div>
                </li>
            {/each}
        </ul>
    {:else}
        <p>No workspaces available.</p>
    {/if}
</main>

