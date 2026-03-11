<script setup>
    import TableButtons from '../TableButtons.vue';
    import TableCounter from '../TableCounter.vue';
    import TableTitle from './TableTitle.vue';
    import { ref, reactive, onMounted} from 'vue';
    import { api_call, db_inifnite_scroll_query} from '@/utils/database';

    const add_supplier_dialog = reactive(
    {
        opened: false,
        error_message: "Undefined error!",
        is_error_message_active: false,
        textfield: "",
        ok: async () => 
        {
            const response = await api_call('/api/suppliers/create', "POST", {name: add_supplier_dialog.textfield})
            switch(response.status)
            {
                case 201:
                    add_supplier_dialog.cancel()
                    suppliers_table.value.update({has_more: true, next_cursor: null})
                    break;
                case 409:
                    add_supplier_dialog.error_message = "The entered supplier is already exsist."
                    add_supplier_dialog.is_error_message_active = true
                    break;
                case 422:
                    add_supplier_dialog.error_message = "The wrong format of the entered name."
                    add_supplier_dialog.is_error_message_active = true
                    break;
                default:
                    add_supplier_dialog.error_message = "Undefined error."
                    add_supplier_dialog.is_error_message_active = true
                    break;
            }  
        },
        cancel: () => {
            add_supplier_dialog.error_message = "Undefined error!"
            add_supplier_dialog.is_error_message_active = false
            add_supplier_dialog.textfield = ""
            add_supplier_dialog.opened = false
        },
        input(e)
        {
            add_supplier_dialog.is_error_message_active = false
        }
    })

    const suppliers_table = ref({
        next_cursor: null, 
        total: 0,
        limit: 20,
        items: [],
        has_more: true,
        async update(options = {},)
        {
            if(options)
            {
                if (options.next_cursor !== undefined) 
                {
                    suppliers_table.value.next_cursor = options.next_cursor;
                }

                if (options.has_more !== undefined) 
                {
                    suppliers_table.value.has_more = options.has_more;
                }

                if (options.total !== undefined && options.total !== null) 
                {
                    suppliers_table.value.total = options.total;
                }
            }
        
            if(suppliers_table.value.has_more)
            {
                let data = await db_inifnite_scroll_query("/api/suppliers/", {limit: suppliers_table.value.limit, cursor: suppliers_table.value.next_cursor});
                if(data.status == 200)
                {
                    if(suppliers_table.value.next_cursor != null)
                    {
                        suppliers_table.value.items.push(...data.data.items)
                    }
                    else
                    {
                        suppliers_table.value.items = data.data.items
                    }
                    suppliers_table.value.next_cursor = data.data.next_cursor
                    if (data.data.total !== undefined && data.data.total !== null) 
                    {
                        suppliers_table.value.total = data.data.total;
                    }
                    suppliers_table.value.has_more = data.data.has_more
                }
            }
        },

        async scroll_end()
        {
            suppliers_table.value.update()
        }
    });

    onMounted(async () =>
    {
        suppliers_table.value.update()
    })

</script>       

<template>

    <!-- ADD SUPPLIER -->
    <onyks-dialog has-title="true" title="Add a new supplier" modal id="add_supplier_dialog" :opened="add_supplier_dialog.opened">
        <onyks-dialog-content>
            <p>Enter the name of a new supplier below:</p>
            <onyks-textfield @input="add_supplier_dialog.input" size="l" v-model="add_supplier_dialog.textfield"></onyks-textfield>
            <onyks-text-help size="md" :class="{hide: !add_supplier_dialog.is_error_message_active }">{{ add_supplier_dialog.error_message }}</onyks-text-help>
        </onyks-dialog-content>
        <onyks-button slot="footer" background="green" @click="add_supplier_dialog.ok">OK</onyks-button>
        <onyks-button slot="footer" background="red" @click="add_supplier_dialog.cancel">Cancel</onyks-button>
    </onyks-dialog>

    <!-- EDIT SUPPLIER -->
    <!-- <onyks-dialog has-title="true" title="Edit a new supplier" modal id="edit_supplier_dialog">
        <onyks-dialog-content>
            <p>Enter a new name of the supplier</p>
            <onyks-textfield size="l"></onyks-textfield>
            <onyks-text-help size="md">Error!</onyks-text-help>
        </onyks-dialog-content>
        <onyks-button slot="footer" background="green">OK</onyks-button>
        <onyks-button slot="footer" background="red">Cancel</onyks-button>
    </onyks-dialog> -->


    <!-- DELETE SUPPLIER -->
    <!-- <onyks-dialog has-title="true" title="Delete the supplier" modal id="delete_supplier_dialog" opened>
        <onyks-dialog-content>
            
            <div style="font-size: var(--size-xl);">Supplier</div>
            <p>Are you sure you want to delete:</p>
            <onyks-text-help size="md">Error!</onyks-text-help>
        </onyks-dialog-content>
        <onyks-button slot="footer" background="green">OK</onyks-button>
        <onyks-button slot="footer" background="red">Cancel</onyks-button>
    </onyks-dialog> -->

    <main>
        <table-title>Suppliers</table-title>
        <table-buttons>
            <onyks-button background="green" size="l" @click="add_supplier_dialog.opened = true">Add</onyks-button>
            <onyks-button background="blue" size="l" disabled>Edit</onyks-button>
            <onyks-button background="red" size="l" disabled>Delete</onyks-button>
        </table-buttons>
        <!-- <table-search placeholder="Search for a supplier!"></table-search> -->
        <table-counter :index="suppliers_table.items.length" :max="suppliers_table.total"></table-counter>
        <onyks-table @scroll-end="suppliers_table.scroll_end" id="table">
            <onyks-row header>
                <onyks-col checkbox></onyks-col>
                <onyks-col>Name</onyks-col>
            </onyks-row>
            <onyks-row v-for="supplier in suppliers_table.items" :key="supplier.id">
                <onyks-col checkbox></onyks-col>
                <onyks-col>{{ supplier.name }}</onyks-col>
            </onyks-row>
        </onyks-table>
    </main>
</template>

<style scoped>
    main
    {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-lg);
    }

    p
    {
        padding: 0;
        margin: 0;
        font-size: var(--size-md);
        /* text-align: justify; */
    }

    onyks-dialog-content
    {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-md);
    }

    onyks-table
    {
        height: 450px;
    }

    onyks-dialog > onyks-button
    {
        width: 100px;
    }

    onyks-dialog-content > onyks-textfield
    {
        width: 100%;
    }

    onyks-text-help.hide
    {
        visibility: hidden;
    }
</style>    