<script setup>
    import { RouterView, useRoute } from 'vue-router'
    const route = useRoute()
</script>

<template>
    <onyks-container align="center" class="manager-view">
        <onyks-nav class="manager-nav" size="m" mobile-breakpoint="900" max-view-items="5">
            <img src="../../node_modules/onyks-web-ui-system/dist/logo.png" class="logo">
            <router-link slot="nav" to="dashboard" .selected="route.path.endsWith('/dashboard')">Dashboard</router-link>
            <router-link slot="nav" to="management" .selected="route.path.endsWith('/management')">Management</router-link>
            <router-link slot="nav" to="repository" .selected="route.path.endsWith('/repository')">Repository</router-link>
            <router-link slot="nav" to="settings" .selected="route.path.endsWith('/settings')">Settings</router-link>
            <router-link slot="nav" to="admin" .selected="route.path.endsWith('/admin')">Admin</router-link>
        </onyks-nav>
        <onyks-container gap="" class="content">
            <router-view v-slot="{ Component }">
                <transition name="fade" mode="out-in">
                    <component :is="Component"/>
                </transition>
            </router-view>
        </onyks-container>
        <!-- <onyks-container class="footer"></onyks-container> -->
    </onyks-container>
</template>

<style lang="css" scoped>
    .manager-view
    {
        width: 100%;
        min-height: 90vh;
        flex-shrink: 0;
    }

    .logo
    {
        height: 100%;
        padding: var(--onyks-spacing-md);
        box-sizing: border-box;
        position: absolute;
    }

    .content
    {
        max-width: 1024px;
        height: 100%;
        width: 100%;
        flex: 1;
        box-sizing: border-box;
    }

    .footer
    {
        height: 300px;
        width: 100%;
        background-color: var(--onyks-surface-1);
        border: 1px solid var(--onyks-surface-1-border);
        border-width: 1px 0 0 0;
        flex-shrink: 0;
    }
</style>