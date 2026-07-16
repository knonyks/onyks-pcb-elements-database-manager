<script setup lang="js">
    import BasicTable from '../BasicTable.vue';
    import { onMounted, ref } from 'vue';
    import { reactive } from 'vue';
    import BasicButtonsPanel from '../BasicButtonsPanel.vue';
    import { useRouter } from 'vue-router';
    import { element } from '@/utils/api.js';
    import { LabelsDoc } from '@/utils/tools.js';
    import DeleteDialog from '../DeleteDialog.vue';
    import AvailableSoonDialog from '../AvailableSoonDialog.vue';

    const router = useRouter()
    const table = ref(null)
    const columns = reactive(
    [
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
    ])

    const editBtn = ref(null)
    const deleteBtn = ref(null)
    const duplicateBtn = ref(null)
    const datasheetBtn = ref(null)
    const labelsBtn = ref(null)
    const detailsBtn = ref(null)
    const deleteDialog = ref(null)
    const deleteItems = ref([])
    const availableSoonDialog = ref(null)

    onMounted(async () =>
    {
        table.value.init()
    })

    const checkboxClick = (e) =>
    {
        switch(table.value.getSelectedRows().length)
        {
            case 0:
                editBtn.value.disabled = true
                deleteBtn.value.disabled = true
                duplicateBtn.value.disabled = true
                datasheetBtn.value.disabled = true
                detailsBtn.value.disabled = true
                labelsBtn.value.disabled = true
                break;
            case 1:
                editBtn.value.disabled = false
                deleteBtn.value.disabled = false
                duplicateBtn.value.disabled = false
                datasheetBtn.value.disabled = false
                labelsBtn.value.disabled = false
                detailsBtn.value.disabled = false
                break;
            default:
                editBtn.value.disabled = true
                deleteBtn.value.disabled = false
                duplicateBtn.value.disabled = true
                datasheetBtn.value.disabled = true
                labelsBtn.value.disabled = false
                detailsBtn.value.disabled = true
                break;
        }
    }

    const labelsClick = async (e) =>
    {
        let data = table.value.getSelectedRows()
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
    }

    const deleteClick = () =>
    {
        deleteItems.value = table.value.getSelectedRows()
        deleteDialog.value.open()
    }
</script>

<template>
    <onyks-container padding="0" gap="l">
        <onyks-header level="3">Elements</onyks-header>
        <BasicButtonsPanel>
            <onyks-button background="green" @click="router.push('/element/add')">Add</onyks-button>
            <onyks-button ref="editBtn" background="blue" @click="router.push(`/element/edit/${table.getSelectedRows()[0].uuid}`)" disabled>Edit</onyks-button>
            <onyks-button ref="deleteBtn" background="red" @click="deleteClick" disabled>Delete</onyks-button>
            <onyks-button ref="duplicateBtn" background="yellow" @click="router.push(`/element/duplicate/${table.getSelectedRows()[0].uuid}`)" disabled>Duplicate</onyks-button>
            <onyks-button ref="datasheetBtn" background="green" @click="availableSoonDialog.open()" disabled>Datasheet</onyks-button>
            <onyks-button ref="labelsBtn" background="red" @click="labelsClick" disabled>Labels</onyks-button>
            <onyks-button ref="detailsBtn" background="red" @click="router.push(`/element/details/${table.getSelectedRows()[0].uuid}`)" disabled>Details</onyks-button>
        </BasicButtonsPanel>
        <BasicTable ref="table" :columns="columns" :data="data" :update="element.list" @checkbox-click="checkboxClick"></BasicTable>
    </onyks-container>

    <DeleteDialog @delete-end="table.init()" ref="deleteDialog" :interface="{name: 'partName', id: 'uuid'}" :items="deleteItems"></DeleteDialog>
    <AvailableSoonDialog ref="availableSoonDialog"></AvailableSoonDialog>
</template>

<style lang="css" scoped>

</style>