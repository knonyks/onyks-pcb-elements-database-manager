<template>
    <onyks-container class="container" align="center">
        <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in" appear>
                <component :is="Component"/>
            </transition>
        </router-view>
    </onyks-container>
</template>

<style lang="css">
    html, body, #app 
    {
        height: 100%;
        margin: 0;
        padding: 0;
    }

    onyks-nav
    {
        position: sticky;
        top: 0;
        z-index: 101;
        width: 100%;
        flex-shrink: 0;
    }

    onyks-dialog
    {
        z-index: 12;
    }

    onyks-button
    {
        min-width: 120px;
    }

    .fade-enter-active, .fade-leave-active
    {
        transition: opacity 0.25s ease;
    }

    .fade-enter-from, .fade-leave-to
    {
        opacity: 0;
    }

    .fade-enter-to, .fade-leave-from
    {
        opacity: 1;
    }
</style>

<style lang="css" scoped>
    .container
    {
        width: 100%;
        height: 100%;
        overflow-y: scroll;
    }
</style>