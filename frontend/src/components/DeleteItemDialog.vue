<script setup>
    import { ref } from 'vue'

    const props = defineProps(['action', 'formater', 'subject', 'processor'])
    const emit = defineEmits(['success'])
    
    const dialog = ref(null)
    const error = ref('')
    const items = ref([])

    const open = (a) => 
    {
        items.value = a
        console.log(items.value)
        error.value = ''
        dialog.value.open = true
    }

    const close = () =>
    {
        dialog.value.open = false
    }

    const action = async () =>
    {
        for(let i=0; i<items.value.length; i++)
        {
            await props.action(props.processor(items.value[i]))
        }
        dialog.value.open = false
        emit('success')
    }

    defineExpose({
        open,
        close
    });
</script>

<template>
    <onyks-dialog :title="`Deleting`" corner-close bottom-buttons modal ref="dialog">
        
        <onyks-container type="stack" padding="" gap="l">
            <slot name="top"></slot>
            <onyks-text>You are deleting {{ items.length }} {{ props.subject }}:</onyks-text>
                <onyks-container type="stack" gap="l">
                    <onyks-text v-for="item in items" size="s">{{ props.formater(item) }}</onyks-text>
                </onyks-container>
            <onyks-text :class="error === '' ? 'error-invisible' : ''">{{ error }}</onyks-text>
        </onyks-container>
        <onyks-button background="green" slot="footer" @click="action" size="m">OK</onyks-button>
        <onyks-button background="red" slot="footer" @click="dialog.open = false">Close</onyks-button>
    </onyks-dialog>
</template>

<style lang="css" scoped>
    onyks-textfield
    {
        width: 100%;
    }

    .error-invisible
    {
        visibility: hidden;
    }

    onyks-dialog
    {
        position: fixed;
    }

    onyks-dialog
    {
        position: fixed;
    }
</style>