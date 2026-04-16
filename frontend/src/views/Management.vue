<script setup>
    import BasicTable from '@/components/BasicTable.vue';
    import PageContent from '@/components/PageContent.vue';
    import Warning from '@/components/Warning.vue';
    import { ref } from 'vue';
    import { api_call } from '../utils/api';
    import { ui_toast } from '@/utils/ui';
    import { db_inifnite_scroll_query } from '@/utils/database';

    const add_current_item = ref('supplier');
    const add_current_item_error_text = ref('');
    const add_dialog = ref(null);
    const add_current_item_name = ref('');

    const suppliers_data = ref([
        { selected: false, id: 1, name: "Dostawca 1", createdAt: '13.03.2023 14:00' },
        { selected: true,  id: 2, name: "Dostawca 2",  createdAt: '13.03.2023 14:00' },
        { selected: false, id: 3, name: "Dostawca 3", createdAt: '13.03.2023 14:00' }
    ]);
    
    const suppliers_columns = ref([{ key: 'selected', label: 'Wybierz' },
        { key: 'id', label: 'ID' },
        { key: 'name', label: 'Nazwa' },
        { key: 'createdAt', label: 'Data utworzenia' }
    ]);

    const manufacturers_data = ref([
        { selected: false, id: 1, name: "Dostawca 1", createdAt: '13.03.2023 14:00' },
        { selected: true,  id: 2, name: "Dostawca 2",  createdAt: '13.03.2023 14:00' },
        { selected: false, id: 3, name: "Dostawca 3", createdAt: '13.03.2023 14:00' }
    ]);
    
    const manufacturers_columns = ref([{ key: 'selected', label: 'Wybierz' },
        { key: 'id', label: 'ID' },
        { key: 'name', label: 'Nazwa' },
        { key: 'createdAt', label: 'Data utworzenia' }
    ]);

    const add_supplier_button_clicked = () => 
    {
        add_current_item.value = 'supplier';
        add_dialog.value.opened = true;
        add_current_item_name.value = "";
        add_current_item_error_text.value = "";
    };

    console.log(db_inifnite_scroll_query("/api/manufacturers/", {limit: 50, cursor: null}))













    const remove_supplier_button_clicked = () => 
    {
        console.log('Remove supplier button clicked');
    };

    const edit_supplier_button_clicked = () => 
    {
        console.log('Edit supplier button clicked');
    };

    const add_manufacturer_button_clicked = () => 
    {
        add_current_item.value = 'supplier';
        add_dialog.value.opened = true;
        add_current_item_name.value = "";
        add_current_item_error_text.value = "";
    };

    const remove_manufacturer_button_clicked = () => 
    {
        console.log('Remove manufacturer button clicked');
    };

    const edit_manufacturer_button_clicked = () => 
    {
        console.log('Edit manufacturer button clicked');
    };


    const add_item = async () => 
    {
        if(add_current_item_name.value.trim() === "")
        {
            add_current_item_error_text.value = "Name cannot be empty";
            return;
        }
        let query = '/api/' + (add_current_item.value === 'supplier'? 'suppliers':'manufacturers') + '/create';
        const response = await api_call(query, "POST", {name: add_current_item_name.value});

        switch(response.status)
        {
            case 201:
                add_dialog.value.opened = false;
                ui_toast("Item added successfully!", "success");
                // manufacturers_table.value.update({has_more: true, next_cursor: null})
                break;
            case 409:
                add_current_item_error_text.value = "The entered manufacturer is already exsist."
                add_dialog.value.opened = true
                break;
            case 422:
                add_current_item_error_text.value = "The wrong format of the entered name."
                add_dialog.value.opened = true
                break;
            default:
                add_current_item_error_text.value = "Undefined error."
                add_dialog.value.opened = true
                break;
        }
    };

</script>

<template>
    <PageContent>
        <h1>Management</h1>
        <Warning/>
        <BasicTable title="Suppliers" :data="suppliers_data" :columns="suppliers_columns">
            <template #buttons>
                <onyks-button @click="add_supplier_button_clicked" background="green">Add</onyks-button>
                <onyks-button @click="remove_supplier_button_clicked" disabled>Remove</onyks-button>
                <onyks-button @click="edit_supplier_button_clicked" background="blue" disabled>Edit</onyks-button>
            </template>
        </BasicTable>
        <BasicTable title="Manufacturers" :data="manufacturers_data" :columns="manufacturers_columns">
            <template #buttons>
                <onyks-button @click="add_manufacturer_button_clicked" background="green">Add</onyks-button>
                <onyks-button @click="remove_manufacturer_button_clicked" disabled>Remove</onyks-button>
                <onyks-button @click="edit_manufacturer_button_clicked" background="blue" disabled>Edit</onyks-button>
            </template>
        </BasicTable>

        <onyks-dialog ref="add_dialog" has-title="true" :title="`Creating a new ${add_current_item}`" corner-close modal size="m">
            <onyks-dialog-content>
                <h3>Enter a name</h3>
                <onyks-textfield size="m" :value="add_current_item_name" 
                @input="event => add_current_item_name = event.target.value" placeholder="Enter a name"></onyks-textfield>
                <onyks-text-help size="m" color="red">{{ add_current_item_error_text }}</onyks-text-help>
            </onyks-dialog-content>
            <onyks-button slot="footer" background="green" @click="add_item">OK</onyks-button>
            <onyks-button slot="footer" background="red" @click="add_dialog.opened = false">Cancel</onyks-button>
        </onyks-dialog>

    </PageContent>
</template>

<style scoped>
    onyks-dialog > onyks-button
    {
        min-width: 120px;
    }

    onyks-dialog-content > onyks-textfield
    {
        width: 100%;
    }

    onyks-dialog-content
    {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-md);
    }
</style>