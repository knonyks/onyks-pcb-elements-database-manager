<script setup>
</script>

<template>
    <onyks-nav size="l">
        <onyks-logo></onyks-logo>
        <onyks-nav-content maxviewitems="5">
            <router-link to="/dashboard"><onyks-nav-option :selected="$route.path === '/dashboard'">Dashboard</onyks-nav-option></router-link>
            <router-link to="/management"><onyks-nav-option :selected="$route.path === '/management'">Management</onyks-nav-option></router-link>
            <router-link to="/repository"><onyks-nav-option :selected="$route.path === '/repository'">Repository</onyks-nav-option></router-link>
            <router-link to="/settings"><onyks-nav-option :selected="$route.path === '/settings'">Settings</onyks-nav-option></router-link>
            <router-link to="/admin"><onyks-nav-option :selected="$route.path === '/admin'">Admin</onyks-nav-option></router-link>
        </onyks-nav-content>
    </onyks-nav>
</template>

<style scoped>
    onyks-logo
    {
        position: absolute;
        height: 100%;
        width: auto;
        padding: var(--spacing-md);
        box-sizing: border-box;
    }

    a
    {
        color: inherit;
        text-decoration: none;
    }

    onyks-nav
    {
        position: fixed;
        top: 0;
        z-index: 100;
    }
</style>