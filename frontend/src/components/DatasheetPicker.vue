<script setup>
    import { ref } from 'vue';
    const uploader = ref(null)

    const dane = ref(null)
    const reset = () => 
    {
        console.dir(uploader.value.files)
    }
</script>

<template>
    <onyks-container align="start" padding="" type="stack" gap="l">
        <onyks-file-upload multiple accept=".pdf" ref="uploader"></onyks-file-upload>
        <onyks-button @click="reset">Reset</onyks-button>
    </onyks-container>
</template>

<style>
    onyks-file-upload
    {
        width: 100%;
    }

</style>