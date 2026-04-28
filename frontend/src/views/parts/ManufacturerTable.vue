<script setup lang="js">
    import BasicTable from '@/components/BasicTable.vue';
    import BasicTablePanel from '@/components/BasicTablePanel.vue';
    import DeleteDialog from '@/components/DeleteDialog.vue';
    import ManufactuterSupplierAddDialog from '@/components/ManufactuterSupplierAddDialog.vue';
    import PageContentElement from '@/components/PageContentElement.vue';
    import { api_manufacturer_list } from '@/utils/api';
    import { DateTime } from "luxon";
    import { ref } from 'vue';
    
    const add_dialog = ref(null)
    const delete_dialog = ref(null)
    const table = ref(null)

    const columns = [
        { key: 'selected', label: 'Select' },
        { key: 'id', label: 'ID' },
        { key: 'name', label: 'Name' },
        { key: 'created_at', label: 'Created' }
    ]

    const update = async (page = 1, limit = 50) =>
    {
        let result = await api_manufacturer_list(page, limit)
        result.data.data.map((x) =>
        {
            x.selected = false
            x.created_at = DateTime.fromISO(x.created_at, { zone: 'utc' }).setZone("Europe/Warsaw").toFormat("dd.MM.yyyy HH:mm");
        })
        return result
    }

    const edit_isDisabled = ref(true)
    const delete_isDisabled = ref(true)

    const checkbox_change = (data) => 
    {
        let x = data.filter(element => element.selected).length
        if(x == 1)
        {
            edit_isDisabled.value = false
            delete_isDisabled.value = false          
        }
        else if(x >= 1)
        {
            edit_isDisabled.value = true
            delete_isDisabled.value = false
        }
        else
        {
            edit_isDisabled.value = true
            delete_isDisabled.value = true
        }
    };
</script>

<template>
    <PageContentElement>
        <h1>Manufacturers</h1>
        <BasicTablePanel :maxWidth="550">
            <onyks-button background="green" @click="add_dialog.open(true)">Add</onyks-button>
            <onyks-button background="blue" :disabled="edit_isDisabled">Edit</onyks-button>
            <onyks-button background="red" @click="delete_dialog.open(true)" :disabled="delete_isDisabled">Delete</onyks-button>
        </BasicTablePanel>
        <BasicTable :columns="columns" :update="update" @checkbox-change="checkbox_change" ref="table"></BasicTable>
    </PageContentElement>
    <ManufactuterSupplierAddDialog title="manufacturer" ref="add_dialog" @close="table.reset()"></ManufactuterSupplierAddDialog>
    <DeleteDialog @close="table.reset()" ref="delete_dialog"></DeleteDialog>
</template>
