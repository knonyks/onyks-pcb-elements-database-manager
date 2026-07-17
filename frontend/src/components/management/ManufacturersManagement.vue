<script setup lang="js">
    import BasicTable from '../BasicTable.vue';
    import { onMounted, ref } from 'vue';
    import { reactive } from 'vue';
    import BasicButtonsPanel from '../BasicButtonsPanel.vue';
    import { manufacturer } from '@/utils/api.js';
    import AddItemDialog from './AddItemDialog.vue';
    import DeleteDialog from '../DeleteDialog.vue';

    const table = ref(null)
    const columns = reactive(
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
    ])

    const dialogs = ref({add: null, edit: null, delete: null})

    const add = async (e) =>
    {
        let data = await manufacturer.create({name: e})
        if(data.status == 200)
        {
            dialogs.value.add.close()
        }
        else
        {
            dialogs.value.add.errorDetails = data.response.data.detail
        }
        table.value.init()
    }

    onMounted(async () =>
    {
        table.value.init()

        await manufacturer.edit(14, {name: 'zbyszek'})
    })
</script>

<template>
    <onyks-container padding="0" gap="l">
        <onyks-header level="3">Manufacturers</onyks-header>
        <BasicButtonsPanel>
            <onyks-button background="green" @click="dialogs.add.open()">Add</onyks-button>
            <onyks-button background="blue">Edit</onyks-button>
            <onyks-button  background="red" @click="dialogs.delete.items = table.getSelectedRows(); dialogs.delete.open()">Delete</onyks-button>
        </BasicButtonsPanel>
        <BasicTable ref="table" :columns="columns" :data="data" :update="manufacturer.list" @checkbox-click="checkboxClick"></BasicTable>
    </onyks-container>

    <AddItemDialog subject="manufacturer" :ref="(el) => { if (el) dialogs.add = el }" @accept-click="add"></AddItemDialog>



    <DeleteDialog :action="manufacturer.delete" @delete-end="table.init();" :ref="(el) => { if (el) dialogs.delete = el }" :interface="{name: 'name', id: 'id'}"></DeleteDialog>

</template>

<style lang="css" scoped>
</style>