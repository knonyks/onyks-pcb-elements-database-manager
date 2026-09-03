<script setup>
    import { ref } from 'vue';
    import { onMounted } from 'vue';
    import DataLoader from '@/components/DataLoader.vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import BasicButtonsPanel from '@/components/BasicButtonsPanel.vue';
    import { services } from '@/utils/api';
    import { MyLoaderState, MyTime, MyTable } from '@/utils/tools';
    import BasicTable from '@/components/BasicTable.vue';
    import BasicSearch from '@/components/BasicSearch.vue';
    import { watch } from 'vue';

    // OTHER
    const loading = ref(new MyLoaderState())
    



    // TABLES
    const elements = ref(new MyTable(services.suppliers.list, 
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

    const suppliers = ref(new MyTable(services.suppliers.list, 
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
    
    const manufacturers = ref(new MyTable(services.manufacturers.list, 
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
    
    const tables = ref(new MyTable(services.tables.list, 
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

    const handleElementsBtnsClick = (name) =>
    {
        switch(name)
        {
            case 'Add':
                break;
            case 'Edit':
                break;
            case 'Delete':
                break;
            case 'Duplicate':
                break;
            case 'Datasheet':
                break;
            case 'Labels':
                break;
            case 'Details':
                break;
            case 'extend':
                elements.value.extend = !elements.value.extend
                break;
        }
    }

    onMounted(async () =>
    {
        loading.value.state += 100/4
        await tables.value.init()
        
        loading.value.state += 100/4
        await manufacturers.value.init()
        
        loading.value.state += 100/4
        await suppliers.value.init()
        
        loading.value.state = 100
        loading.value.isLoading = false
    })
</script>

<template>
    <DataLoader v-model="loading">
        <ManagerPage title="Management">

            <!-- #region Elements -->
            <onyks-header level=3>Elements</onyks-header>
            <BasicButtonsPanel>
                <onyks-button background="green" @click="handleElementsBtnsClick">Add</onyks-button>
                <onyks-button background="blue" @click="handleElementsBtnsClick" :disabled="elements.selectedCount != 1">Edit</onyks-button>
                <onyks-button background="red" @click="handleElementsBtnsClick" :disabled="elements.selectedCount < 1">Delete</onyks-button>
                <onyks-button background="yellow" @click="handleElementsBtnsClick" :disabled="elements.selectedCount != 1">Duplicate</onyks-button>
                <onyks-button background="grey" @click="handleElementsBtnsClick" :disabled="elements.selectedCount != 1">Datasheet</onyks-button>
                <onyks-button background="green" @click="handleElementsBtnsClick" :disabled="elements.selectedCount < 1">Labels</onyks-button>
                <onyks-button background="blue" @click="handleElementsBtnsClick" :disabled="elements.selectedCount != 1">Details</onyks-button>
                <onyks-button background="yellow" icon="F150" @click="handleElementsBtnsClick('extend')">Extend</onyks-button>
            </BasicButtonsPanel>
            <BasicTable v-model="elements"></BasicTable>
            <!-- #endregion -->

            <!-- #region Maufacturers -->
            <onyks-header level=3>Tables</onyks-header>
            <BasicButtonsPanel>
                <onyks-button background="green">Add</onyks-button>
                <onyks-button background="blue" :disabled="tables.selectedCount != 1">Edit</onyks-button>
                <onyks-button :disabled="tables.selectedCount < 1">Delete</onyks-button>
            </BasicButtonsPanel>
            <BasicTable v-model="tables"></BasicTable>
            <!-- #endregion -->

            <!-- #region Maufacturers -->
            <onyks-header level=3>Maufacturers</onyks-header>
            <BasicButtonsPanel>
                <onyks-button background="green">Add</onyks-button>
                <onyks-button background="blue" :disabled="manufacturers.selectedCount != 1">Edit</onyks-button>
                <onyks-button :disabled="manufacturers.selectedCount < 1">Delete</onyks-button>
            </BasicButtonsPanel>
            <BasicTable v-model="manufacturers"></BasicTable>
            <!-- #endregion -->

            <!-- #region Suppliers -->
            <onyks-header level=3>Suppliers</onyks-header>
            <BasicButtonsPanel>
                <onyks-button background="green">Add</onyks-button>
                <onyks-button background="blue" :disabled="suppliers.selectedCount != 1">Edit</onyks-button>
                <onyks-button :disabled="suppliers.selectedCount < 1">Delete</onyks-button>
            </BasicButtonsPanel>
            <BasicTable v-model="suppliers"></BasicTable>
            <!-- #endregion -->
        </ManagerPage>
    </DataLoader>
</template>

<style lang="css">
</style>