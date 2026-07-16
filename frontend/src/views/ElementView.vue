<script setup lang="js">
    import ElementForm from '@/components/ElementForm.vue';
    import WarningAlert from '@/components/WarningAlert.vue';
    import { ref } from 'vue';
    import { element } from '@/utils/api';
    import { defineProps, onMounted } from 'vue';
    import { Element } from '@/utils/db';
    import { dateUTCtoDestination } from '@/utils/tools';
    import { useRoute } from 'vue-router';
    import BasicButtonsPanel from '@/components/BasicButtonsPanel.vue';
    import { useRouter } from 'vue-router';
    import { LabelsDoc } from '@/utils/tools';
    import DeleteDialog from '@/components/DeleteDialog.vue';

    const router =  useRouter()
    const route = useRoute()
    // const form = ref(null)

    // const actionBtn = ref(null)
    // const actionStatusDialog = ref(null)
    // const errorDialog = ref(null)   
    // const errorDialogDetails = ref('')
    
    // const actionFunction = async () =>
    // {
    //     let data = structuredClone(form.value.getData())
    //     actionBtn.value.disabled = true
    //     actionStatusDialog.value.open = true

    //     let result = await element.create(data)
    //     if(result.status == 200)
    //     {
    //         setTimeout(() => 
    //         {
    //             actionStatusDialog.value.open = false
    //             router.push(`/element/details/${result.data.uuid}`)
    //         }, 1000)
    //     }
    //     else
    //     {
    //         setTimeout(() => 
    //         {
    //             actionStatusDialog.value.open = false
    //             errorDialog.value.open = true
    //             console.dir(result)
    //             errorDialogDetails.value = result.code
    //             actionBtn.value.disabled = false
    //         }, 1000)
    //     }
    // }

    const props = defineProps(['type'])
    const elementData = ref(new Element())
    const processingDialog = ref(null)
    const errorDialog = ref(null)
    const deleteDialog = ref(null)
    
    const fillData = () =>
    {
        element.get(route.params.uuid).then((e) =>
        {
            if(e.status == 200)
            {
                e.data.createdAt = dateUTCtoDestination(e.data.createdAt)
                Object.assign(elementData.value, e.data);
            }
        })
    }

    const addAction = async () =>
    {
        processingDialog.value.open = true
        let result = await element.create(elementData.value)
        if(result.status == 200)
        {
            setTimeout(() => 
            {
                processingDialog.value.open = true
                router.push(`/element/details/${result.data.uuid}`)
            }, 1000)
        }
        else
        {
            setTimeout(() => 
            {
                processingDialog.value.open = false
                errorDialog.value.open = true
            }, 1000)
        }
    }

    const editAction = async () =>
    {
        processingDialog.value.open = true
        let result = await element.edit(elementData.value.uuid, elementData.value)
        if(result.status == 200)
        {
            setTimeout(() => 
            {
                processingDialog.value.open = true
                router.push(`/element/details/${result.data.uuid}`)
            }, 1000)
        }
        else
        {
            setTimeout(() => 
            {
                processingDialog.value.open = false
                errorDialog.value.open = true
            }, 1000)
        }
    }

    const duplicateAction = async () =>
    {
        processingDialog.value.open = true
        let result = await element.create(elementData.value)
        if(result.status == 200)
        {
            setTimeout(() => 
            {
                processingDialog.value.open = false
                router.push(`/element/details/${result.data.uuid}`)
            }, 1000)
        }
        else
        {
            setTimeout(() => 
            {
                processingDialog.value.open = false
                errorDialog.value.open = true
            }, 1000)
        }
    }

    const labelsAction = async () =>
    {
        const doc = new LabelsDoc(1)
        await doc.init()

        await doc.drawData(0, elementData.value)
        await doc.drawQR(0, elementData.value.uuid)

        await doc.drawBorders()
        await doc.finish()
    }

    const deleteAction = async () =>
    {
        deleteDialog.value.open()
    }

    switch(props.type)
    {
        case 'add':
            break;
        case 'details':
            fillData()
            break;
        case 'edit':
            fillData()
            break;
        case 'duplicate':
            fillData()
            break;
    }
</script>

<template>
    <onyks-container gap="l" padding="l">

        <onyks-header v-if="props.type == 'add'">Add an element</onyks-header>
        <onyks-header v-else-if="props.type == 'duplicate'">Duplicate an element</onyks-header>
        <onyks-header v-else-if="props.type == 'details'">Element's details</onyks-header>
        <onyks-header v-if="props.type == 'edit'">Edit an element</onyks-header>

        <WarningAlert></WarningAlert>

        <onyks-container align="start" padding="" gap="l">
            <onyks-button background="red" @click="router.back()">Return</onyks-button>
        </onyks-container>

        <ElementForm ref="form" v-model="elementData" :type="props.type"></ElementForm>
        
        <onyks-container align="end" padding="" v-if="props.type == 'duplicate' || props.type == 'edit' || props.type == 'add'">
            <onyks-button v-if="props.type == 'add'" background="green" @click="addAction">Add</onyks-button>
            <onyks-button v-else-if="props.type == 'edit'" background="blue" @click="editAction">Edit</onyks-button>
            <onyks-button v-else-if="props.type == 'duplicate'" background="yellow" @click="duplicateAction">Duplicate</onyks-button>
        </onyks-container>

        <BasicButtonsPanel v-if="props.type == 'details'">
            <onyks-button background="blue" @click="router.push(`/element/edit/${route.params.uuid}`)">Edit</onyks-button>
            <onyks-button background="yellow" @click="router.push(`/element/duplicate/${route.params.uuid}`)">Duplicate</onyks-button>
            <onyks-button background="red" @click="deleteAction">Delete</onyks-button>
            <onyks-button background="green">Datasheet</onyks-button>
            <onyks-button background="blue" @click="labelsAction">Label</onyks-button>
        </BasicButtonsPanel>

    </onyks-container>

    <onyks-dialog no-title scroll-target="body" modal ref="processingDialog">
        <onyks-text v-if="props.type == 'add'" size="m">Creating the element...</onyks-text>
        <onyks-text v-else-if="props.type == 'duplicate'" size="m">Duplicating the element...</onyks-text>
        <onyks-text v-else-if="props.type == 'edit'" size="m">Editing the element...</onyks-text>
    </onyks-dialog>  
    
    <onyks-dialog title="Error!" scroll-target="body" corner-close modal ref="errorDialog">
        <onyks-container padding="" gap="l">
            <onyks-text size="m" v-if="props.type == 'add'">There was an error during adding the element!</onyks-text>
            <onyks-text size="m" v-else-if="props.type == 'duplicate'">There was an error during duplicating the element!</onyks-text>
            <onyks-text size="m" v-else-if="props.type == 'edit'">There was an error during editing the element!</onyks-text>
        </onyks-container>
    </onyks-dialog>

    <DeleteDialog @delete-end="router.push('/management')" ref="deleteDialog" v-if="props.type == 'details'" :items="[elementData]" :interface="{name: 'partName', id: 'uuid'}"></DeleteDialog>

</template>

<style>
    onyks-button
    {
        width: 120px;
    }
</style>