<script setup lang="js">
    import PageContentElement from '@/components/PageContentElement.vue';
    import WarningElement from '@/components/WarningElement.vue';
    import { api_repository_name, api_repository_list } from '@/utils/api';
    import { ref, onMounted } from 'vue';

    const repo_path = ref(null);
    const repo_path_content = ref([]);
    const repo_explorer_content = ref([]);

    const repo_process_received_list = async (url_format) => 
    {
        return (await api_repository_list(url_format)).data.map(({ name, type }) =>
        {
            if(name.toLowerCase().endsWith('.schlib') || name.toLowerCase().endsWith('.pcblib') )
            {
                return {
                    name: name,
                    type: 'folder'
                }
            }
            else
            {
                return {
                    name: name,
                    type: type
                }
            }
        })
    }

    const repo_explorer_enter_folder = async (e) => 
    {
        const folder_name = e.detail.folder.name;
        repo_path.value.add_folder(folder_name);
        let tab = repo_path.value.current_path().slice()
        tab.shift();
        const url_format = '/' + tab.join('/');
        repo_explorer_content.value = (await repo_process_received_list(url_format));
    };

    const repo_path_changed = async (event) => 
    {
        const current_path = event.detail.path;
        let tab = current_path.slice()
        tab.shift();
        const url_format = '/' + tab.join('/');
        repo_explorer_content.value = (await repo_process_received_list(url_format));
    };

    onMounted(async () => 
    { 
        try
        {
            repo_path.value.add_folder((await api_repository_name()).data);
            repo_explorer_content.value = (await repo_process_received_list())
        }
        catch(e)
        {
            console.log("!E!", e);
        }
    });
</script>

<template>
    <PageContentElement>
        <h1>Repository</h1>
        <WarningElement/>
        <onyks-path ref="repo_path" @path-changed="repo_path_changed" :content.prop="repo_path_content"></onyks-path>
        <onyks-file-explorer :content.prop="repo_explorer_content" @enter-folder="repo_explorer_enter_folder"></onyks-file-explorer>
    </PageContentElement>
</template>