<script setup>
    import { defineModel } from 'vue';

    const model = defineModel()
</script>

<template>
    <onyks-textfield placeholder="Search a phrase..." v-model="model.search" @input="() => {model.searchPhrase()}"></onyks-textfield>
</template>

<style>
    onyks-textfield
    {
        width: 100%;
    }
</style>