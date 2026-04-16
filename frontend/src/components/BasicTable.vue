<script setup lang="ts">
    import PageContent from './PageContent.vue';
    import {ref} from 'vue';
    const props = defineProps(['title', 'data', 'columns', 'breakpoint']);
</script>

<template>
    <PageContent>
        <h2>{{ title }}</h2>
        <h4>Displaying {{ props.data.length }} of Y</h4>
        <div class="buttons">
            <slot name="buttons"></slot>
        </div>
        <onyks-table :data="props.data" :columns.prop="props.columns"></onyks-table>
    </PageContent>
</template>

<style lang="css">

    onyks-table
    {
        height: 400px;
    }

    .buttons
    {
        display: grid;
        grid-template-columns: repeat(3, 150px);
        grid-column-gap: var(--spacing-md);
        grid-row-gap:  var(--spacing-md);
    }

    .buttons > onyks-button 
    {
        min-width: 120px;
    }
</style>