<script>
    /** @type {import('./$types').PageServerData} */
    export let data;
</script>

<style>
    main {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        font-family: Arial, sans-serif;
    }

    h1 {
        text-align: center;
        color: #333;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        background: #f9f9f9;
        margin-bottom: 1rem;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    li h2 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
        color: #555;
    }

    li p {
        margin: 0.2rem 0;
        font-size: 0.9rem;
        color: #666;
    }

    .workspace-owner,
    .workspace-membership {
        margin-top: 0.5rem;
        padding: 0.5rem;
        background: #eee;
        border-radius: 4px;
    }

    .workspace-membership-nested {
        margin-top: 0.3rem;
        padding: 0.2rem;
        background: #f8f8f8;
        border-radius: 4px;
    }

    .workspace-membership h3 {
        margin: 0;
        font-size: 1rem;
        color: #444;
    }

    .workspace-membership p {
        margin: 0.2rem 0;
        font-size: 0.85rem;
        color: #666;
    }
</style>

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
