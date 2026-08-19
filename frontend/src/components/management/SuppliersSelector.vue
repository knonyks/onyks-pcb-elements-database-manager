<script setup lang="js">
    import { supplier } from '@/utils/api';
    import { ref, onMounted } from 'vue';
    import { useWindowSize } from '@vueuse/core';
    import { defineModel } from 'vue';
    const model = defineModel()
    const items = ref([])
    const { width } = useWindowSize()

    onMounted(async () => 
    {
        let response = await supplier.list()
        items.value = response.data.items
    })
</script>

<template>
    <onyks-container type="grid" :cols="width > 550? 2:1" padding="" gap="l" >
        <onyks-container v-for="item in items" :key="item.id" padding="" gap="l">
            <onyks-text>{{ item.name }}</onyks-text>
            <onyks-textfield v-model="model[item.name]"></onyks-textfield>
        </onyks-container>
    </onyks-container>
    <onyks-container type="grid" cols="3" padding="" gap="m" class="btns">
        <onyks-button background="green">Add</onyks-button>
        <onyks-button background="blue">Edit</onyks-button>
        <onyks-button>Delete</onyks-button>
    </onyks-container>
</template>

<style lang="css" scoped>
    onyks-select
    {
        width: 100%;
        height: 300px;
    }

    onyks-container
    {
        width: 100%;
    }

    onyks-textfield
    {
        width: 100%;
    }

    onyks-button
    {
        max-width: 100%;
    }

    .btns
    {
        max-width: 450px;
        width: 100%;
    }
</style>