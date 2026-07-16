<script setup>
    import { element } from '@/utils/api';
    import { ref } from 'vue';
    import { defineProps } from 'vue';
    import { defineEmits } from 'vue';

    const dialog = ref(null)
    const props = defineProps(['items', 'interface'])
    const emit = defineEmits(['delete-end'])

    const open = (parametr) => 
    {
        dialog.value.open = true
    };

    defineExpose(
    {
        open
    });

    const deleteAction = async () =>
    {
        for(let i=0; i<props.items.length; i++)
        {
            await element.delete(props.items[i].uuid)
        }
        dialog.value.open = false
        emit('delete-end')
    }
</script>

<template>
    <onyks-dialog title="Deleting" scroll-target="body" modal corner-close ref="dialog" bottom-buttons>
        <onyks-text size="m">You are deleting {{ props.items.length }} element(s):</onyks-text>

        <onyks-container type="stack" gap="l">
            <onyks-text v-for="item in props.items" size="s">{{ item[props.interface.name] }}</onyks-text>
        </onyks-container>
        
        <onyks-button slot="footer" @click="dialog.open = false">Close</onyks-button>
        <onyks-button slot="footer" @click="deleteAction" background="green">Accept</onyks-button>
    </onyks-dialog>             
</template>

<style scoped>
    onyks-dialog
    {
        position: relative;
        z-index: 20;
    }
</style>