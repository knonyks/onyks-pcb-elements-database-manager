<script setup>
    import { ref } from 'vue';
    import { defineExpose } from 'vue';

    const emit = defineEmits(['accept-click'])
    const props = defineProps(['subject'])

    const dialog = ref(null)
    const name = ref('')
    const errorDetails = ref('')

    const open = () => 
    {
        dialog.value.open = true
    };

    const close = () =>
    {
        dialog.value.open = false
    }

    defineExpose({
        open,
        close,
        errorDetails
    });
</script>


<template>
    <onyks-dialog :title="`Add a ${props.subject}`" corner-close bottom-buttons modal ref="dialog">

        <onyks-container type="stack" padding="" gap="l">
            <onyks-text>Enter the name of a new {{ props.subject }} below:</onyks-text>
            <onyks-textfield :placeholder="`Name of a new ${props.subject}`" v-model="name" @input="errorDetails = ''"></onyks-textfield>
            <onyks-text :class="errorDetails === '' ? 'error-invisible' : ''">Error! {{ errorDetails }}</onyks-text>
        </onyks-container>

        <onyks-button background="green" slot="footer" @click="emit('accept-click', name); name = ''" size="m">OK</onyks-button>
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