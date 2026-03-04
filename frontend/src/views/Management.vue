<script setup>
    import Panel_Content from '../components/Panel_Content.vue';
    import {onMounted, ref} from 'vue';
    import {api_call} from '@/utils/database';

    // ADD SUPPLIER
    const add_supplier_dialog_error_message = ref("");

    const add_supplier_ok = async () =>
    {
        let value = document.querySelector('#add-supplier-textfield').value
        const response = await api_call('/api/suppliers/create', "POST", {name: value})
        console.log(response.status)
        console.log(response)
        switch(response.status)
        {
            case 201:
                add_supplier_cancel()
                break;
            case 409:
                add_supplier_dialog_error_message.value = "The entered supplier is already exsist."
                break;
            case 422:
                add_supplier_dialog_error_message.value = "The wrong format of the entered name."
                break;
            default:
                add_supplier_dialog_error_message.value = "Undefined error."
                break;
        }  
    }

    const add_supplier_cancel = () =>
    {
        add_supplier_dialog_error_message.value = ""
        document.querySelector('#add-supplier-textfield').value = ""
        document.querySelector('#add-supplier-dialog').opened = false
    }
    
    const add_supplier_input_event = () =>
    {
        add_supplier_dialog_error_message.value = ""
    }

    // EDIT SUPPLIER
    const edit_supplier_name = ref("Example supplier")
    const edit_supplier_dialog_error_message = ref("")

    const edit_supplier_ok = () => 
    {

    }

    const edit_supplier_cancel = () =>
    {
        edit_supplier_dialog_error_message.value = ""
        document.querySelector('#edit-supplier-textfield').value = ""
        document.querySelector('#edit-supplier-dialog').opened = false
    }

    // TABLE
    const suppliers_table = ref({
        next_cursor: 0, 
        total_count: 0,
        suppliers: []
    });


    const update_table = async () => 
    {
        const response = await api_call('/api/suppliers/')
        console.log(response)
        if(response.status == 200)
        {
            suppliers_table.value.next_cursor = response.data.next_cursor;
            suppliers_table.value.total_count = response.data.total_count;
            suppliers_table.value.suppliers = response.data.suppliers;
        }
    }

    onMounted(() =>
    {
        update_table()
        document.querySelector("#suppliers-table").addEventListener("scroll", (event) => 
        { 
            console.log("sss")
        })
    })

</script>

<template>
    <Panel_Content>

       <!-- ADD A SUPPLIER -->
        <onyks-dialog  id="add-supplier-dialog" has-title="true" title="Add a supplier" modal>
            <div class="dialog-content">
                <p>Enter a name of a supplier</p>
                <onyks-textfield size="l" type="text" class="dialog-textfield" id="add-supplier-textfield" @input="add_supplier_input_event"></onyks-textfield>
                <p class="help">{{add_supplier_dialog_error_message}}</p>
            </div>
            <onyks-button class="dialog-btn" slot="footer" background="green" @click="add_supplier_ok">OK</onyks-button>
            <onyks-button class="dialog-btn" slot="footer" background="red" @click="add_supplier_cancel">Cancel</onyks-button>
        </onyks-dialog>

        <!-- EDIT A SUPPLIER -->
        <onyks-dialog  id="edit-supplier-dialog" has-title="true" title="Edit a supplier" modal>
            <div class="dialog-content">
                <p>You are editing the supplier called:</p>
                <h3>{{edit_supplier_name}}</h3>
                <p>Enter a new name of the supplier:</p>
                <onyks-textfield size="l" type="text" class="dialog-textfield" id="edit-supplier-textfield"></onyks-textfield>
                <p class="help">{{edit_supplier_dialog_error_message}}</p>
            </div>
            <onyks-button class="dialog-btn" slot="footer" background="green" @click="edit_supplier_ok">OK</onyks-button>
            <onyks-button class="dialog-btn" slot="footer" background="red" @click="edit_supplier_cancel">Cancel</onyks-button>
        </onyks-dialog>


        <!-- DELTE A SUPPLIER -->
        <!-- <onyks-dialog  id="delete-supplier-dialog" has-title="true" title="Delete the supplier" modal>
            <p class="dialog-p">Are you sure to delete the choosen supplier?</p>
            <h3 class="dialog-p">{{delete_supplier_name}}</h3>
            <onyks-text-help>{{delete_supplier_dialog_error_message}}</onyks-text-help>
            <onyks-button class="dialog-btn" slot="footer" background="green" @click="add_supplier">Yes</onyks-button>
            <onyks-button class="dialog-btn" slot="footer" background="red" onclick="document.querySelector('#add-supplier-dialog').opened = false">Cancel</onyks-button>
        </onyks-dialog> -->




        
        <h1>Suppliers</h1>
        <div id="suppliers-panel">
            <onyks-textfield size="l" type="text" id="suppliers-search"></onyks-textfield>
            <onyks-button size="l" background="green" onclick="document.getElementById('add-supplier-dialog').opened = true" id="add-supplier-btn">Add</onyks-button>
            <onyks-button size="l" background="blue" disabled onclick="document.getElementById('edit-supplier-dialog').opened = true"  id="edit-supplier-btn">Edit</onyks-button>
            <onyks-button size="l" background="red" disabled onclick="document.getElementById('delete-supplier-dialog').opened = true" id="delete-supplier-btn">Delete</onyks-button>
        </div>

        <onyks-table id="suppliers-table">
            <onyks-row header>
                <onyks-col checkbox></onyks-col>
                <onyks-col>ID</onyks-col>
                <onyks-col>Supplier</onyks-col>
                <onyks-col>Created at</onyks-col>
            </onyks-row>
            <onyks-row v-for="supplier in suppliers_table.suppliers" :key="supplier.id">
                <onyks-col checkbox></onyks-col>
                <onyks-col>{{ supplier.id }}</onyks-col>
                <onyks-col>{{ supplier.name }}</onyks-col>
                <onyks-col>{{ supplier.created_at }}</onyks-col>
            </onyks-row>
        </onyks-table>
    </Panel_Content>
</template>

<style scoped>
    onyks-button 
    {
        min-width: 100px;
        height: fit-content;
    }

    h1
    {
        margin: 0;
    }

    p.help
    {
        color: #ff4040;
    }

    onyks-table
    {
        width: 100%;
        height: 450px;
    }

    #suppliers-panel
    {
        display: flex;
        flex-direction: row;
        gap: var(--spacing-md);
        width: 100%;
        height: fit-content;
        flex-wrap: wrap;
    }

    .dialog-p
    {
        margin: 0 0 var(--spacing-lg) 0;
    }

    .dialog-textfield
    {
        width: 100%;
    }

    .dialog-content
    {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-md);
    }

    p
    {
        margin: 0;
    }

    @media screen and (max-width: 700px)
    {
        #suppliers-search
        {
            width: 100%;
        }

        #add-supplier-btn, #edit-supplier-btn, #delete-supplier-btn
        {
            width: 100%;
        }
    }
</style>