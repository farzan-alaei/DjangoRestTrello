<script>
    import {Router, Link, Route} from "svelte-routing";
    import Home from "./pages/Home.svelte";
    import Login from "./pages/Login.svelte";
    import Register from "./pages/Register.svelte";
    import Profile from "./pages/Profile.svelte";
    import Routes from "./routes.js";

    export let name;
</script>


<Router>
    <nav>
        <Link to="/">Home</Link>
        <Link to="/login">Login</Link>
        <Link to="/register">Register</Link>
        <Link to="/profile">Profile</Link>
    </nav>
    <Route path="/" component="{Home}"/>
    <Route path="/login" component="{Login}"/>
    <Route path="/register" component="{Register}"/>
    <Route path="/profile" component="{Profile}"/>
</Router>



<style>
    nav {
        display: flex;
        gap: 10px;
    }
</style>