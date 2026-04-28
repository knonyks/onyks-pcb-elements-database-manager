<script setup lang="js">
    import { api_manufacturer_create } from '@/utils/api';
    import { ui_toast } from '@/utils/ui';
    import { ref } from 'vue';

    const props = defineProps(['title', 'opened'])
    const emit = defineEmits(['close'])
    
    const value = ref('')
    const dialog = ref(null)
    const error_text = ref('')


    const add_btn_event = async () =>
    {
        try
        {
            let x = await api_manufacturer_create(value.value)
            dialog.value.opened = false;
            emit('close')
            error_text.value = ""
            ui_toast("Item added successfully!", "success");
        }
        catch(e)
        {
            switch(e.status)
            {
                case 201:
                    break;
                case 409:
                    error_text.value = "The entered manufacturer is already exsist."
                    break;
                case 422:
                    error_text.value = "The wrong format of the entered name."
                    break;
                default:
                    error_text.value = "Undefined error."
                    break;
            }   
        }
    }

    const open = (flag) => 
    {
        console.log('xx')
        dialog.value.opened = flag
    }

    const input_event = (event) => 
    {
        value.value = event.target.value
        error_text.value = ""
    }

    defineExpose({open})
</script>

<template>
    <onyks-dialog ref="dialog" has-title="true" :title="`Creating a new ${props.title}`" corner-close modal size="m" @keyup.enter="add_btn_event">
        <onyks-dialog-content>
            <h3>Enter a name</h3>
            <onyks-textfield size="m" :value="value" @input="input_event" placeholder="Enter a name"></onyks-textfield>
            <onyks-text-help size="m" color="red">{{ error_text }}</onyks-text-help>
        </onyks-dialog-content>

        <onyks-button slot="footer" background="green" @click="add_btn_event">OK</onyks-button>
        <onyks-button slot="footer" background="red" @click="dialog.opened = false">Cancel</onyks-button>
    </onyks-dialog>
</template>

<style>
    onyks-dialog
    {
        z-index: 999999;
    }

    onyks-dialog-content
    {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-md);
    }

    onyks-textfield
    {
        width: 100%;
    }

    onyks-button
    {
        width: 100px;
    }
</style>