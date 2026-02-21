<script setup>
    import Panel_Content from '../components/Panel_Content.vue';
    import { Onyks_Button } from 'onyks-web-ui-system';
</script>

<template>
    <Panel_Content>
        <h1>Users</h1>
        <div class="buttons-container">
            <onyks-button size="l" background="green">Add</onyks-button>
            <onyks-button size="l" background="blue" disabled>Edit</onyks-button>
            <onyks-button size="l" background="red" disabled>Delete</onyks-button>
            <onyks-button size="l" background="green">Import</onyks-button>
        </div>
        <onyks-table>
            <onyks-row header>
                <onyks-col>UUID</onyks-col>
                <onyks-col>Name</onyks-col>
                <onyks-col>Family Name</onyks-col>
                <onyks-col>E-mail</onyks-col>
                <onyks-col>Expiration Time</onyks-col>
                <onyks-col>Rank</onyks-col>
            </onyks-row>
        </onyks-table>
    </Panel_Content>
</template>

<style scoped>
    onyks-button 
    {
        width: fit-content;
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