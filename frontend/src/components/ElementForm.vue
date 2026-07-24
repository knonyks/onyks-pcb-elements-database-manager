<script setup>
    import { useWindowSize } from '@vueuse/core';
    import { ref } from 'vue';
    import RepositoryModelSelector from './RepositoryModelSelector.vue';
    import ValueSelector from './ValueSelector.vue';
    import { manufacturer, table } from '@/utils/api.js';
    import AddItemDialog from './management/AddItemDialog.vue'

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

        <onyks-container gap="l" padding="">
            <!-- Library -->
            <onyks-header level="5">Symbol</onyks-header>

            <!-- Library Reference -->
            <onyks-text>Library Reference</onyks-text>
            <onyks-textfield disabled size="m" placeholder="Library Reference" type="text" v-model="model.libraryReference"></onyks-textfield>

            <!-- Library Path -->
            <onyks-text>Library Path</onyks-text>
            <onyks-textfield disabled size="m" placeholder="Library Path" type="text" v-model="model.libraryPath"></onyks-textfield>
            <onyks-button v-if="props.type != 'details'" background="blue" @click="dialogs?.symbol?.open">Select</onyks-button>

            <!-- Footprint No. 1 -->
            <onyks-header level="5">Footprint No. 1</onyks-header>

            <!-- Footprint Reference -->
            <onyks-text>Footprint Reference</onyks-text>
            <onyks-textfield size="m" placeholder="Footprint Reference" disabled type="text" v-model="model.footprintReferenceNo1"></onyks-textfield>

            <!-- Footprint Path -->
            <onyks-text>Footprint Path</onyks-text>
            <onyks-textfield size="m" placeholder="Footprint Path" type="text" disabled v-model="model.footprintPathNo1"></onyks-textfield>
            <onyks-button v-if="props.type != 'details'" background="yellow" @click="dialogs?.footprint1?.open">Select</onyks-button>

        </onyks-container>

        <onyks-container gap="l" padding="">
            <!-- Footprint No. 2 -->
            <onyks-header level="5">Footprint No. 2</onyks-header>

            <!-- Footprint Reference -->
            <onyks-text>Footprint Reference</onyks-text>
            <onyks-textfield size="m" disabled placeholder="Footprint Reference" type="text" v-model="model.footprintReferenceNo2"></onyks-textfield>

            <!-- Footprint Path -->
            <onyks-text>Footprint Path</onyks-text>
            <onyks-textfield size="m" disabled placeholder="Footprint Path" type="text" v-model="model.footprintPathNo2"></onyks-textfield>
            <onyks-button v-if="props.type != 'details'" background="yellow" @click="dialogs?.footprint2.open()">Select</onyks-button>

            <onyks-header level="5">Footprint No. 3</onyks-header>

            <!-- Footprint Reference -->
            <onyks-text>Footprint Reference</onyks-text>
            <onyks-textfield size="m" disabled placeholder="Footprint Reference" type="text" v-model="model.footprintReferenceNo3"></onyks-textfield>

            <!-- Footprint Path -->
            <onyks-text>Footprint Path</onyks-text>
            <onyks-textfield size="m" placeholder="Footprint Path" disabled type="text" v-model="model.footprintPathNo3"></onyks-textfield>
            <onyks-button v-if="props.type != 'details'" background="yellow" @click="dialogs?.footprint3.open()">Select</onyks-button>
        </onyks-container>

    </onyks-container>

    <RepositoryModelSelector v-if="props.type != 'details'" :filter="filters.symbol" 
    title="symbol" :ref="(el) => { if (el) dialogs.symbol = el }" 
    @model-select="(e) => {model.libraryReference = e.name; model.libraryPath = e.path.join('/')}">
    </RepositoryModelSelector>

    <RepositoryModelSelector v-if="props.type != 'details'" :filter="filters.footprint" 
    title="footprint no. 1" :ref="(el) => { if (el) dialogs.footprint1 = el }" 
    @model-select="(e) => {model.footprintReferenceNo1 = e.name; model.footprintPathNo1 = e.path.join('/')}">
    </RepositoryModelSelector>

    <RepositoryModelSelector v-if="props.type != 'details'" :filter="filters.footprint" 
    title="footprint no. 2" :ref="(el) => { if (el) dialogs.footprint2 = el }" 
    @model-select="(e) => {model.footprintReferenceNo2 = e.name; model.footprintPathNo2 = e.path.join('/')}">
    </RepositoryModelSelector>

    <RepositoryModelSelector v-if="props.type != 'details'" :filter="filters.footprint" 
    title="footprint no. 3" :ref="(el) => { if (el) dialogs.footprint3 = el }" 
    @model-select="(e) => {model.footprintReferenceNo3 = e.name; model.footprintPathNo3 = e.path.join('/')}">
    </RepositoryModelSelector>

    <AddItemDialog subject="manufacturer" :action="manufacturer.create" @success="selectors?.manufacturer?.reset"
    :ref="(el) => { if (el) dialogs.manufacturer.add = el }"></AddItemDialog>

    <AddItemDialog subject="table" :action="table.create" @success="selectors?.table?.reset"
    :ref="(el) => { if (el) dialogs.table.add = el }"></AddItemDialog>

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