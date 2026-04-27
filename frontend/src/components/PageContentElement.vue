<template>
    <div class="content">
        <slot></slot>
    </div>
</template>

<style lang="css" scoped>
    .content
    {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-lg);
    }
</style>