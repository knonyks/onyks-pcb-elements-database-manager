<script setup lang="js">
    import {onMounted, ref} from 'vue';
    const props = defineProps(['title', 'columns', 'update']);

    const data = ref([])
    const index = ref(0)
    const maxIndex = ref(0)
    const total = ref(0);

    const page_changed = async (e) =>
    {
        let result = (await props.update(e.detail.index, 50))
        console.log(result)
        data.value = result.data.data
        index.value = result.data.meta.current_page
        maxIndex.value = result.data.meta.total_pages
        total.value = result.data.meta.total_records
        console.log(data.value.length)
    }

    onMounted(async () => 
    {
        let result = (await props.update(1, 50))
        console.log(result)
        data.value = result.data.data
        index.value = result.data.meta.current_page
        maxIndex.value = result.data.meta.total_pages
        total.value = result.data.meta.total_records
        console.log(data.value.length)
    })
</script>

<template>
    <h4>Total: {{ total }}</h4>
    <onyks-table :data="data" :columns.prop="props.columns"></onyks-table>
    <onyks-pagination-nav maxView="4" :index="index" @page-changed="page_changed" :maxIndex="maxIndex"></onyks-pagination-nav>
</template>

<style lang="css">
    onyks-table
    {
        height: 400px;
    }

    onyks-pagination-nav
    {
        margin: 0 auto 0 auto;
    }
</style>