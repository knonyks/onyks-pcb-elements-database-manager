<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import { fetch_data } from '../utils/database'
    const total_elements = ref(0)
    const total_tables = ref(0)
    const last_added_element = ref({"part_name": "N/A", "uuid": "N/A"})
    const repository_stats = ref({
        footprints_total: 0,
        symbols_total: 0,
        pcblibs_files_total: 0,
        schlibs_files_total: 0
    })

    const total_manufacturers = ref(0)
    const total_suppliers = ref(0)
    const tables_amounts = ref({})
    const manufacturers_amounts = ref({})
    const suppliers_amounts = ref({})
    console.log("Fetching data...")
    onMounted(() => 
    {
        console.log("Mounted, fetching data...")
        fetch_data("/elements/total").then(data => total_elements.value = data.total)
        fetch_data("/tables/total").then(data => total_tables.value = data.total)
        fetch_data("/elements/last_added").then(data => last_added_element.value = data)
        fetch_data("/repository/summary").then(data => repository_stats.value = data)
        fetch_data("/manufacturers/total").then(data => total_manufacturers.value = data.total)
        fetch_data("/suppliers/total").then(data => total_suppliers.value = data.total)
        fetch_data("/tables/amounts").then(data => tables_amounts.value = data.tables)
        fetch_data("/manufacturers/amounts").then(data => manufacturers_amounts.value = data.manufacturers)
        fetch_data("/suppliers/amounts").then(data => suppliers_amounts.value = data.suppliers)
        // fetch_data("/suppliers/create", {name: "Supplier " + Math.floor(Math.random() * 1000)}).then(data => console.log(data))
    })
</script>

<template>
<h1>Hi, Jan Kowalski!</h1>

<onyks-grid cols="4">

    <onyks-card title="Total Elements" span="1">
        <div class="desc counter">{{ total_elements }}</div>
    </onyks-card>

    <onyks-card title="Total Tables" span="1">
        <div class="desc counter">{{ total_tables }}</div>
    </onyks-card>

    <onyks-card title="Total Manufacturers" span="1">
        <div class="desc counter">{{ total_manufacturers }}</div>
    </onyks-card>

    <onyks-card title="Total Suppliers" span="1">
        <div class="desc counter">{{ total_suppliers }}</div>
    </onyks-card>

    <onyks-card title="Last added element" span="2">
        <div class="desc text">
            <p>UUID: {{ last_added_element.uuid }}</p>
            <p>Part Name: {{ last_added_element.part_name }}</p>
        </div>
    </onyks-card>

    <onyks-card title="Repository Summary" span="2">
        <div class="desc text">
            <div class="row">
                <div class="col">
                    <p>Symbols</p>
                    <p>Footprints</p>
                    <p>PcbLib Files</p>
                    <p>SchLib Files</p>
                </div>
                <div class="col">
                    <p>{{ repository_stats.symbols_total }}</p>
                    <p>{{ repository_stats.footprints_total }}</p>
                    <p>{{ repository_stats.pcblibs_files_total }}</p>
                    <p>{{ repository_stats.schlibs_files_total }}</p>
                </div>
            </div>
        </div>
    </onyks-card>

</onyks-grid>

<h2>Tables</h2>

<onyks-grid cols="4">
    <onyks-card v-for="(count, name) in tables_amounts" :key="name" span="1" :title="name">
        <div class="desc counter">{{ count }}</div>
    </onyks-card>
</onyks-grid>

<h2>Manufacturers</h2>

<onyks-grid cols="4">
    <onyks-card v-for="(count, name) in manufacturers_amounts" :key="name" span="1" :title="name">
        <div class="desc counter">{{ count }}</div>
    </onyks-card>
</onyks-grid>

<h2>Suppliers</h2>

<onyks-grid cols="4">
    <onyks-card v-for="(count, name) in suppliers_amounts" :key="name" span="1" :title="name">
        <div class="desc counter">{{ count }}</div>
    </onyks-card>
</onyks-grid>

</template>

<style lang="css" scoped>
    .counter 
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