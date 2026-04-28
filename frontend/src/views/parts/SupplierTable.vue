<script setup lang="js">
    import BasicTable from '@/components/BasicTable.vue';
    import PageContentElement from '@/components/PageContentElement.vue';
    import { api_supplier_list } from '@/utils/api';
    import { DateTime } from "luxon";

    const columns = [{ key: 'selected', label: 'Select' },
    { key: 'id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { key: 'created_at', label: 'Created' }]

    const update = async (page = 1, limit = 50) =>
    {
        let result = await api_supplier_list(page, limit)
        result.data.data.map((x) => {
            x.selected = false
            x.created_at = DateTime.fromISO(x.created_at, { zone: 'utc' }).setZone("Europe/Warsaw").toFormat("dd.MM.yyyy HH:mm");
        })
        return result
    }
</script>

<template>
    <PageContentElement>
        <h1>Suppliers</h1>
        <BasicTable :columns="columns" :update="update"></BasicTable>
    </PageContentElement>
</template>