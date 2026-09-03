<script setup lang="js">
    import RepositoryExplorer from '@/components/RepositoryExplorer.vue';
    import { onMounted, ref } from 'vue';
    import DataLoader from '@/components/DataLoader.vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import { MyLoaderState, MyRepository } from '@/utils/tools';
    import { MyError } from '@/utils/tools';
    
    const loading = ref(new MyLoaderState())
    const repository = ref(new MyRepository((e) => e.type === 'dir' || e.type === 'schlib' || e.type === 'pcblib' || e.type === 'footprint' || e.type === 'symbol'))

    onMounted(async () =>
    {
        try 
        {
            loading.value.state += 50
            await repository.value.init()
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
    <DataLoader v-model="loading">
        <ManagerPage title="Repository">
            <RepositoryExplorer v-model="repository"></RepositoryExplorer>
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