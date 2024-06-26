<script>
    import {page} from '$app/stores';
    import {Sidebar, SidebarGroup, SidebarItem, SidebarWrapper} from 'flowbite-svelte';
    import {
        ChartPieSolid,
        GridSolid,
        ClipboardListSolid,
        ArrowRightToBracketOutline,
        UsersGroupSolid,
    } from 'flowbite-svelte-icons';

    $: activeUrl = $page.url.pathname;
</script>

<Sidebar {activeUrl}>
    <SidebarWrapper class="h-96 border-r dark:bg-gray-800 dark:border-gray-700">
        <SidebarGroup class="space-x-5 m-8">
            <SidebarItem label="Dashboard" href="/">
                <svelte:fragment slot="icon">
                    <ChartPieSolid
                            class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"/>
                </svelte:fragment>
            </SidebarItem>
            <SidebarItem label="Workspaces" href="/docs/components/accordion">
                <svelte:fragment slot="icon">
                    <GridSolid
                            class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"/>
                </svelte:fragment>
            </SidebarItem>
            <SidebarItem label="Boards" href="/docs/components/alert">
                <svelte:fragment slot="icon">
                    <ClipboardListSolid
                            class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"/>
                </svelte:fragment>
            </SidebarItem>
            <SidebarItem label="members" href="/docs/components/sidebar">
                <svelte:fragment slot="icon">
                    <UsersGroupSolid
                            class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"/>
                </svelte:fragment>
            </SidebarItem>
        </SidebarGroup>
    </SidebarWrapper>
</Sidebar>