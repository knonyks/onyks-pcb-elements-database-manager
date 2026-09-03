<script setup lang="js">
    import RepositoryExplorer from '@/components/RepositoryExplorer.vue';
    import { onMounted, ref } from 'vue';
    import DataLoader from '@/components/DataLoader.vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import { MyLoaderState, MyRepository } from '@/utils/tools';
    import { MyError } from '@/utils/tools';
    
    const loading = ref(new MyLoaderState())
    const repo = ref(new MyRepository((e) => e.type === 'dir' || e.type === 'schlib' || e.type === 'pcblib' || e.type === 'footprint' || e.type === 'symbol'))

    onMounted(async () =>
    {
        try 
        {
            loading.value.state += 50
            await repo.value.init()
            loading.value.state = 100
            loading.value.isLoading = false
        } 
        catch (err) 
        {
            loading.value.error = MyError.process(err)
            loading.value.isLoading = false
        }
    })
</script>

<template>
    <DataLoader :is-loading="loading.isLoading" :error="loading.error" :state="loading.state">
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