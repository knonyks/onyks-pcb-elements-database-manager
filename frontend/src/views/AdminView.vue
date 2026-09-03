<script setup>
    import { ref } from 'vue';
    import { onMounted } from 'vue';
    import DataLoader from '@/components/DataLoader.vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import BasicButtonsPanel from '@/components/BasicButtonsPanel.vue';
    import { services } from '@/utils/api';
    import { MyLoaderState, MyTime } from '@/utils/tools';
    import BasicTable from '@/components/BasicTable.vue';
    import { MyTable } from '@/utils/tools';
    import BasicSearch from '@/components/BasicSearch.vue';

    const loading = ref(new MyLoaderState())
    const users = ref(new MyTable(services.users.list, 
    [
        {
            "key": "selected",
            "label": "Select"
        },
        {
            'key': 'id',
            'label': 'ID'
        },
        {
            "key": "login",
            "label": "Login"
        },
        {
            "key": "expirationTime",
            "label": "Expiration Time"
        },
    ], (e) => {e.selected = false; e.createdAt = MyTime.getLocalTime(e.expirationTime, 'en'); return e}))


    onMounted(async () =>
    {
        loading.value.state += 100/4
        await users.value.init()
        
        loading.value.state = 100
        loading.value.isLoading = false
    })
</script>

<template>
    <DataLoader v-model="loading">
        <ManagerPage title="Admin">

            <!-- #region Users -->
            <onyks-header level=3>Users</onyks-header>
            <BasicButtonsPanel>
                <onyks-button background="green">Add</onyks-button>
                <onyks-button background="blue">Edit</onyks-button>
                <onyks-button>Delete</onyks-button>
            </BasicButtonsPanel>
            <BasicSearch v-model="users"></BasicSearch>
            <BasicTable v-model="users"></BasicTable>
            <!-- #endregion -->
        </ManagerPage>
    </DataLoader>
</template>

<style lang="css">
</style>