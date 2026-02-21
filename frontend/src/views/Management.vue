<script setup>
    import Panel_Content from '../components/Panel_Content.vue';
    import { Onyks_Button } from 'onyks-web-ui-system';
</script>

<template>
    <Panel_Content>
        <h1>Elements</h1>
        <div class="buttons-container">
            <onyks-button size="l" background="green">Add</onyks-button>
            <onyks-button size="l" background="blue" disabled>Edit</onyks-button>
            <onyks-button size="l" background="red" disabled>Delete</onyks-button>
            <onyks-button size="l" background="green" disabled>Labels</onyks-button>
            <onyks-button size="l" background="blue" disabled>Details</onyks-button>
            <onyks-button size="l" background="red" disabled>Datasheet</onyks-button>
        </div>
        <onyks-table>
            <onyks-row header>
                <onyks-col>UUID</onyks-col>
                <onyks-col>Part Name</onyks-col>
                <onyks-col>Manufacturer</onyks-col>
                <onyks-col>Datasheet</onyks-col>
                <onyks-col>Description</onyks-col>
                <onyks-col>Value</onyks-col>
                <onyks-col>Availability</onyks-col>
                <onyks-col>Library Reference</onyks-col>
                <onyks-col>Library Path</onyks-col>
                <onyks-col>Footprint Reference No. 1</onyks-col>
                <onyks-col>Footprint Path No. 1</onyks-col>
                <onyks-col>Footprint Ref No. 2</onyks-col>
                <onyks-col>Footprint Path No. 2</onyks-col>
                <onyks-col>Footprint Ref No. 3</onyks-col>
                <onyks-col>Footprint Path No. 3</onyks-col>
                <onyks-col>Created at</onyks-col>
            </onyks-row>
        </onyks-table>

        <h1>Tables</h1>
        <div class="buttons-container">
            <onyks-button size="l" background="green">Add</onyks-button>
            <onyks-button size="l" background="blue" disabled>Edit</onyks-button>
            <onyks-button size="l" background="red" disabled>Delete</onyks-button>
        </div>
        <onyks-table>
            <onyks-row header>
                <onyks-col>UUID</onyks-col>
                <onyks-col>Table name</onyks-col>
                <onyks-col>Created at</onyks-col>
            </onyks-row>
        </onyks-table>

        <h1>Manufacturers</h1>
        <div class="buttons-container">
            <onyks-button size="l" background="green">Add</onyks-button>
            <onyks-button size="l" background="blue" disabled>Edit</onyks-button>
            <onyks-button size="l" background="red" disabled>Delete</onyks-button>
        </div>
        <onyks-table>
            <onyks-row header>
                <onyks-col>UUID</onyks-col>
                <onyks-col>Manufacturer</onyks-col>
                <onyks-col>Created at</onyks-col>
            </onyks-row>
        </onyks-table>

        <h1>Suppliers</h1>
        <div class="buttons-container">
            <onyks-button size="l" background="green">Add</onyks-button>
            <onyks-button size="l" background="blue" disabled>Edit</onyks-button>
            <onyks-button size="l" background="red" disabled>Delete</onyks-button>
        </div>
        <onyks-table>
            <onyks-row header>
                <onyks-col>UUID</onyks-col>
                <onyks-col>Supplier</onyks-col>
                <onyks-col>Created at</onyks-col>
            </onyks-row>
        </onyks-table>
    </Panel_Content>
</template>

<style scoped>
    onyks-button 
    {
        min-width: 150px;
    }

    onyks-table
    {
        width: 100%;
        height: 400px;
    }

    .buttons-container
    {
        display: flex;
        flex-direction: row;
        gap: 10px;
        width: 100%;
        height: fit-content;
        flex-wrap: wrap;
    }
</style>