<script>
    import Header from '$lib/Header.svelte';
    import Footer from '$lib/Footer.svelte';
</script>

<Header/>

<slot/>

<Footer/>

<style>
    main {
        min-height: calc(100vh - 100px); /* Adjust according to your header and footer height */
        padding: 2rem;
    }
</style>
