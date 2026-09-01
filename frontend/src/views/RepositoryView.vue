<script setup lang="js">
    import RepositoryExplorer from '@/components/RepositoryExplorer.vue';
    import { onMounted, ref } from 'vue';
    import DataLoader from '@/components/DataLoader.vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import { Repository } from '@/utils/tools';
    
    const isLoading = ref(true)
    const error = ref(null)
    const repo = ref(new Repository((e) => e.type === 'dir' || e.type === 'schlib' || e.type === 'pcblib' || e.type === 'footprint' || e.type === 'symbol'))

    onMounted(async () =>
    {
        try 
        {
            await repo.value.init()
        } 
        catch (err) 
        {
            error.value = err.message
        }
        isLoading.value = false
    })
</script>

<template>
    <DataLoader :is-loading="isLoading" :error="error">
        <ManagerPage title="Repository">
            <RepositoryExplorer :explorerContent="repo.content" :path="repo.path"
            @enter-folder="(e) => repo.enterFolder(e)"
            @path-change="(e) => repo.pathChange(e)"
            @refresh="(e) => repo.refresh()"></RepositoryExplorer>
        </ManagerPage>
    </DataLoader>
</template>

<style lang="css" scoped>
    onyks-container :deep(onyks-file-explorer)
    {
        width: 100%;
        height: 300px;
    }
</style>