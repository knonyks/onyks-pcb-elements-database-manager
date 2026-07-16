<script setup lang="js">
    import WarningAlert from '@/components/WarningAlert.vue';
    import RepositoryExplorer from '@/components/RepositoryExplorer.vue';
</script>

<template>
    <onyks-container type="stack" padding="l" gap="l">
        <onyks-header>Repository</onyks-header>
        <WarningAlert></WarningAlert>
        <RepositoryExplorer></RepositoryExplorer>
    </onyks-container>
</template>

<style lang="css" scoped>
    onyks-container :deep(onyks-file-explorer)
    {
        width: 100%;
        height: 300px;
    }
</style>