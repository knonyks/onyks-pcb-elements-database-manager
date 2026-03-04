<template>
    <div class="content">
        <slot></slot>
    </div>
</template>

<style scoped>
    .content
    {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-md);
        height: 100%;
    }
</style>