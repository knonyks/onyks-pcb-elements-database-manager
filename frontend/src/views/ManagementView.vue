<script setup lang="js">
    import ElementsManagement from '@/components/management/ElementsManagement.vue';
    import ManufacturersManagement from '@/components/management/ManufacturersManagement.vue';
    import SuppliersManagement from '@/components/management/SuppliersManagement.vue';
    import TablesManagement from '@/components/management/TablesManagement.vue';
    import WarningAlert from '@/components/WarningAlert.vue';
</script>

<template>
    <onyks-container gap="l" padding="l">
        <onyks-header>Management</onyks-header>
        <WarningAlert></WarningAlert>
        <ElementsManagement></ElementsManagement>
        <TablesManagement></TablesManagement>
        <ManufacturersManagement></ManufacturersManagement>
        <SuppliersManagement></SuppliersManagement>
    </onyks-container>
</template>

<style scoped>

</style>