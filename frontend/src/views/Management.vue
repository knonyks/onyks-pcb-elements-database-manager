<script setup>
    import BasicTable from '@/components/BasicTable.vue';
    import PageContent from '@/components/PageContent.vue';
    import Warning from '@/components/Warning.vue';
    import { reactive, ref } from 'vue';
    import { api_call } from '../utils/api';
    import { ui_toast } from '@/utils/ui';
    import { db_get_list } from '@/utils/database';
    import { DateTime } from "luxon";

    const manufacturers = reactive(
    {
        data: [],
        columns: [{ key: 'selected', label: 'Select' },
        { key: 'id', label: 'ID' },
        { key: 'name', label: 'Name' },
        { key: 'created_at', label: 'Created' }],
        total: 0,
        has_more: false,
        next_cursor: null,
        init()
        {
            db_get_list("/api/manufacturers/", {limit: 50, cursor: null}).then(response => 
            {
                if (response.status === 200) 
                {
                    this.data = manufacturers_suppliers_process_data(response.data.items);
                    this.has_more = response.data.has_more
                    this.next_cursor = response.data.next_cursor
                }
            })
            api_call('/api/manufacturers/total').then(response => 
            {
                this.total = response.status == 200? response.data.total:0
            })
        }
    })

    const suppliers = reactive(
    {
        data: [],
        columns: [{ key: 'selected', label: 'Select' },
        { key: 'id', label: 'ID' },
        { key: 'name', label: 'Name' },
        { key: 'created_at', label: 'Created' }],
        total: 0,
        has_more: false,
        next_cursor: null,
        init()
        {
            db_get_list("/api/suppliers/", {limit: 50, cursor: null}).then(response => 
            {
                if (response.status === 200) 
                {
                    this.data = manufacturers_suppliers_process_data(response.data.items);
                    this.has_more = response.data.has_more
                    this.next_cursor = response.data.next_cursor
                }
            })
            api_call('/api/suppliers/total').then(response => 
            {
                this.total = response.status == 200? response.data.total:0
            })
        }
    })

    const manufacturers_suppliers_process_data = (items) => 
    {
        return items.map(item => 
        {
            let formatted_date = "None"; 

            if (item.created_at) 
            {
                formatted_date = DateTime.fromISO(item.created_at, { zone: 'utc' })
                .setZone("Europe/Warsaw")
                .toFormat("dd.MM.yyyy, HH:mm");
            }

            return {
                ...item,
                selected: false,
                created_at: formatted_date
            };
        });
    }

    manufacturers.init()
    suppliers.init()

    const adding_dialog = ref(null);
    const adding_current_table = ref("");
    const adding_current_name = ref("")
    const adding_error_message = ref("")
    const adding_open_dialog = (val) =>
    {
        if(val == 'manufacturer')
        {
            adding_current_name.value = ""
            adding_current_table.value = 'manufacturer'
            adding_error_message.value = ''
        }
        else
        {
            adding_current_name.value = ""
            adding_current_table.value = 'supplier'
            adding_error_message.value = ''
        }
        adding_dialog.value.opened = true
    }

    const adding_ok = () =>
    {
        if(adding_current_name.value.trim() === "")
        {
            adding_error_message.value = "Name cannot be empty";
            return;
        }

        let query = '/api/' + (adding_current_table.value == 'manufacturer'? 'manufacturers':'suppliers') + '/';

        api_call(query + 'create', "POST", {name: adding_current_name.value}).then((response) => 
        {
            switch(response.status)
            {
                case 201:
                    adding_dialog.value.opened = false;
                    ui_toast("Item added successfully!", "success");
                    db_get_list(query, {limit: 50, cursor: null}).then(response => 
                    {
                        console.log(response)
                        if (response.status === 200) 
                        {
                            if(adding_current_table.value == 'manufacturer')
                            {
                                manufacturers.data = manufacturers_suppliers_process_data(response.data.items);
                            }
                            else
                            {
                                suppliers.data = manufacturers_suppliers_process_data(response.data.items);
                            }
                        }
                    })
                    api_call(query + 'total').then(response => 
                    {
                        if(adding_current_table.value == 'manufacturer')
                        {
                            manufacturers.total = response.status == 200? response.data.total:0
                        }
                        else
                        {
                            suppliers.total = response.status == 200? response.data.total:0
                        }
                    })
                    break;
                case 409:
                    adding_error_message.value = "The entered manufacturer is already exsist."
                    adding_dialog.value.opened = true
                    break;
                case 422:
                    adding_error_message.value = "The wrong format of the entered name."
                    adding_dialog.value.opened = true
                    break;
                default:
                    adding_error_message.value = "Undefined error."
                    adding_dialog.value.opened = true
                    break;
            }
        })
        .catch((err) =>
        {});  
    }

    


    // const adding = reactive({
    //     current_table: "xxx",
    //     current_name: "xxx",
    //     error: "xxx",
    //     open_dialog()
    //     {
    //         this.current_table = 'supplier';
    //         adding_dialog.value.opened = true;
    //         this.current_name = "xxx";
    //         this.error = "xxx";
    //     }
    // })


    // const add_current_item = ref('');
    // const add_current_item_error_text = ref('');
    // const add_dialog = ref(null);
    // const add_current_item_name = ref('');

    // const suppliers_data = ref([
    //     // { selected: false, id: 1, name: "Dostawca 1", created_at: '13.03.2023 14:00' },
    //     // { selected: true,  id: 2, name: "Dostawca 2",  created_at: '13.03.2023 14:00' },
    //     // { selected: false, id: 3, name: "Dostawca 3", created_at: '13.03.2023 14:00' }
    // ]);
    
    // const suppliers_columns = ref([{ key: 'selected', label: 'Wybierz' },
    //     { key: 'id', label: 'ID' },
    //     { key: 'name', label: 'Name' },
    //     { key: 'created_at', label: 'Created' }
    // ]);

    // const manufacturers_data = ref([
    //     // { selected: false, id: 1, name: "Dostawca 1", created_at: '13.03.2023 14:00' },
    //     // { selected: true,  id: 2, name: "Dostawca 2",  created_at: '13.03.2023 14:00' },
    //     // { selected: false, id: 3, name: "Dostawca 3", created_at: '13.03.2023 14:00' }
    // ]);
    
    // const manufacturers_columns = ref([{ key: 'selected', label: 'Wybierz' },
    //     { key: 'id', label: 'ID' },
    //     { key: 'name', label: 'Name' },
    //     { key: 'created_at', label: 'Created' }
    // ]);

    // const add_supplier_button_clicked = () => 
    // {
    //     add_current_item.value = 'supplier';
    //     add_dialog.value.opened = true;
    //     add_current_item_name.value = "";
    //     add_current_item_error_text.value = "";
    // };

    // db_get_list("/api/manufacturers/", {limit: 50, cursor: null}).then(response => 
    // {
    //     if (response.status === 200) 
    //     {
    //         manufacturers_data.value = manufacturers_suppliers_process_data(response.data.items);
    //     }
    // })









    // const remove_supplier_button_clicked = () => 
    // {
    //     console.log('Remove supplier button clicked');
    // };

    // const edit_supplier_button_clicked = () => 
    // {
    //     console.log('Edit supplier button clicked');
    // };

    // const add_manufacturer_button_clicked = () => 
    // {
    //     add_current_item.value = 'manufacturer';
    //     add_dialog.value.opened = true;
    //     add_current_item_name.value = "";
    //     add_current_item_error_text.value = "";
    // };

    // const remove_manufacturer_button_clicked = () => 
    // {
    //     console.log('Remove manufacturer button clicked');
    // };

    // const edit_manufacturer_button_clicked = () => 
    // {
    //     console.log('Edit manufacturer button clicked');
    // };


    // const add_item = async () => 
    // {
    //     if(add_current_item_name.value.trim() === "")
    //     {
    //         add_current_item_error_text.value = "Name cannot be empty";
    //         return;
    //     }
    //     let query = '/api/' + (add_current_item.value === 'supplier'? 'suppliers':'manufacturers') + '/create';
    //     const response = await api_call(query, "POST", {name: add_current_item_name.value});

    //     switch(response.status)
    //     {
    //         case 201:
    //             add_dialog.value.opened = false;
    //             ui_toast("Item added successfully!", "success");
    //             db_get_list("/api/manufacturers/", {limit: 50, cursor: null}).then(response => 
    //             {
    //                 if (response.status === 200) 
    //                 {
    //                     manufacturers_data.value = manufacturers_suppliers_process_data(response.data.items);
    //                 }
    //             })
    //             break;
    //         case 409:
    //             add_current_item_error_text.value = "The entered manufacturer is already exsist."
    //             add_dialog.value.opened = true
    //             break;
    //         case 422:
    //             add_current_item_error_text.value = "The wrong format of the entered name."
    //             add_dialog.value.opened = true
    //             break;
    //         default:
    //             add_current_item_error_text.value = "Undefined error."
    //             add_dialog.value.opened = true
    //             break;
    //     }
    // };
</script>

<template>
    <PageContent>
        <h1>Management</h1>
        <Warning/>

        <BasicTable title="Manufacturers" :data="manufacturers.data" :columns="manufacturers.columns" :total="manufacturers.total" :scroll_end="console.log">
            <template #buttons>
                <onyks-button @click="adding_open_dialog('manufacturer')" background="green">Add</onyks-button>
                <!-- <onyks-button @click="remove_manufacturer_button_clicked" disabled>Remove</onyks-button>
                <onyks-button @click="edit_manufacturer_button_clicked" background="blue" disabled>Edit</onyks-button> -->
            </template>
        </BasicTable>

        <BasicTable title="Suppliers" :data="suppliers.data" :columns="suppliers.columns" :total="suppliers.total" :scroll_end="console.log(e)">
            <template #buttons>
                <onyks-button @click="adding_open_dialog('supplier')" background="green">Add</onyks-button>
                <!-- <onyks-button @click="remove_supplier_button_clicked" disabled>Remove</onyks-button>
                <onyks-button @click="edit_supplier_button_clicked" background="blue" disabled>Edit</onyks-button> -->
            </template>
        </BasicTable>
        
        <onyks-dialog ref="adding_dialog" has-title="true" :title="`Creating a new ${adding_current_table}`" corner-close modal size="m">
            <onyks-dialog-content>
                <h3>Enter a name</h3>
                <onyks-textfield size="m" :value="adding_current_name" 
                @input="event => adding_current_name = event.target.value" placeholder="Name"></onyks-textfield>
                <onyks-text-help size="m" color="red">{{ adding_error_message }}</onyks-text-help>
            </onyks-dialog-content>
            <onyks-button slot="footer" background="green" @click="adding_ok">OK</onyks-button>
            <onyks-button slot="footer" background="red" @click="adding_dialog.opened = false">Cancel</onyks-button>
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