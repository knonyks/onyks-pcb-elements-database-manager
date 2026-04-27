<script setup lang="ts">
    import { api_manufacturer_total } from '@/utils/api';
    import { api_supplier_total } from '@/utils/api';
    import { ref } from 'vue';
    import { onMounted } from 'vue';
    import PageContentElement from '@/components/PageContentElement.vue';
    import WarningElement from '@/components/WarningElement.vue';

    const manufacturer_total = ref(0)
    const supplier_total = ref(0)

    onMounted(async () => 
    {
        try
        {
            manufacturer_total.value = (await api_manufacturer_total()).data
            supplier_total.value = (await api_supplier_total()).data

        }
        catch(error)
        {
            console.log("!!!ERROR!!!", error)
        }
    })
</script>

<template>
    <PageContentElement>
        <h1>Dashboard</h1>
        <WarningElement></WarningElement>
        <onyks-grid cols="3">
            <onyks-card title="Total Manufacturers">
                <h1>{{ manufacturer_total }}</h1>
            </onyks-card>
            <onyks-card title="Total Suppliers">
                <h1>{{ supplier_total }}</h1>
            </onyks-card>
        </onyks-grid>
    </PageContentElement>
</template>

<style lang="css" scoped>
 
</style>