<script setup>
    import ManufacturerTable from './parts/ManufacturerTable.vue';
    import SupplierTable from './parts/SupplierTable.vue';
    import WarningElement from '@/components/WarningElement.vue';
    import PageContentElement from '@/components/PageContentElement.vue';


</script>

<template>
    <PageContentElement>
        <h1>Management</h1>
        <WarningElement></WarningElement>
        <!-- <SupplierTable></SupplierTable> -->
        <ManufacturerTable></ManufacturerTable>
    </PageContentElement>
</template>

<style scoped>
  
</style>