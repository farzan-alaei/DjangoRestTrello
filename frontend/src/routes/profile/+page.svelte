<script>
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    let profile = {};

    onMount(async () => {
        profile = await api('profile/');
    });
</script>

<h1>Profile Page</h1>
<p>Email: {profile.email}</p>
