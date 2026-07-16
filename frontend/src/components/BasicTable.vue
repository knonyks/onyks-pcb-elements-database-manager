<script setup>
    import { dateUTCtoDestination } from '@/utils/tools';
    import { defineProps, ref } from 'vue';
    import { defineExpose } from 'vue';

    const props = defineProps(['columns', 'update']);
    const emit = defineEmits(['checkbox-click'])

    const table = ref(null)
    const data = ref([])
    const total = ref(0)
    const skip = ref(0)
    const limit = ref(50)
    const selected = ref(0)

    const pageChange = async (e) =>
    {
        skip.value = (e.detail.index  - 1)*limit.value
        let temp = await props.update(limit.value, skip.value)
        if(temp.status == 200)
        {
            temp.data.items.forEach(element => 
            {
                element.selected = false
                element.createdAt = dateUTCtoDestination(element.createdAt)
            });
            data.value = temp.data.items
        }
    }

    const init = async () =>
    {
        let temp = await props.update(limit.value, skip.total)
        if(temp.status == 200)
        {
            temp.data.items.forEach(element => 
            {
                element.selected = false
                element.createdAt = dateUTCtoDestination(element.createdAt)
            });
            data.value = temp.data.items
            total.value = temp.data.total
            skip.value = 0
        }
    }

    const getSelectedRows = () =>
    {
        return table.value.getSelectedRows()
    }

    defineExpose({init, getSelectedRows})
</script>

<template>
    <onyks-container gap="l" align="center" padding="">
        <onyks-table ref="table" .columns="columns" .data="data" @checkbox-click="(e) => {emit('checkbox-click', e); selected = table.getSelectedRows().length}"></onyks-table>
        <onyks-container type="group" align="center" justify="center" padding="" gap="l">
            <onyks-pagination-nav :max-index="Math.ceil(total / limit)" index="1" max-view="3" size="m" @page-change="pageChange"></onyks-pagination-nav>
            <onyks-text>Selected: {{selected}}&emsp;|&emsp;Total: {{ total }}</onyks-text>
        </onyks-container>
    </onyks-container>
</template>

<style lang="css" scoped>
    onyks-table
    {
        height: 400px;
    }

    onyks-container
    {
        width: 100%;
        white-space: nowrap
    }

    onyks-text
    {
        flex: 1;
        text-align: right;
    }
</style>