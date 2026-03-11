<script setup>
    import TableButtons from '../TableButtons.vue';
    import TableCounter from '../TableCounter.vue';
    import TableSearch from '../TableSearch.vue';
    import TableTitle from './TableTitle.vue';
</script>

<template>
    <main>
        <table-title>Tables of elements</table-title>
        <table-buttons>
            <onyks-button background="green" size="l">Add</onyks-button>
            <onyks-button background="blue" size="l">Rename</onyks-button>
            <onyks-button background="red" size="l">Delete</onyks-button>
        </table-buttons>
        <table-search placeholder="Search for a table!"></table-search>
        <table-counter></table-counter>
        <onyks-table>
            <onyks-row header>
                <onyks-col checkbox></onyks-col>
                <onyks-col>Name</onyks-col>
            </onyks-row>
        </onyks-table>
    </main>

</template>

<style scoped>
    main
    {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-lg);
    }

    onyks-table
    {
        height: 450px;
    }
</style>    