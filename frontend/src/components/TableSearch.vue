<script setup>
    import { ref } from 'vue'   
    const props = defineProps(
    {
        placeholder: 
        {
            type: String,
            default: 'aa'
        }
    })
</script>

<template>
    <onyks-textfield :placeholder="placeholder" type="text" size="l"></onyks-textfield>
</template>

<style scoped>  
    onyks-textfield
    {
        width: 100%;
    }
</style>