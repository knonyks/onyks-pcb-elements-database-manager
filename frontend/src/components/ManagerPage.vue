<script setup>
    import WarningAlert from './WarningAlert.vue';
    const props = defineProps(['title'])
</script>

<template>
    <onyks-container gap="m">
        <onyks-container class="header" padding="l">
            <onyks-header>{{ props.title }}</onyks-header>
        </onyks-container>
        <WarningAlert></WarningAlert>
        <slot></slot>
    </onyks-container>
</template>

<style scoped>
    .header
    {
        padding-left: 0 !important;
    }
</style>