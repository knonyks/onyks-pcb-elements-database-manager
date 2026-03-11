<script setup>
    import TableButtons from '../TableButtons.vue';
    import TableCounter from '../TableCounter.vue';
    import TableTitle from './TableTitle.vue';
    import { ref, reactive, onMounted} from 'vue';
    import { api_call, db_inifnite_scroll_query} from '@/utils/database';

    const add_manufacturer_dialog = reactive(
    {
        opened: false,
        error_message: "Undefined error!",
        is_error_message_active: false,
        textfield: "",
        ok: async () => 
        {
            const response = await api_call('/api/manufacturers/create', "POST", {name: add_manufacturer_dialog.textfield})
            switch(response.status)
            {
                case 201:
                    add_manufacturer_dialog.cancel()
                    manufacturers_table.value.update({has_more: true, next_cursor: null})
                    break;
                case 409:
                    add_manufacturer_dialog.error_message = "The entered manufacturer is already exsist."
                    add_manufacturer_dialog.is_error_message_active = true
                    break;
                case 422:
                    add_manufacturer_dialog.error_message = "The wrong format of the entered name."
                    add_manufacturer_dialog.is_error_message_active = true
                    break;
                default:
                    add_manufacturer_dialog.error_message = "Undefined error."
                    add_manufacturer_dialog.is_error_message_active = true
                    break;
            }  
        },
        cancel: () => {
            add_manufacturer_dialog.error_message = "Undefined error!"
            add_manufacturer_dialog.is_error_message_active = false
            add_manufacturer_dialog.textfield = ""
            add_manufacturer_dialog.opened = false
        },
        input(e)
        {
            add_manufacturer_dialog.is_error_message_active = false
        }
    })

    const manufacturers_table = ref({
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
                    manufacturers_table.value.next_cursor = options.next_cursor;
                }

                if (options.has_more !== undefined) 
                {
                    manufacturers_table.value.has_more = options.has_more;
                }

                if (options.total !== undefined && options.total !== null) 
                {
                    manufacturers_table.value.total = options.total;
                }
            }
        
            if(manufacturers_table.value.has_more)
            {
                let data = await db_inifnite_scroll_query("/api/manufacturers/", {limit: manufacturers_table.value.limit, cursor: manufacturers_table.value.next_cursor});
                if(data.status == 200)
                {
                    if(manufacturers_table.value.next_cursor != null)
                    {
                        manufacturers_table.value.items.push(...data.data.items)
                    }
                    else
                    {
                        manufacturers_table.value.items = data.data.items
                    }
                    manufacturers_table.value.next_cursor = data.data.next_cursor
                    if (data.data.total !== undefined && data.data.total !== null) 
                    {
                        manufacturers_table.value.total = data.data.total;
                    }
                    manufacturers_table.value.has_more = data.data.has_more
                }
            }
        },

        async scroll_end()
        {
            manufacturers_table.value.update()
        }
    });

    onMounted(async () =>
    {
        manufacturers_table.value.update()
    })

</script>       

<template>

    <!-- ADD -->
    <onyks-dialog has-title="true" title="Add a new manufacturer" modal id="add_manufacturer_dialog" :opened="add_manufacturer_dialog.opened">
        <onyks-dialog-content>
            <p>Enter the name of a new manufacturer below:</p>
            <onyks-textfield @input="add_manufacturer_dialog.input" size="l" v-model="add_manufacturer_dialog.textfield"></onyks-textfield>
            <onyks-text-help size="md" :class="{hide: !add_manufacturer_dialog.is_error_message_active }">{{ add_manufacturer_dialog.error_message }}</onyks-text-help>
        </onyks-dialog-content>
        <onyks-button slot="footer" background="green" @click="add_manufacturer_dialog.ok">OK</onyks-button>
        <onyks-button slot="footer" background="red" @click="add_manufacturer_dialog.cancel">Cancel</onyks-button>
    </onyks-dialog>

    <main>
        <table-title>Manufacturers</table-title>
        <table-buttons>
            <onyks-button background="green" size="l" @click="add_manufacturer_dialog.opened = true">Add</onyks-button>
            <onyks-button background="blue" size="l" disabled>Edit</onyks-button>
            <onyks-button background="red" size="l" disabled>Delete</onyks-button>
        </table-buttons>
        <!-- <table-search placeholder="Search for a manufacturer!"></table-search> -->
        <table-counter :index="manufacturers_table.items.length" :max="manufacturers_table.total"></table-counter>
        <onyks-table @scroll-end="manufacturers_table.scroll_end" id="table">
            <onyks-row header>
                <onyks-col checkbox></onyks-col>
                <onyks-col>Name</onyks-col>
            </onyks-row>
            <onyks-row v-for="manufacturer in manufacturers_table.items" :key="manufacturer.id">
                <onyks-col checkbox></onyks-col>
                <onyks-col>{{ manufacturer.name }}</onyks-col>
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