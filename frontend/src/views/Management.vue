<script setup>
    import {onMounted, ref} from 'vue';
    import {api_call} from '@/utils/database';

    onMounted(() =>
    {

    })
</script>

<template>
    <PanelContent>
        <Title>Management</Title>
        <ElementsTable></ElementsTable>
        <TablesTable></TablesTable>
        <ManufacturersTable></ManufacturersTable>
        <SuppliersTable></SuppliersTable>
    </PanelContent>
</template>

<style scoped>

</style>