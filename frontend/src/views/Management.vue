<script setup>
    import Panel_Content from '../components/Panel_Content.vue';
    import {onMounted, ref} from 'vue';
    import {api_call} from '@/utils/database';
    import Title from '@/components/Title.vue';
    import ElementsTable from '@/components/management/ElementsTable.vue';
    import SuppliersTable from '@/components/management/SuppliersTable.vue';
    import ManufacturersTable from '@/components/management/ManufacturersTable.vue';
    import TablesTable from '@/components/management/TablesTable.vue';

    onMounted(() =>
    {

    })
</script>

<template>
    <Panel_Content>
        <Title>Management</Title>
        <ElementsTable></ElementsTable>
        <TablesTable></TablesTable>
        <ManufacturersTable></ManufacturersTable>
        <SuppliersTable></SuppliersTable>
    </Panel_Content>
</template>

<style scoped>

</style>