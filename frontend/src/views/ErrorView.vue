<script setup lang="js">
    import { useRoute } from 'vue-router'
    import Logos from '@/components/Logos.vue';

    const route = useRoute()
    console.log(route.params.message)
</script>

<template>
    <onyks-container type="stack" padding="m" gap="l" align="center" :class="$style.container" justify="center">
        <Logos></Logos>
        <onyks-header>ERROR! {{route.params.message != undefined? route.params.message.toUpperCase():'SOMETHING WENT WRONG!'}}</onyks-header>
        <router-link :to="{ path: '/manager/dashboard' }">
            <onyks-button>Return</onyks-button>
        </router-link>
    </onyks-container>
</template>

<style lang="css" module>
    .container
    {
        width: 100%;
        max-width: 800px;
        height: 100%;
        box-sizing: border-box;
    }
</style>