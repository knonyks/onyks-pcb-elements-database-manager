<script setup>
    import Nav from './Nav.vue';
</script>

<template>
    <Nav></Nav>
    <main>
        <router-view></router-view>
    </main>
</template>

<style scoped>
    main
    {
        min-height: calc(100vh - var(--spacing-md)*2);
        max-width: 1024px;
        margin-left: auto;
        margin-right: auto;
        padding: var(--spacing-md);
        margin-top: 72px;
    }
</style>