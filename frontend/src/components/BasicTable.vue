<script setup lang="js">
    import {onMounted, ref} from 'vue';
    
    const props = defineProps(['title', 'columns', 'update']); 
    const emit = defineEmits(['checkbox-change']);

    const data = ref([])
    const index = ref(0)
    const maxIndex = ref(0)
    const total = ref(0);
    const table = ref(null)

    const page_changed = async (e) =>
    {
        let result = (await props.update(e.detail.index, 50))
        data.value = result.data.data
        index.value = result.data.meta.current_page
        maxIndex.value = result.data.meta.total_pages
        total.value = result.data.meta.total_records
        emit('checkbox-change', []);
    }

    onMounted(async () => 
    {
        reset()
    })

    const checkbox_change = (e) =>
    {
        emit('checkbox-change', table.value.getTableData());
    }

    const reset = async (e) =>
    {
        let result = (await props.update(1, 50))
        data.value = result.data.data
        index.value = result.data.meta.current_page
        maxIndex.value = result.data.meta.total_pages
        total.value = result.data.meta.total_records
    }

    defineExpose({reset})
</script>

<template>
    <h4>Total: {{ total }}</h4>
    <onyks-table ref="table" :data="data" :columns.prop="props.columns" @checkbox-change="checkbox_change"></onyks-table>
    <onyks-pagination-nav maxView="4" :index="index" @page-changed="page_changed" :maxIndex="maxIndex"></onyks-pagination-nav>
</template>

<style lang="css">
    onyks-table
    {
        height: 400px;
        z-index: 0;
    }

    onyks-pagination-nav
    {
        margin: 0 auto 0 auto;
    }
</style>