<script setup>
    import { element } from '@/utils/api';
    import { ref } from 'vue';
    import { defineProps } from 'vue';
    import { defineEmits } from 'vue';

    const dialog = ref(null)
    const props = defineProps(['interface', 'action'])
    const emit = defineEmits(['delete-end'])
    const items = ref([])


    const open = (parametr) => 
    {
        dialog.value.open = true
    };

    defineExpose(
    {
        open,
        items
    });

    const action = async () =>
    {
        for(let i=0; i<items.value.length; i++)
        {
            await props.action((items.value[i])[props.interface.id])
        }
        dialog.value.open = false
        emit('delete-end')
    }
</script>

<template>
    <onyks-dialog title="Deleting" scroll-target="body" modal corner-close ref="dialog" bottom-buttons>
        <onyks-container type="stack" gap="l" padding="">
            <slot name="footer"></slot>
            <onyks-text size="m">You are deleting {{ items.length }} items:</onyks-text>
            <onyks-container type="stack" gap="l">
                <onyks-text v-for="item in items" size="s">{{ item[interface.name] }}</onyks-text>
            </onyks-container>
        </onyks-container>
        <onyks-button slot="footer" @click="dialog.open = false">Close</onyks-button>
        <onyks-button slot="footer" @click="action" background="green">Accept</onyks-button>
    </onyks-dialog>             
</template>

<style scoped>
    onyks-dialog
    {
        position: relative;
        z-index: 20;
    }
</style>