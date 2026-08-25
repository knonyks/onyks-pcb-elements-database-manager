<script setup>
    import { useWindowSize } from '@vueuse/core';
    import ValueSelector from './ValueSelector.vue';
    import { ref } from 'vue';
    import { manufacturer, table, supplier } from '@/utils/api.js';
    import AddItemDialog from './AddItemDialog.vue';
    import EditItemDialog from './EditItemDialog.vue';
    import DeleteItemDialog from './DeleteItemDialog.vue';
    import RepositoryModelSelector from './RepositoryModelSelector.vue';
    import SuppliersSelector from './SuppliersSelector.vue';
    import DatasheetPicker from './DatasheetPicker.vue';
    import { defineExpose } from 'vue';


    const {width} = useWindowSize()
    const props = defineProps(['type'])
    const model = defineModel({ data: Object })
    const selectors = ref({manufacturer: null, supplier: null, table: null})
    const dialogs = ref({manufacturer: {add: null, edit: null, delete: null}, 
    table: {add: null, edit: null, delete: null}, supplier: {add: null, edit: null, delete: null}, library: null, footprint1: null, footprint2: null, footprint3: null})
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

    const datasheetFile = ref(null)
    defineExpose({datasheetFile})
</script>

<template>
    <onyks-container gap="l" type="grid" :cols="width > 550? 2:1" padding="">
        
        <onyks-container gap="l" padding="">
            <!-- UUID -->
            <onyks-header level="5" v-if="props.type == 'details' || props.type == 'edit'">UUID</onyks-header>

            <onyks-textfield :disabled="props.type === 'details' || props.type == 'edit'" 
                v-if="props.type == 'details' || props.type == 'edit'" 
                size="m" placeholder="Part Name" 
                type="text" v-model="model.uuid">
            </onyks-textfield>

            <!-- Part Name -->
            <onyks-header level="5">Part Name</onyks-header>
            
            <onyks-textfield :disabled="props.type === 'details'" 
                size="m" placeholder="Part Name" 
                type="text" v-model="model.partName">
            </onyks-textfield>
            
            <onyks-text size="m" v-if="props.type != 'details'">Min. 3 characters</onyks-text>

            <!-- Manufacturer -->
            <onyks-header level="5">Manufacturer</onyks-header>
            
            <onyks-text v-if="props.type != 'details'">Selected: {{ model.manufacturer  || 'Undefined'}}</onyks-text>
            
            <ValueSelector :ref="(el) => { if (el && selectors) selectors.manufacturer = el }"  
                @add-click="dialogs?.manufacturer?.add?.open"
                @edit-click="() => {dialogs.manufacturer.edit.open(selectors.manufacturer.name, selectors.manufacturer.id)}" 
                @delete-click="() => {dialogs.manufacturer.delete.open([{name: selectors.manufacturer.name, id: selectors.manufacturer.id}])}"
                :action="manufacturer.list" v-model:name="model.manufacturer" 
                v-if="props.type != 'details'" subject="manufacturer">
            </ValueSelector>

            <onyks-textfield v-else :disabled="props.type === 'details'" 
                size="m" placeholder="Manufacturer" type="text" 
                v-model="model.manufacturer">
            </onyks-textfield>
            
            <AddItemDialog subject="manufacturer" 
                :ref="(el) => { if (el && dialogs) dialogs.manufacturer.add = el }"
                :action="manufacturer.create"
                @success="selectors?.manufacturer?.reset">
            </AddItemDialog>

            <EditItemDialog subject="manufacturer"
                :ref="(el) => { if (el && dialogs) dialogs.manufacturer.edit = el }"
                :action="manufacturer.edit"
                @success="selectors?.manufacturer?.reset">
            </EditItemDialog>

            <DeleteItemDialog
                subject="manufacturer(s)"
                :processor="(item) => item.id"
                :ref="(el) => { if (el && dialogs) dialogs.manufacturer.delete = el }"
                :action="manufacturer.delete"
                :formater="(item) => item.name"
                @success="selectors?.manufacturer?.reset">
                <template v-slot:top>
                    <onyks-alert type="warning">This operation cannot be undone.</onyks-alert>
                </template>
            </DeleteItemDialog>

            <onyks-header level="5">Description</onyks-header>

            <onyks-textarea 
                size="m" 
                placeholder="Description"
                v-model="model.description"
                rows="10" 
                cols="100" 
                minlength="0" 
                maxlength="256"
                :disabled="props.type === 'details'" 
                resize="none">
            </onyks-textarea>

        </onyks-container>

        <onyks-container gap="l" padding="">
            <!-- Value -->
            <onyks-header level="5">Value</onyks-header>
            <onyks-textfield :disabled="props.type === 'details'" size="m" placeholder="Value" type="text" v-model="model.value"></onyks-textfield>
            <onyks-text size="m" v-if="props.type != 'details'">Max. 256 characters</onyks-text>

            <!-- Table -->
            <onyks-header level="5" v-model="model.table">Table</onyks-header>
            <onyks-text v-if="props.type != 'details'">Selected: {{ model.table  || 'Undefined'}}</onyks-text>
            <ValueSelector :ref="(el) => { if (el && selectors) selectors.table = el }"  
                @add-click="dialogs?.table?.add?.open"
                @edit-click="() => {dialogs.table.edit.open(selectors.table.name, selectors.table.id)}" 
                @delete-click="() => {dialogs.table.delete.open([{name: selectors.table.name, id: selectors.table.id}])}"
                :action="table.list" v-model:name="model.table" 
                v-if="props.type != 'details'" subject="table">
            </ValueSelector>

            <AddItemDialog subject="table" 
                :ref="(el) => { if (el && dialogs) dialogs.table.add = el }"
                :action="table.create"
                @success="selectors?.table?.reset">
            </AddItemDialog>

            <EditItemDialog subject="table"
                :ref="(el) => { if (el && dialogs) dialogs.table.edit = el }"
                :action="table.edit"
                @success="selectors?.table?.reset">
            </EditItemDialog>

            <DeleteItemDialog
                subject="table(s)"
                :processor="(item) => item.id"
                :ref="(el) => { if (el && dialogs) dialogs.table.delete = el }"
                :action="table.delete"
                :formater="(item) => item.name"
                @success="selectors?.table?.reset">
                <template v-slot:top>
                    <onyks-alert type="warning">This operation cannot be undone.</onyks-alert>
                </template>
            </DeleteItemDialog>

            <onyks-textfield v-if="props.type == 'details'" :disabled="props.type === 'details'" 
                size="m" placeholder="Table" type="text" 
                v-model="model.table">
            </onyks-textfield>

            <!-- Availability -->
            <onyks-header level="5">Availability</onyks-header>
            <onyks-textfield :disabled="props.type === 'details'" size="m" placeholder="Value" type="text" v-model="model.availability"></onyks-textfield>
            <onyks-text size="m" v-if="props.type != 'details'">Max. 256 characters</onyks-text>

            <!-- Created At -->
            <onyks-header v-if="props.type == 'details'" level="5">Created At</onyks-header>
            <onyks-textfield v-if="props.type == 'details'" :disabled="props.type === 'details'" size="m" placeholder="Value" type="text" v-model="model.createdAt"></onyks-textfield>
        </onyks-container>

        <onyks-container gap="l" padding="">
            <!-- Library -->
            <onyks-header level="5">Schematic</onyks-header>

            <!-- Library Reference -->
            <onyks-text>Library Reference</onyks-text>
            <onyks-textfield disabled size="m" 
                placeholder="Library Reference" 
                type="text" 
                v-model="model.libraryReference">
            </onyks-textfield>

            <!-- Library Path -->
            <onyks-text>Library Path</onyks-text>
            <onyks-textfield disabled size="m" 
                placeholder="Library Path" 
                type="text" v-model="model.libraryPath">
            </onyks-textfield>
            
            <onyks-button v-if="props.type != 'details'" background="blue" @click="dialogs?.library?.open">Select</onyks-button>

            <RepositoryModelSelector v-if="props.type != 'details'" :filter="filters.symbol" 
                title="symbol" :ref="(el) => { if (el && dialogs) dialogs.library = el }" 
                @model-select="(e) => {model.libraryReference = e.name; model.libraryPath = e.path.join('/')}">
            </RepositoryModelSelector>

            <!-- Footprint No. 1 -->
            <onyks-header level="5">Footprint No. 1</onyks-header>

            <!-- Footprint Reference -->
            <onyks-text>Footprint Reference</onyks-text>
            <onyks-textfield size="m" placeholder="Footprint Reference" disabled type="text" v-model="model.footprintReferenceNo1"></onyks-textfield>

            <!-- Footprint Path -->
            <onyks-text>Footprint Path</onyks-text>
            <onyks-textfield size="m" placeholder="Footprint Path" type="text" disabled v-model="model.footprintPathNo1"></onyks-textfield>
            <onyks-button v-if="props.type != 'details'" background="yellow" @click="dialogs?.footprint1?.open">Select</onyks-button>



            <RepositoryModelSelector v-if="props.type != 'details'" :filter="filters.footprint" 
            title="footprint no. 1" :ref="(el) => { if (el) dialogs.footprint1 = el }" 
            @model-select="(e) => {model.footprintReferenceNo1 = e.name; model.footprintPathNo1 = e.path.join('/')}">
            </RepositoryModelSelector>

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

            <RepositoryModelSelector v-if="props.type != 'details'" :filter="filters.footprint" 
            title="footprint no. 2" :ref="(el) => { if (el) dialogs.footprint2 = el }" 
            @model-select="(e) => {model.footprintReferenceNo2 = e.name; model.footprintPathNo2 = e.path.join('/')}">
            </RepositoryModelSelector>

            <onyks-header level="5">Footprint No. 3</onyks-header>

            <!-- Footprint Reference -->
            <onyks-text>Footprint Reference</onyks-text>
            <onyks-textfield size="m" disabled placeholder="Footprint Reference" type="text" v-model="model.footprintReferenceNo3"></onyks-textfield>

            <!-- Footprint Path -->
            <onyks-text>Footprint Path</onyks-text>
            <onyks-textfield size="m" placeholder="Footprint Path" disabled type="text" v-model="model.footprintPathNo3"></onyks-textfield>
            <onyks-button v-if="props.type != 'details'" background="yellow" @click="dialogs?.footprint3.open()">Select</onyks-button>
        
            <RepositoryModelSelector v-if="props.type != 'details'" :filter="filters.footprint" 
            title="footprint no. 3" :ref="(el) => { if (el) dialogs.footprint3 = el }" 
            @model-select="(e) => {model.footprintReferenceNo3 = e.name; model.footprintPathNo3 = e.path.join('/')}">
            </RepositoryModelSelector>


        </onyks-container>

        <onyks-container gap="l" padding="">
            <onyks-header level="5">Suppliers</onyks-header>

            <SuppliersSelector @add-click="dialogs?.supplier?.add?.open" :ref="(el) => { if (el && selectors) selectors.supplier = el }"
                @edit-click="() => {dialogs.supplier.edit.open(selectors.supplier.name, selectors.supplier.id)}" 
                @delete-click="() => {dialogs.supplier.delete.open([{name: selectors.supplier.name, id: selectors.supplier.id}])}"
                :action="supplier.list" v-model:codes="model.suppliers"
                 subject="supplier" :disabled="props.type === 'details'">
            </SuppliersSelector>
            
            <AddItemDialog subject="supplier" 
                :ref="(el) => { if (el && dialogs) dialogs.supplier.add = el }"
                :action="supplier.create"
                @success="selectors?.supplier?.reset">
            </AddItemDialog>

            <EditItemDialog subject="supplier"
                :ref="(el) => { if (el && dialogs) dialogs.supplier.edit = el }"
                :action="supplier.edit"
                @success="selectors?.supplier?.reset">
            </EditItemDialog>

            <DeleteItemDialog
                subject="supplier(s)"
                :processor="(item) => item.id"
                :ref="(el) => { if (el && dialogs) dialogs.supplier.delete = el }"
                :action="supplier.delete"
                :formater="(item) => item.name"
                @success="selectors?.supplier?.reset">
                <template v-slot:top>
                    <onyks-alert type="warning">This operation cannot be undone.</onyks-alert>
                </template>
            </DeleteItemDialog>
        </onyks-container>

        <onyks-container gap="l" padding="">
            <onyks-header level="5">Datasheet</onyks-header>
            <DatasheetPicker :datasheet="true" :type="props.type" @change="(e) => {datasheetFile = e}"></DatasheetPicker>
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

    onyks-textarea
    {
        width: 100%;
    }
</style>