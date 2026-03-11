<script setup>
    const props = defineProps({
        index: {
            type: Number,
            default: 0
        },
        max: {
            type: Number,
            default: 0
        }
        })
</script>

<template>
    <p>Displaying {{index}} of {{max}}.</p>
</template>

<style scoped>  
    p
    {
        font-size: 1.2rem;
        margin: 0;
        padding: 0;
    }
</style>