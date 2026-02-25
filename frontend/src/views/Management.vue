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

        <onyks-dialog  id="add-manufacturer-dialog" has-title="true" title="Add a manufacturer">
            <p style="margin-top: 0;">Enter a name of a manufacturer</p>
            <onyks-textfield size="l" type="text" style="width: 100%;"></onyks-textfield>
            
            <onyks-button slot="footer" background="green" onclick="document.getElementById('add-manufacturer-dialog').opened = false">OK</onyks-button>
            <onyks-button slot="footer" background="red" onclick="console.log('Hi!')">Cancel</onyks-button>
        </onyks-dialog>

        <h1>Manufacturers</h1>
        <div class="buttons-container">
            <onyks-button size="l" background="green" onclick="document.getElementById('add-manufacturer-dialog').opened = true">Add</onyks-button>
            <onyks-button size="l" background="blue" disabled>Edit</onyks-button>
            <onyks-button size="l" background="red" disabled>Delete</onyks-button>
        </div>
        <onyks-table>
            <onyks-row header>
                <onyks-col>ID</onyks-col>
                <onyks-col>Manufacturer</onyks-col>
                <onyks-col>Elements Amount</onyks-col>
                <onyks-col>Created at</onyks-col>
            </onyks-row>
            <onyks-row>
                <onyks-col>1</onyks-col>
                <onyks-col>Example Manufacturer</onyks-col>
                <onyks-col>100</onyks-col>
                <onyks-col>2024-01-01 12:00:00</onyks-col>
            </onyks-row>
        </onyks-table>

        <onyks-dialog  id="add-supplier-dialog" has-title="true" title="Add a supplier">
            <p style="margin-top: 0;">Enter a name of a supplier</p>
            <onyks-textfield size="l" type="text" style="width: 100%;"></onyks-textfield>
            
            <onyks-button slot="footer" background="green" onclick="document.getElementById('add-supplier-dialog').opened = false">OK</onyks-button>
            <onyks-button slot="footer" background="red" onclick="console.log('Hi!')">Cancel</onyks-button>
        </onyks-dialog>

        <h1>Suppliers</h1>
        <div class="buttons-container">
            <onyks-button size="l" background="green" onclick="document.getElementById('add-supplier-dialog').opened = true">Add</onyks-button>
            <onyks-button size="l" background="blue" disabled>Edit</onyks-button>
            <onyks-button size="l" background="red" disabled>Delete</onyks-button>
        </div>
        <onyks-table>
            <onyks-row header>
                <onyks-col>ID</onyks-col>
                <onyks-col>Supplier</onyks-col>
                <onyks-col>Elements Amount</onyks-col>
                <onyks-col>Created at</onyks-col>
            </onyks-row>
            <onyks-row>
                <onyks-col>1</onyks-col>
                <onyks-col>Example Supplier</onyks-col>
                <onyks-col>100</onyks-col>
                <onyks-col>2024-01-01 12:00:00</onyks-col>
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