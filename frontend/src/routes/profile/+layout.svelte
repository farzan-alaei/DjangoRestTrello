<script>
    import {page} from '$app/stores';
    import {Sidebar, SidebarGroup, SidebarItem, SidebarWrapper} from 'flowbite-svelte';
    import {
        ChartPieSolid,
        GridSolid,
        ClipboardListSolid,
        UsersGroupSolid,
    } from 'flowbite-svelte-icons';

    $: activeUrl = $page.url.pathname;
</script>

<div class="flex flex-col md:flex-row min-h-screen dark:bg-gray-900">
    <Sidebar {activeUrl} class="w-full md:w-1/2 lg:w-1/5 h-full border-r dark:bg-gray-800 dark:border-gray-700">
        <SidebarWrapper class="h-full">
            <SidebarGroup class="space-y-5 m-8">
                <SidebarItem label="Dashboard" href="/profile">
                    <svelte:fragment slot="icon">
                        <ChartPieSolid class="w-6 h-6 text-primary-700 transition duration-75 dark:text-primary-700 group-hover:text-gray-900 dark:group-hover:text-white"/>
                    </svelte:fragment>
                </SidebarItem>
                <SidebarItem label="Workspaces" href="/profile/workspaces">
                    <svelte:fragment slot="icon">
                        <GridSolid class="w-6 h-6 text-primary-700 transition duration-75 dark:text-primary-700 group-hover:text-gray-900 dark:group-hover:text-white"/>
                    </svelte:fragment>
                </SidebarItem>
                <SidebarItem label="Boards" href="/profile/boards">
                    <svelte:fragment slot="icon">
                        <ClipboardListSolid class="w-6 h-6 text-primary-700 transition duration-75 dark:text-primary-700 group-hover:text-gray-900 dark:group-hover:text-white"/>
                    </svelte:fragment>
                </SidebarItem>
                <SidebarItem label="Members" href="/profile/members">
                    <svelte:fragment slot="icon">
                        <UsersGroupSolid class="w-6 h-6 text-primary-700 transition duration-75 dark:text-primary-700 group-hover:text-gray-900 dark:group-hover:text-white"/>
                    </svelte:fragment>
                </SidebarItem>
            </SidebarGroup>
        </SidebarWrapper>
    </Sidebar>

    <div class="flex-grow w-full md:w-3/4 lg:w-4/5 p-4">
        <slot />
    </div>
</div>
