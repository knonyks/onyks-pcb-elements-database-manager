<script setup>
    import Panel_Content from '../components/Panel_Content.vue';
    import { Onyks_Button } from 'onyks-web-ui-system';
</script>

<template>
    <Panel_Content>
        <h1>Add a new element</h1>
        <form action="" method="post">
            <div class="form-part">
                <onyks-label size="l" class="left">Part Name</onyks-label>
                <onyks-textfield size="l" placeholder="eg. BC547BBU" class="left"></onyks-textfield>
                <onyks-label size="l" class="left">Manufacturer</onyks-label>
                <onyks-select>
                    <onyks-option value="" disabled hidden>Wybierz owoc...</onyks-option>
                    <onyks-option value="apple">Jabłko</onyks-option>
                    <onyks-option value="banana" selected>Banan (Domyślnie wybrany)</onyks-option>
                    <onyks-option value="orange">Pomarańcza</onyks-option>
                </onyks-select>
                <onyks-button>Add a new manufacturer</onyks-button>
                <onyks-label size="l" class="left">Datasheet</onyks-label>
                <onyks-file-upload>dsasdsad</onyks-file-upload>
                <onyks-label size="l" class="left">Description</onyks-label>
                <onyks-textarea resize="none"></onyks-textarea>
                <onyks-label size="l" class="left">Suppliers</onyks-label>

            </div>
            <div class="form-part">
                
                <!-- <onyks-label size="l" class="right">Symbol Reference</onyks-label>
                <onyks-textfield size="l" placeholder="eg. BC547BBU_Symbol" class="right" disabled></onyks-textfield>
                <onyks-label size="l" class="right">Symbol Path</onyks-label>
                <onyks-textfield size="l" placeholder="eg. symbols/transistors/" class="right" disabled></onyks-textfield>
                <onyks-button size="l" class="right" background="blue">Select</onyks-button>
                
                <onyks-label size="l" class="right">Footprint Reference No. 1</onyks-label>
                <onyks-textfield size="l" placeholder="eg. BC547BBU_TO_92_3" class="right" disabled></onyks-textfield>
                <onyks-label size="l" class="right">Footprint Path No. 1</onyks-label>
                <onyks-textfield size="l" placeholder="eg. footprints/transistors/" class="right" disabled></onyks-textfield>
                <onyks-button size="l" class="right" background="red">Select</onyks-button>

                <onyks-label size="l" class="right">Footprint Reference No. 2</onyks-label>
                <onyks-textfield size="l" placeholder="eg. BC547BBU_TO_92_3" class="right" disabled></onyks-textfield>
                <onyks-label size="l" class="right">Footprint Path No. 2</onyks-label>
                <onyks-textfield size="l" placeholder="eg. footprints/transistors/" class="right" disabled></onyks-textfield>
                <onyks-button size="l" class="right" background="green">Select</onyks-button>

                <onyks-label size="l" class="right">Footprint Reference No. 3</onyks-label>
                <onyks-textfield size="l" placeholder="eg. BC547BBU_TO_92_3" class="right" disabled></onyks-textfield>
                <onyks-label size="l" class="right">Footprint Path No. 3</onyks-label>
                <onyks-textfield size="l" placeholder="eg. footprints/transistors/" class="right" disabled></onyks-textfield>
                <onyks-button size="l" class="right" background="blue">Select</onyks-button> -->
                
                <onyks-button background="green" type="submit" size="l">Add</onyks-button>
                <onyks-button background="red" type="" size="l">Cancel</onyks-button>
            </div>
        </form>
    </Panel_Content>
</template>

<style scoped>
    form, h1
    {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        max-width: 800px;
        width: 100%;
        margin: 0 auto;
    }
    


    h1
    {
        padding: var(--spacing-lg);
    }

    .form-part 
    {

        flex: 1 1 200px;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    onyks-button, onyks-textfield
    {
        width: 100%;
    }
</style>