<script setup lang="js">
    import BasicButtonsPanel from '@/components/BasicButtonsPanel.vue';
    import BasicTable from '@/components/BasicTable.vue';
    import WarningAlert from '@/components/WarningAlert.vue';
    import { element, manufacturer, supplier, table } from '@/utils/api';
    import DeleteItemDialog from '@/components/DeleteItemDialog.vue';
    import { LabelsDoc } from '@/utils/tools';
    import { onMounted, ref } from 'vue';
    import { useRouter } from 'vue-router';
    import AvailableSoonDialog from '@/components/AvailableSoonDialog.vue';
    import AddItemDialog from '@/components/management/AddItemDialog.vue';
    window.supplier = supplier
    const dialogs = ref({other: {}, table: {add: null}, manufacturer: {add: null}, supplier: {add: null}})
    const router = useRouter()
    const btns = ref({element:{}, table: {}, manufacturer: {}, supplier: {}}) 
    const columns = ref({
        element: [
        {
            "key": "selected",
            "label": "Select"
        },
        {
            "key": "uuid",
            "label": "UUID"
        },
        {
            "key": "partName",
            "label": "Part Name"
        },
        {
            "key": "manufacturer",
            "label": "Manufacturer"
        },
        {
            "key": "table",
            "label": "Table"
        },
        {
            "key": "description",
            "label": "Description"
        },
        {
            "key": "value",
            "label": "Value"
        },
        {
            "key": "availability",
            "label": "Availability"
        },
        {
            "key": "libraryReference",
            "label": "Library Reference"
        },
        {
            "key": "libraryPath",
            "label": "Library Path"
        },
        {
            "key": "footprintReferenceNo1",
            "label": "Footprint Reference No. 1"
        },
        {
            "key": "footprintPathNo1",
            "label": "Footprint Path No. 1"
        },
        {
            "key": "footprintReferenceNo2",
            "label": "Footprint Reference No. 2"
        },
        {
            "key": "footprintPathNo2",
            "label": "Footprint Path No. 2"
        },
        {
            "key": "footprintReferenceNo3",
            "label": "Footprint Reference No. 3"
        },
        {
            "key": "footprintPathNo3",
            "label": "Footprint Path No. 3"
        },
        ,
        {
            "key": "createdAt",
            "label": "Created At"
        },
    ],
    table: [
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
    ],
    manufacturer: [
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
    ],
    supplier: [
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
    ]
    })
    const tables = ref({
        element: null,
        table: null,
        supplier: null,
        manufacturer: null
    })

    onMounted(() => 
    {
        tables.value.element.init()
        tables.value.table.init()
        tables.value.manufacturer.init()
        tables.value.supplier.init()
    })
    
    const actions = ref({
        element: async (e) =>
        {
            switch(e)
            {
                case 'add':
                    router.push('/element/add')
                    break;
                case 'edit':
                    router.push(`/element/edit/${tables.value.element.getSelectedRows()[0].uuid}`)
                    break;
                case 'delete':
                    break;
                case 'duplicate':
                    router.push(`/element/duplicate/${tables.value.element.getSelectedRows()[0].uuid}`)
                    break;
                case 'datasheet':
                    dialogs.value.other.availableSoon.open()
                    break;
                case 'labels':
                    let data = tables.value.element.getSelectedRows()
                    let total = data.length
                
                    let doc = new LabelsDoc(total)
                    await doc.init()

                    for(let i=0; i<total; i++)
                    {
                        await doc.drawData(i, data[i])
                        await doc.drawQR(i, data[i].uuid)
                    }

                    await doc.drawBorders()
                    await doc.finish()
                    break;
                case 'details':
                    router.push(`/element/details/${tables.value.element.getSelectedRows()[0].uuid}`)
                    break;
            }
        }
    })

    const checkbox = ref(
    {
        element: (e) =>
        {
            let toDisable = []
            let toEnable = []
            switch(tables.value.element.getSelectedRows().length)
            {
                case 0:
                    toDisable = ['edit', 'delete', 'duplicate', 'labels', 'details', 'datasheet']
                    break;
                case 1:
                    toEnable = ['edit', 'delete', 'duplicate', 'labels', 'details', 'datasheet']
                    break;
                default:
                    toEnable = ['delete', 'labels']
                    toDisable = ['edit', 'duplicate', 'details', 'datasheet']
                    break;
            }
            toDisable.forEach((e) => 
            {
                btns.value.element[e].disabled = true
            })
            toEnable.forEach((e) =>
            {
                btns.value.element[e].disabled = false
            })
        },
        manufacturer: (e) =>
        {
            let toDisable = []
            let toEnable = []
            switch(tables.value.manufacturer.getSelectedRows().length)
            {
                case 1:
                    toEnable = ['edit', 'delete']
                    break;
                default:
                    toDisable = ['edit', 'delete']
                    break;
            }
            toDisable.forEach((e) => 
            {
                btns.value.manufacturer[e].disabled = true
            })
            toEnable.forEach((e) =>
            {
                btns.value.manufacturer[e].disabled = false
            })
        },
        table: (e) =>
        {
            let toDisable = []
            let toEnable = []
            switch(tables.value.table.getSelectedRows().length)
            {
                case 1:
                    toEnable = ['edit', 'delete']
                    break;
                default:
                    toDisable = ['edit', 'delete']
                    break;
            }
            toDisable.forEach((e) => 
            {
                btns.value.table[e].disabled = true
            })
            toEnable.forEach((e) =>
            {
                btns.value.table[e].disabled = false
            })
        },
        supplier: (e) =>
        {
            let toDisable = []
            let toEnable = []
            switch(tables.value.supplier.getSelectedRows().length)
            {
                case 1:
                    toEnable = ['edit', 'delete']
                    break;
                default:
                    toDisable = ['edit', 'delete']
                    break;
            }
            toDisable.forEach((e) => 
            {
                btns.value.supplier[e].disabled = true
            })
            toEnable.forEach((e) =>
            {
                btns.value.supplier[e].disabled = false
            })
        }
    })
</script>

<template>
    <onyks-container gap="l" padding="l">
        <onyks-header>Management</onyks-header>
        <WarningAlert></WarningAlert>
        <onyks-container padding="" gap="l">
            <onyks-header level="3">Elements</onyks-header>
            <BasicButtonsPanel>
                <onyks-button background="green" @click="() => actions?.element('add')">Add</onyks-button>
                <onyks-button @click="() => actions?.element('edit')" :ref="(el) => { if (el) btns.element.edit = el }" background="blue" disabled>Edit</onyks-button>
                <onyks-button @click="() => actions?.element('delete')" :ref="(el) => { if (el) btns.element.delete = el }" background="red" disabled>Delete</onyks-button>
                <onyks-button @click="() => actions?.element('duplicate')" :ref="(el) => { if (el) btns.element.duplicate = el }" background="yellow" disabled>Duplicate</onyks-button>
                <onyks-button @click="() => actions?.element('datasheet')" :ref="(el) => { if (el) btns.element.datasheet = el }" background="green" disabled>Datasheet</onyks-button>
                <onyks-button @click="() => actions?.element('labels')" :ref="(el) => { if (el) btns.element.labels = el }" background="red" disabled>Labels</onyks-button>
                <onyks-button @click="() => actions?.element('details')" :ref="(el) => { if (el) btns.element.details = el }" background="red" disabled>Details</onyks-button>
            </BasicButtonsPanel>
            <BasicTable :ref="(el) => { if (el) tables.element = el }" :columns="columns?.element" 
                :update="element.list" @checkbox-click="checkbox?.element"></BasicTable>
            
            <onyks-header level="3">Tables</onyks-header>
            <BasicButtonsPanel>
                <onyks-button background="green" @click="dialogs?.table?.add?.open">Add</onyks-button>
                <onyks-button @click="() => actions?.table('edit')" :ref="(el) => { if (el) btns.table.edit = el }" background="blue" disabled>Edit</onyks-button>
                <onyks-button @click="() => actions?.table('delete')" :ref="(el) => { if (el) btns.table.delete = el }" background="red" disabled>Delete</onyks-button>
            </BasicButtonsPanel>
            <BasicTable :ref="(el) => { if (el) tables.table = el }" :columns="columns?.table"
                 :update="table.list" @checkbox-click="checkbox?.table"></BasicTable>
            
            <onyks-header level="3">Manufacturers</onyks-header>
            <BasicButtonsPanel>
                <onyks-button background="green" @click="dialogs?.manufacturer?.add?.open">Add</onyks-button>
                <onyks-button @click="() => actions?.manufacturer('edit')" :ref="(el) => { if (el) btns.manufacturer.edit = el }" background="blue" disabled>Edit</onyks-button>
                <onyks-button @click="() => actions?.manufacturer('delete')" :ref="(el) => { if (el) btns.manufacturer.delete = el }" background="red" disabled>Delete</onyks-button>
            </BasicButtonsPanel>
            <BasicTable :ref="(el) => { if (el) tables.manufacturer = el }" :columns="columns?.manufacturer" 
                :update="manufacturer.list" @checkbox-click="checkbox?.manufacturer"></BasicTable>
            
            <onyks-header level="3">Suppliers</onyks-header>
            <BasicButtonsPanel>
                <onyks-button background="green" @click="dialogs?.supplier?.add?.open">Add</onyks-button>
                <onyks-button @click="() => actions?.supplier('edit')" :ref="(el) => { if (el) btns.supplier.edit = el }" background="blue" disabled>Edit</onyks-button>
                <onyks-button @click="() => actions?.supplier('delete')" :ref="(el) => { if (el) btns.supplier.delete = el }" background="red" disabled>Delete</onyks-button>
            </BasicButtonsPanel>
            <BasicTable :ref="(el) => { if (el) tables.supplier = el }" :columns="columns?.supplier" 
                :update="supplier.list" @checkbox-click="checkbox?.supplier"></BasicTable>
        </onyks-container>
    </onyks-container>

    <AvailableSoonDialog :ref="(el) => {if (el) dialogs.other.availableSoon = el}"></AvailableSoonDialog>

    <AddItemDialog subject="table" :action="table.create" @success="tables?.table?.init"
    :ref="(el) => { if (el) dialogs.table.add = el }"></AddItemDialog>

    <AddItemDialog subject="manufacturer" :action="manufacturer.create" @success="tables?.manufacturer?.init"
    :ref="(el) => { if (el) dialogs.manufacturer.add = el }"></AddItemDialog>

    <AddItemDialog subject="supplier" :action="supplier.create" @success="tables?.supplier?.init"
    :ref="(el) => { if (el) dialogs.supplier.add = el }"></AddItemDialog>
    

    <DeleteItemDialog>
        <template v-slot:footer>
            <onyks-alert type="warning">This operation deletes the table and its elements!</onyks-alert>
        </template>
    </DeleteItemDialog>
</template>

<style scoped>

</style>