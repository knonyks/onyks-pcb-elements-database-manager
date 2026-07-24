<script setup lang="js">
    import WarningAlert from '@/components/WarningAlert.vue';
    import BasicButtonsPanel from '@/components/BasicButtonsPanel.vue';
    import ElementForm from '@/components/ElementForm.vue';
    import { useRoute, useRouter } from 'vue-router';
    import { ref } from 'vue';
    import { Element } from '@/utils/db';
    import { element } from '@/utils/api';
    import { dateUTCtoDestination } from '@/utils/tools';
    import RepositoryModelSelector from '@/components/RepositoryModelSelector.vue';
    import AvailableSoonDialog from '@/components/AvailableSoonDialog.vue';

    const props = defineProps(['type'])
    const router = useRouter()
    const route = useRoute()
    const data = ref(new Element())
    const dialogs = ref({})
    import { LabelsDoc } from '@/utils/tools';

    const fillData = () =>
    {
        element.get(route.params.uuid).then((e) =>
        {
            if(e.status == 200)
            {
                e.data.createdAt = dateUTCtoDestination(e.data.createdAt)
                Object.assign(data.value, e.data);
            }
        })
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

    const label = async () =>
    {
        const doc = new LabelsDoc(1)
        await doc.init()

        await doc.drawData(0, data.value)
        await doc.drawQR(0, data.value.uuid)

        await doc.drawBorders()
        await doc.finish()
    }
</script>

<template>
    <onyks-container gap="l" padding="l">

        <onyks-header v-if="props.type == 'add'">Create an element</onyks-header>
        <onyks-header v-else-if="props.type == 'duplicate'">Duplicate an element</onyks-header>
        <onyks-header v-else-if="props.type == 'details'">Element's details</onyks-header>
        <onyks-header v-if="props.type == 'edit'">Edit an element</onyks-header>

        <WarningAlert></WarningAlert>

        <onyks-container align="start" padding="" gap="l">
            <onyks-button background="red" @click="router.back()">Return</onyks-button>
        </onyks-container>

        <ElementForm v-model="data" :type="props.type"></ElementForm>

        <onyks-container align="end" padding="" v-if="props.type == 'duplicate' || props.type == 'edit' || props.type == 'add'">
            <onyks-button v-if="props.type == 'add'" background="green">Create</onyks-button>
            <onyks-button v-else-if="props.type == 'edit'" background="blue">Edit</onyks-button>
            <onyks-button v-else-if="props.type == 'duplicate'" background="yellow">Duplicate</onyks-button>
        </onyks-container>

        <BasicButtonsPanel v-if="props.type == 'details'">
            <onyks-button background="blue" @click="() => {router.push(`/element/edit/${route.params.uuid}`)}">Edit</onyks-button>
            <onyks-button background="yellow" @click="() => {router.push(`/element/duplicate/${route.params.uuid}`)}">Duplicate</onyks-button>
            <onyks-button background="red" @click="() => {}">Delete</onyks-button>
            <onyks-button background="green" @click="dialogs?.availableSoon.open">Datasheet</onyks-button>
            <onyks-button background="blue" @click="label">Label</onyks-button>
        </BasicButtonsPanel>

    </onyks-container>
    <AvailableSoonDialog :ref="(el) => {if(el) dialogs.availableSoon = el}"></AvailableSoonDialog>
    
</template>

<style>
    onyks-button
    {
        width: 120px;
    }
</style>