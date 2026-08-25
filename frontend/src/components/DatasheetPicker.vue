<script setup>
    import { ref } from 'vue';
    import { defineExpose } from 'vue';
    import { defineEmits } from 'vue';

    const props = defineProps(['type', 'datasheet'])
    const uploader = ref(null)
    const file = ref(null)
    const emit = defineEmits(['change'])

    defineExpose({file})
</script>

<template>
    <onyks-file-upload ref="uploader" accept=".pdf" message="Drag a file or click to add it" @change="emit('change', uploader.files[0])"></onyks-file-upload>
    <onyks-container type="group">
        <onyks-button @click="uploader.reset">Reset</onyks-button>
    </onyks-container>
</template>

<style scoped>
    onyks-file-upload
    {
        width: 100%;
    }
</style>