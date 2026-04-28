<script setup>
    import { ref, onMounted, onUnmounted } from 'vue';

    const props = defineProps({
        maxWidth: 
        {
            type: Number,
            default: 800
        }
    });

    const isSingleColumn = ref(false);

    const checkWidth = () => 
    {
        isSingleColumn.value = window.innerWidth <= props.maxWidth;
    };

    onMounted(() => 
    {
        checkWidth();
        window.addEventListener('resize', checkWidth);
    });

    onUnmounted(() => {
        window.removeEventListener('resize', checkWidth);
    });
</script>

<template>
    <div class="grid-container" :class="{ 'single-column': isSingleColumn }">
        <slot></slot>
    </div>
</template>

<style scoped>
    .grid-container 
    {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 150px));
        gap: var(--spacing-md, 15px);
        width: 100%;
    }

    .grid-container.single-column 
    {
        grid-template-columns: 1fr; 
    }

    :slotted(*) 
    {
        width: 100%;
    }
</style>