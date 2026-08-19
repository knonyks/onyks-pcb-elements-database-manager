<script setup>
    import { useWindowSize } from '@vueuse/core';
    import { ref } from 'vue';
    import RepositoryModelSelector from './RepositoryModelSelector.vue';
    import ValueSelector from '../ValueSelector.vue';
    import { manufacturer, table } from '@/utils/api.js';
    import AddItemDialog from './management/AddItemDialog.vue';

    const props = defineProps(['type'])
    const model = defineModel({ data: Object })
    const {width} = useWindowSize()

    const selectors = ref({manufacturer: null, table: null})
    const dialogs = ref({symbol: null, footprint1: null, footprint2: null, footprint3: null, manufacturer: {add: null}, table: {add: null}})
    const filters = ref(
    {
        footprint: (e) => 
        {
            return e.type == 'dir' || e.type == 'pcblib' || e.type == 'footprint'
        },
        symbol: (e) =>
        {
            return e.type == 'dir' || e.type == 'schlib' || e.type == 'symbol'
        }
    })
</script>

<template>
    <onyks-container gap="l" type="grid" :cols="width > 550? 2:1" padding="">
        
        <onyks-container gap="l" padding="">
            <!-- UUID -->
            <onyks-header level="5" v-if="props.type == 'details'">UUID</onyks-header>

            <onyks-textfield :disabled="props.type === 'details'" 
            v-if="props.type == 'details'" 
            size="m" placeholder="Part Name" 
            type="text" v-model="model.uuid"></onyks-textfield>

            <!-- Part Name -->
            <onyks-header level="5">Part Name</onyks-header>
            <onyks-textfield :disabled="props.type === 'details'" size="m" placeholder="Part Name" 
            type="text" v-model="model.partName"></onyks-textfield>
            <onyks-text size="m" v-if="props.type != 'details'">Min. 3 characters</onyks-text>

            <!-- Manufacturer -->
            <onyks-header level="5">Manufacturer</onyks-header>
            <onyks-text v-if="props.type != 'details'">Selected: {{ model.manufacturer  || 'Undefined'}}</onyks-text>
            <ValueSelector :ref="(el) => { if (el) selectors.manufacturer = el }"  @add-click="dialogs?.manufacturer?.add?.open"
            @edit-click="dialogs?.manufacturer?.edit?.open" :action="manufacturer.list" v-model:name="model.manufacturer" 
            v-if="props.type != 'details'" subject="manufacturer"></ValueSelector>
            
            <onyks-textfield v-else :disabled="props.type === 'details'" size="m" placeholder="Part Name" type="text" v-model="model.manufacturer"></onyks-textfield>
        </onyks-container>

        <onyks-container gap="l" padding="">
            <!-- Value -->
            <onyks-header level="5">Value</onyks-header>
            <onyks-textfield :disabled="props.type === 'details'" size="m" placeholder="Value" type="text" v-model="model.value"></onyks-textfield>
            <onyks-text size="m" v-if="props.type != 'details'">Max. 256 characters</onyks-text>

            <!-- Table -->
            <onyks-header level="5" v-model="model.table">Table</onyks-header>
            <onyks-text v-if="props.type != 'details'">Selected: {{ model.table  || 'Undefined'}}</onyks-text>
            <ValueSelector :ref="(el) => { if (el) selectors.table = el }" 
                @add-click="dialogs?.table?.add?.open" :action="table.list" 
                @edit-click="dialogs?.table?.edit?.open" v-model:name="model.table" v-if="props.type != 'details'" subject="table"></ValueSelector>
            <onyks-textfield v-else :disabled="props.type === 'details'" size="m" placeholder="Part Name" type="text" v-model="model.table"></onyks-textfield>

            <!-- Created At -->
            <onyks-header v-if="props.type == 'details'" level="5">Created At</onyks-header>
            <onyks-textfield v-if="props.type == 'details'" :disabled="props.type === 'details'" size="m" placeholder="Value" type="text" v-model="model.createdAt"></onyks-textfield>
        </onyks-container>

    </onyks-container>

</template>

<style scoped>
    onyks-textfield
    {
        width: 100%;
    }

    onyks-button
    {
        width: 140px;
    }
</style>