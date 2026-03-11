<script setup>


</script>

<template>
    <div class="container">
        <slot></slot>
    </div>
</template>

<style scoped>
    .container
    {
        display: flex;
        flex-direction: row;
        gap: var(--spacing-md);
        width: 100%;
    }

    :slotted(onyks-button)
    {
        min-width: 150px;
    }

    @media screen and (max-width: 550px)
    {
        :slotted(onyks-button)
        {
            width: 100%;
        }

        .container
        {

            flex-direction: column;
        }
    }
</style>