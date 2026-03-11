<script setup>
    import TableTitle from './TableTitle.vue';
    import TableSearch from '../TableSearch.vue';
    import TableCounter from '../TableCounter.vue'
    import TableButtons from '../TableButtons.vue';

</script>

<template>
    <table-title>All elements</table-title>
    <div class="btns">
        <onyks-button background="green" size="l">Add</onyks-button>
        <onyks-button background="blue" size="l">Rename</onyks-button>
        <onyks-button background="red" size="l">Delete</onyks-button>
        <onyks-button background="green" size="l">View</onyks-button>
        <onyks-button background="blue" size="l">Labels</onyks-button>
        <onyks-button background="red" size="l">Export</onyks-button>
    </div>
    <table-search placeholder="Search for an element!"></table-search>
    <table-counter></table-counter>
    <onyks-table>
        <onyks-row header>
            <onyks-col checkbox></onyks-col>
            <onyks-col>Part Name</onyks-col>
            <onyks-col>Manufacturer</onyks-col>
            <onyks-col>Description</onyks-col>
            <onyks-col>Datasheet</onyks-col>
            <onyks-col>Value</onyks-col>
            <onyks-col>Quantity</onyks-col>
            <onyks-col>Library Reference</onyks-col>
            <onyks-col>Library Path</onyks-col>
            <onyks-col>Footprint Reference No. 1</onyks-col>
            <onyks-col>Footprint Path No. 1</onyks-col>
            <onyks-col>Footprint Reference No. 2</onyks-col>
            <onyks-col>Footprint Path No. 2</onyks-col>
            <onyks-col>Footprint Reference No. 3</onyks-col>
            <onyks-col>Footprint Path No. 3</onyks-col>
        </onyks-row>
    </onyks-table>
</template>

<style scoped>

    .btns 
    {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        grid-column-gap: var(--spacing-md);
        grid-row-gap: var(--spacing-md);
    }

    onyks-table
    {
        height: 450px;
    }

    onyks-button
    {
        min-width: 150px;
    }

    @media screen and (max-width: 1000px)
    {
        .btns 
        {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: repeat(2, 1fr);
        }
    }

    @media screen and (max-width: 600px)
    {
        .btns 
        {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            grid-template-rows: repeat(3, 1fr);
        }
    }
</style>    