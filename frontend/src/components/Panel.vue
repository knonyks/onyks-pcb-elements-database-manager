<script setup>
    import Nav from './Nav.vue';
    import Footer from './Footer.vue'
</script>

<template>
    <Nav></Nav>
    <main>
        <router-view v-slot="{ Component, route }">
            <transition name="fade" mode="out-in">
                <div :key="route.path">
                    <component :is="Component" />
                </div>
            </transition>
        </router-view>
    </main>
    <Footer></Footer>
</template>

<style scoped>
    main
    {
        min-height: calc(100vh - var(--spacing-md)*2);
        max-width: 1024px;
        margin-left: auto;
        margin-right: auto;
        padding: 0 var(--spacing-md);
        margin-top: 71px;
    }
</style>

<style>
    .fade-enter-active, .fade-leave-active 
    {
        transition: opacity 0.2s ease;
    }

    .fade-enter-from, .fade-leave-to 
    {
        opacity: 0;
    }
</style>