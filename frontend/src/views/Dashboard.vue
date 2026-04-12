<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import { api_call } from '../utils/database'

    const total_elements = ref(0)
    const total_tables = ref(0)
    const total_manufacturers = ref(0)
    const total_suppliers = ref(0)
    const last_added_element = ref({part_name: "N/A", uuid: "N/A", manufacturer: "N/A", created_at: "14:32:32, 01.01.1970"})
    const repository_summary = ref({footprints_total: 0, symbols_total: 0, pcblibs_files_total: 0, schlibs_files_total: 0})
    const tables_amounts = ref({})

    onMounted(async () => 
    {
        let received_data = null;

        received_data = await api_call('/api/elements/total');
        total_elements.value = received_data.status == 200? received_data.data.total:0
        
        received_data = await api_call('/api/tables/total');
        total_tables.value = received_data.status == 200? received_data.data.total:0

        received_data = await api_call('/api/manufacturers/total');
        total_manufacturers.value = received_data.status == 200? received_data.data.total:0

        received_data = await api_call('/api/suppliers/total');
        total_suppliers.value = received_data.status == 200? received_data.data.total:0

        received_data = await api_call('/api/elements/last_added');
        last_added_element.value = received_data.status == 200? received_data.data:last_added_element.value

        received_data = await api_call('/api/repository/summary')
        repository_summary.value = received_data.status == 200? received_data.data:repository_summary.value

        received_data = await api_call('/api/tables/amounts')
        tables_amounts.value = received_data.status == 200? received_data.data.tables:tables_amounts.value
    })
</script>

<template>
    <PanelContent>
        <Title>Dashboard</Title>
    <onyks-grid cols="9">

        <onyks-card title="Total Elements" span="3">
            <div class="desc counter">{{ total_elements }}</div>
        </onyks-card>

        <onyks-card title="Total Tables" span="3">
            <div class="desc counter">{{ total_tables }}</div>
        </onyks-card>

        <onyks-card title="Total Manufacturers" span="3">
            <div class="desc counter">{{ total_manufacturers }}</div>
        </onyks-card>

        <onyks-card title="Total Suppliers" span="4">
            <div class="desc counter">{{ total_suppliers }}</div>
        </onyks-card>

        <onyks-card title="Repository Summary" span="5">
            <div class="desc text">
                <div class="row">
                    <div class="col">
                        <p>Symbols</p>
                        <p>Footprints</p>
                        <p>PcbLib Files</p>
                        <p>SchLib Files</p>
                    </div>
                    <div class="col">
                        <p>{{ repository_summary.symbols_total }}</p>
                        <p>{{ repository_summary.footprints_total }}</p>
                        <p>{{ repository_summary.pcblibs_files_total }}</p>
                        <p>{{ repository_summary.schlibs_files_total }}</p>
                    </div>
                </div>
            </div>
        </onyks-card>


        <onyks-card title="Last added element" span="9">
            <div class="desc text">
                <div class="row">
                    <div class="col">
                        <p>UUID</p>
                        <p>Part Name</p>
                        <p>Manufacturer</p>
                        <p>Created at</p>
                    </div>
                    <div class="col">
                        <p>{{ last_added_element.uuid }}</p>
                        <p>{{ last_added_element.part_name }}</p>
                        <p>{{ last_added_element.manufacturer }}</p>
                        <p>{{ last_added_element.created_at }}</p>
                    </div>
                </div>
            </div>
        </onyks-card>
    </onyks-grid>

    <h2>Tables</h2>

    <onyks-grid cols="4">
        <onyks-card v-for="(count, name) in tables_amounts" :key="name" span="1" :title="name">
            <div class="desc table-counter">{{ count }}</div>
        </onyks-card>
    </onyks-grid>
</PanelContent>
</template>

<style lang="css" scoped>
    .counter 
    {
        font-size: 4rem;
        font-weight: bold;
    }

    .table-counter
    {
        font-size: 2rem;
        font-weight: bold;
    }

    .text
    {
        font-size: 1.2rem;
    }

    .text p 
    {
        margin: 0.5rem 0;
    }

    .row
    {
        display: flex;
        flex-direction: row;
    }

    .col
    {
        flex: 1;
    }
</style>