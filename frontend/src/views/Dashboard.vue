<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import { api_call } from '../utils/api';
    import PageContent from '@/components/PageContent.vue';
    import Warning from '@/components/Warning.vue';

    const total_manufacturers = ref(0)
    const total_suppliers = ref(0)

    onMounted(async () => 
    {
        let received_data = null;

        received_data = await api_call('/api/manufacturers/total');
        total_manufacturers.value = received_data.status == 200? received_data.data.total:0

        received_data = await api_call('/api/suppliers/total');
        total_suppliers.value = received_data.status == 200? received_data.data.total:0
    })
</script>

<template>
    <PageContent>
        <h1>Dashboard</h1>
        <Warning></Warning>
        <onyks-grid cols="3">
            <onyks-card title="Total Manufacturers">
                <h1>{{ total_manufacturers }}</h1>
            </onyks-card>
            <onyks-card title="Total Suppliers">
                <h1>{{ total_suppliers }}</h1>
            </onyks-card>
        </onyks-grid>
    </PageContent>
</template>

<style lang="css" scoped>
 
</style>