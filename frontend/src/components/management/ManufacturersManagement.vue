<script setup lang="js">
    import BasicTable from '../BasicTable.vue';
    import { onMounted, ref } from 'vue';
    import { reactive } from 'vue';
    import BasicButtonsPanel from '../BasicButtonsPanel.vue';
    import { element } from '@/utils/api.js';

    const table = ref(null)
    const columns = reactive(
    [
        {
            "key": "selected",
            "label": "Select"
        },
        {
            "key": "name",
            "label": "Name"
        },
        {
            "key": "numberOfItems",
            "label": "Number of items"
        },
        {
            "key": "createdAt",
            "label": "Created At"
        },
    ])

    onMounted(async () =>
    {
        table.value.init()
    })
</script>

<template>
    <onyks-container padding="0" gap="l">
        <onyks-header level="3">Manufacturers</onyks-header>
        <BasicButtonsPanel>
            <onyks-button background="green">Add</onyks-button>
            <onyks-button background="blue">Edit</onyks-button>
            <onyks-button  background="red">Delete</onyks-button>
        </BasicButtonsPanel>
        <BasicTable ref="table" :columns="columns" :data="data" :update="element.list" @checkbox-click="checkboxClick"></BasicTable>
    </onyks-container>
</template>

<style lang="css" scoped>
</style>