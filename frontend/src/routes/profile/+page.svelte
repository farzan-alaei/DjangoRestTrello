<script>
    import {page} from '$app/stores';
    import {Sidebar, SidebarGroup, SidebarItem, SidebarWrapper} from 'flowbite-svelte';
    import {
        ChartPieSolid,
        GridSolid,
        MailBoxSolid,
        UserSolid,
        ArrowRightToBracketOutline,
        EditOutline
    } from 'flowbite-svelte-icons';

    $: activeUrl = $page.url.pathname;
</script>

<Sidebar {activeUrl}>
    <SidebarWrapper class="h-96 border-r dark:bg-gray-800 dark:border-gray-700">
        <SidebarGroup class="space-x-5 mx-8 my-8">
            <SidebarItem label="Dashboard" href="/">
                <svelte:fragment slot="icon">
                    <ChartPieSolid
                            class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"/>
                </svelte:fragment>
            </SidebarItem>
            <SidebarItem label="Accordion" href="/docs/components/accordion">
                <svelte:fragment slot="icon">
                    <GridSolid
                            class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"/>
                </svelte:fragment>
            </SidebarItem>
            <SidebarItem label="Alert" href="/docs/components/alert">
                <svelte:fragment slot="icon">
                    <MailBoxSolid
                            class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"/>
                </svelte:fragment>
            </SidebarItem>
            <SidebarItem label="Sidebar" href="/docs/components/sidebar">
                <svelte:fragment slot="icon">
                    <UserSolid
                            class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"/>
                </svelte:fragment>
            </SidebarItem>
            <SidebarItem label="Badge" href="/docs/components/badge">
                <svelte:fragment slot="icon">
                    <ArrowRightToBracketOutline
                            class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"/>
                </svelte:fragment>
            </SidebarItem>
        </SidebarGroup>
    </SidebarWrapper>
</Sidebar>