<script setup>
    import { manufacturer } from '@/utils/api';
import { ref } from 'vue';
    import { defineExpose } from 'vue';

    const emit = defineEmits(['success'])
    const props = defineProps(['subject', 'action', 'current-name', 'id'])
    const name = ref('')
    const dialog = ref(null)
    const error = ref('')

    const open = () => 
    {
        name.value = props.currentName
        error.value = ''
        dialog.value.open = true
    }

    const close = () =>
    {
        dialog.value.open = false
    }

    const action = async () =>
    {
        let data = await props.action(props.id, {name: name.value})
       
        if(data.status == 200)
        {
            dialog.value.open = false
            emit('success')
        }
        else
        {
            error.value = data.response.data.detail
        }
    }

    defineExpose({
        open,
        close,
        error
    });
</script>

<template>

    <onyks-dialog :title="`Edit a ${props.subject}`" corner-close bottom-buttons modal ref="dialog">
        <onyks-container type="stack" padding="" gap="l">
            <onyks-text>You are editing {{ props.currentName }}.</onyks-text>
            <onyks-text>Enter a new name of the {{ props.subject }} below:</onyks-text>
            <onyks-textfield :placeholder="`New name of the ${props.subject}`" v-model="name" @input="error = ''"></onyks-textfield>
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
</style>