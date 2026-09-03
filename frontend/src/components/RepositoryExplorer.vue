<script setup lang="js">
    import { ref } from 'vue';
    import { defineModel } from 'vue';

    const model = defineModel()

    const types = ref([{type: 'file', icon: 'F390', isLikeDir: false}, 
    {type: 'dir', icon: 'F3D8', isLikeDir: true}, 
    {type: 'schlib', icon: 'F3D5', isLikeDir: true},
    {type: 'pcblib', icon: 'F3D5', isLikeDir: true},
    {type: 'footprint', icon: 'F6E7', isLikeDir: false}, 
    {type: 'symbol', icon: 'F6E2', isLikeDir: false}])
</script>

<template>
    <onyks-path @path-change="model.pathChange($event)" :content="model.path"></onyks-path>
    <onyks-file-explorer :types="types" @enter-folder="model.enterFolder($event)" :content="model.content"></onyks-file-explorer>
    <onyks-container type="group" padding="" justify="end">
        <onyks-button @click="model.refresh" background="green">Refresh</onyks-button>
    </onyks-container>
</template>

<style lang="css" scoped>
    onyks-file-explorer
    {
        width: 100%;
        height: 200px;
    }

    onyks-button
    {
        width: 120px;
    }
</style>