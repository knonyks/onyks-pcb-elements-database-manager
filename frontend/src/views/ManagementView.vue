<script setup>
    import { ref } from 'vue';
    import { onMounted } from 'vue';
    import DataLoader from '@/components/DataLoader.vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import BasicButtonsPanel from '@/components/BasicButtonsPanel.vue';
    import { suppliers } from '@/utils/api';
    import { MyLoaderState, MyTime } from '@/utils/tools';
    import BasicTable from '@/components/BasicTable.vue';
    import { MyManagementTable } from '@/utils/tools';
    import BasicSearch from '@/components/BasicSearch.vue';

    const loading = ref(new MyLoaderState())

    const tablesManagement = ref(new MyManagementTable(suppliers.list, 
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
            "key": "name",
            "label": "Name"
        },
        {
            "key": "createdAt",
            "label": "Created At"
        },
    ], (e) => {e.selected = false; e.createdAt = MyTime.getLocalTime(e.createdAt, 'en'); return e}))

    const manufacturersManagement = ref(new MyManagementTable(suppliers.list, 
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
            "key": "name",
            "label": "Name"
        },
        {
            "key": "createdAt",
            "label": "Created At"
        },
    ], (e) => {e.selected = false; e.createdAt = MyTime.getLocalTime(e.createdAt, 'en'); return e}))

    const suppliersManagement = ref(new MyManagementTable(suppliers.list, 
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
            "key": "name",
            "label": "Name"
        },
        {
            "key": "createdAt",
            "label": "Created At"
        },
    ], (e) => {e.selected = false; e.createdAt = MyTime.getLocalTime(e.createdAt, 'en'); return e}))


    onMounted(async () =>
    {
        loading.value.state += 100/4
        await tablesManagement.value.init()
        
        loading.value.state += 100/4
        await manufacturersManagement.value.init()
        
        loading.value.state += 100/4
        await suppliersManagement.value.init()
        
        loading.value.state = 100
        loading.value.isLoading = false
    })
</script>

<template>
    <DataLoader :is-loading="loading.isLoading" :error="loading.error" :state="loading.state">
        <ManagerPage title="Management">

            <!-- #region Elements -->
            <onyks-header level=3>Elements</onyks-header>

            <BasicButtonsPanel>
                <onyks-button background="green">Add</onyks-button>
                <onyks-button background="blue">Edit</onyks-button>
                <onyks-button>Delete</onyks-button>
                <onyks-button background="yellow">Duplicate</onyks-button>
                <onyks-button background="grey">Datasheet</onyks-button>
                <onyks-button background="green">Labels</onyks-button>
                <onyks-button background="blue">Details</onyks-button>
                <onyks-button background="yellow" icon="F150">Extend</onyks-button>
            </BasicButtonsPanel>
            <!-- #endregion -->


            <!-- #region Tables -->
            <onyks-header level=3>Tables</onyks-header>

            <BasicButtonsPanel>
                <onyks-button background="green">Add</onyks-button>
                <onyks-button background="blue">Edit</onyks-button>
                <onyks-button>Delete</onyks-button>
            </BasicButtonsPanel>

            <!-- <BasicTable v-model="tablesManagement.model" @page-change="tablesManagement.nextPage($event.detail.index)"></BasicTable> -->
            <!-- #endregion -->


            <!-- #region Manufacturers -->
            <onyks-header level=3>Manufacturers</onyks-header>

            <BasicButtonsPanel>
                <onyks-button background="green">Add</onyks-button>
                <onyks-button background="blue">Edit</onyks-button>
                <onyks-button>Delete</onyks-button>
            </BasicButtonsPanel>
            <!-- #endregion -->
            <!-- <BasicTable v-model="manufacturersManagement.model" @page-change="manufacturersManagement.nextPage($event.detail.index)"></BasicTable> -->

            <!-- #region Suppliers -->
            <onyks-header level=3>Suppliers</onyks-header>
    
            <BasicButtonsPanel>
                <onyks-button background="green">Add</onyks-button>
                <onyks-button background="blue">Edit</onyks-button>
                <onyks-button>Delete</onyks-button>
            </BasicButtonsPanel>

            <BasicSearch v-model="suppliersManagement"></BasicSearch>
            <BasicTable v-model="suppliersManagement"></BasicTable>

            <!-- #endregion -->
        </ManagerPage>
    </DataLoader>
</template>

<style lang="css">
</style>