import Home from "./pages/Home.svelte";
import Login from "./pages/Login.svelte";
import Register from "./pages/Register.svelte";
import Profile from "./pages/Profile.svelte";


const routes = {
    '/': Home,
    '/login': Login,
    '/register': Register,
    '/profile': Profile,
}

export default routes;