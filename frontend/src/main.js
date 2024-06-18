import App from './App.svelte';
import {Router} from 'svelte-routing';

const app = new App({
    target: document.body,
    props: {
        name: 'world'
    }
});

export default app;