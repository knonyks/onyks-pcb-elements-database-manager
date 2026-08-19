<script setup lang="js">
    import WarningAlert from '@/components/WarningAlert.vue';
    import ElementForm from '@/components/ElementForm.vue';
    import { ElementModel } from '@/utils/db';
    import { ref } from 'vue';
    import { element } from '@/utils/api';
    import { useRouter } from 'vue-router';
    import { useRoute } from 'vue-router';
    import { dateUTCtoDestination } from '@/utils/tools';

    const props = defineProps(['type'])
    const model = ref(new ElementModel())
    const dialogs = ref({create: null, error: null})
    const router = useRouter()
    const route = useRoute()

    const fillData = () =>
    {
        element.get(route.params.uuid).then((e) =>
        {
            if(e.status == 200)
            {
                e.data.createdAt = dateUTCtoDestination(e.data.createdAt)
                Object.assign(model.value, e.data);
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

    const action = async (mode) =>
    {
        switch(mode)
        {
            case 'create':
                dialogs.value.create.open = true
                let data = await element.create(model.value)
                if(data.status == 200)
                {
                    setTimeout(() => 
                    {
                        dialogs.value.create.open = false
                        router.push(`/element/details/${data.data.uuid}`)
                    }, 1000)
                }
                else
                {
                    setTimeout(() => 
                    {
                        dialogs.value.create.open = false
                        dialogs.value.error.open = true
                    }, 1000)
                }
                break;
        }
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

        <ElementForm v-model="model" :type="props.type"></ElementForm>
       
        <onyks-container align="end" padding="" gap="l">
            <onyks-button background="green" @click="() => {action('create')}">Create</onyks-button>
        </onyks-container>

        <onyks-dialog modal no-title :ref="(el) => { dialogs.create = el }">
            <onyks-text>Creating the element...</onyks-text>
        </onyks-dialog>

        <onyks-dialog :title="`Error`" modal corner-close :ref="(el) => { if (el && dialogs) dialogs.error = el }">
            <onyks-text>Cannot create an element.</onyks-text>
        </onyks-dialog>

    </onyks-container>

</template>

<style>

</style>