<script setup lang="js">
    import { ref } from 'vue';
    
    const props = defineProps(['explorer-content', 'path'])
    const emit = defineEmits(['path-change', 'refresh', 'enter-folder'])

    const types = ref([{type: 'file', icon: 'F390', isLikeDir: false}, 
    {type: 'dir', icon: 'F3D8', isLikeDir: true}, 
    {type: 'schlib', icon: 'F3D5', isLikeDir: true},
    {type: 'pcblib', icon: 'F3D5', isLikeDir: true},
    {type: 'footprint', icon: 'F6E7', isLikeDir: false}, 
    {type: 'symbol', icon: 'F6E2', isLikeDir: false}])
</script>

<template>
    <onyks-path @path-change="(e) => emit('path-change', e)" :content="props.path"></onyks-path>
    <onyks-file-explorer :types="types" @enter-folder="(e) => emit('enter-folder', e)" :content="props.explorerContent"></onyks-file-explorer>
    <onyks-container type="group" padding="" justify="end">
        <onyks-button @click="emit('refresh')" background="green">Refresh</onyks-button>
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