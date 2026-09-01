<script setup lang="js">
    import { ref } from 'vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import { onMounted } from 'vue';
    import { elements, manufacturers, suppliers, tables } from '@/utils/api';
    import DataLoader from '@/components/DataLoader.vue';
    import { useWindowSize } from '@vueuse/core';
    import { Time } from '@/utils/tools';

    const {width} = useWindowSize()
    const isLoading = ref(true)
    const data = ref(
    {
        elements: {},
        tables: {},
        suppliers: {},
        manufacturers: {},
    })
    
    onMounted(async () =>
    {
        data.value.elements = (await elements.count()).data
        data.value.elements.lastAdded = (await elements.lastAdded()).data
        data.value.elements.lastAdded.createdAt = Time.getLocalTime(data.value.elements.lastAdded.createdAt, 'en')
        data.value.tables = (await tables.count()).data
        data.value.tables.counts = (await tables.counts()).data
        data.value.suppliers = (await suppliers.count()).data
        data.value.manufacturers = (await manufacturers.count()).data
        data.value.manufacturers.counts = (await manufacturers.counts()).data
        isLoading.value = false
    })
</script>

<template>
    <DataLoader :is-loading="isLoading">
        <ManagerPage title="Dashboard">
            
            <onyks-header level="3">Overview</onyks-header>

            <onyks-container gap="m" type="grid" :cols="width > 550? 2:1">

                <onyks-card title="Last added element" size="l">

                    <onyks-container gap="m">

                        <onyks-container type="stack" align="left" gap="s">
                            <onyks-header level="6">Part name</onyks-header>
                            <onyks-text size="l">{{ data.elements?.lastAdded?.partName || 'Undefined' }}</onyks-text>
                        </onyks-container>

                        <onyks-container type="stack" align="left" gap="s">
                            <onyks-header level="6">Manufacturer</onyks-header>
                            <onyks-text size="l">{{data.elements?.lastAdded?.manufacturer || 'Undefined'}}</onyks-text>
                        </onyks-container>

                        <onyks-container type="stack" align="left" gap="s">
                            <onyks-header level="6">Table</onyks-header>
                            <onyks-text size="l">{{data.elements?.lastAdded?.table || 'Undefined'}}</onyks-text>
                        </onyks-container>

                        <onyks-container type="stack" align="left" gap="s">
                            <onyks-header level="6">Created At</onyks-header>
                            <onyks-text size="l">{{data.elements?.lastAdded?.createdAt || 'Undefined'}}</onyks-text>
                        </onyks-container>

                    </onyks-container>
                </onyks-card>

                <onyks-grid cols="4" gap="m">
                    <onyks-card title="Elements" span="2" size="l">
                        <onyks-header level="3">{{ data?.elements?.count || 'Undefined' }}</onyks-header>
                    </onyks-card>

                    <onyks-card title="Tables" span="2" size="l">
                        <onyks-header level="3">{{ data?.tables?.count || 'Undefined' }}</onyks-header>
                    </onyks-card>

                    <onyks-card title="Manufacturers" span="2" size="l">
                        <onyks-header level="3">{{ data?.manufacturers?.count || 'Undefined' }}</onyks-header>
                    </onyks-card>

                    <onyks-card title="Suppliers" span="2" size="l">
                        <onyks-header level="3">{{ data?.suppliers?.count || 'Undefined' }}</onyks-header>
                    </onyks-card>
                </onyks-grid>

            </onyks-container>

            <onyks-header level="3">Tables</onyks-header>

            <onyks-grid cols="6" v-if="Object.keys(data.tables.counts || {}).length > 0"  gap="m">
                <onyks-card v-for="(number, name) in data.tables.counts" :key="name" :title="name" span="2" size="l">
                    <onyks-header level="2">{{ number }}</onyks-header>
                </onyks-card>
            </onyks-grid>

            <onyks-text v-else>There is no tables to show.</onyks-text>

            <onyks-header level="3">Manufacturers</onyks-header>
            
            <onyks-grid cols="6" v-if="Object.keys(data.manufacturers.counts || {}).length > 0"  gap="m">
                <onyks-card v-for="(number, name) in data.manufacturers.counts" :title="name" span="2" size="l">
                    <onyks-header level="2">{{ number }}</onyks-header>
                </onyks-card>
            </onyks-grid>

            <onyks-text v-else>There is no manufacturers to show.</onyks-text>
        </ManagerPage>
    </DataLoader>
</template>

<style scoped>
    onyks-container > onyks-header
    {
        width: 120px;
        text-align: left;
    }

    onyks-card
    {
        height: fit-content;
    }
</style>