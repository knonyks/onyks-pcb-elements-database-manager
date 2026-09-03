<script setup>
    import { defineEmits } from 'vue';
    import BasicSearch from './BasicSearch.vue';

    const emit = defineEmits(['page-change', 'checkbox-click'])
    const model = defineModel();

    const handleCheckboxClick = (e) =>
    {
        if(e.detail.type == 'row')
        {
            model.value.data[e.detail.rowIndex].selected = e.detail.checked
        }
        else
        {
            model.value.data.forEach((item) => item.selected = e.detail.checked)
        }
        model.value.selectedCount = model.value.data.filter((item) => item.selected).length
    }
</script>

<template>
    <onyks-container gap="l" align="center">
        <BasicSearch v-model="model"></BasicSearch>
        <onyks-container :class="{ extend: model.extend }" :padding="`${model.extend ? 'l' : ''}`">
            <onyks-table :columns="model?.columns ?? []" :data="model?.data ?? []" @checkbox-click="handleCheckboxClick"></onyks-table>
        </onyks-container>
        <onyks-container type="group" align="center" justify="center" gap="m">
            <onyks-pagination-nav :max-index="Math.ceil(model.total / model.limit)" :index="model.page" max-view="3" size="m" @page-change="model.nextPage($event.detail.index)"></onyks-pagination-nav>
            <onyks-text>Selected:&emsp;{{model.selectedCount}}&emsp;|&emsp;Total:&emsp;{{ model.total }}</onyks-text>
        </onyks-container>
    </onyks-container>
</template>

<style lang="css" scoped>
    onyks-table
    {
        height: 450px;
        box-sizing: border-box;
        width: 100%;
    }

    .extend
    {
        box-sizing: border-box;
        width: 100vw;
        position: relative;
        padding-top: 0;
        padding-bottom: 0;
    }

    .extend > onyks-table
    {
        height: 700px;
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