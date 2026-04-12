<script setup lang="js">
    import PageContent from '@/components/PageContent.vue';
    import { ref, onMounted } from 'vue';
    import { api_call } from '@/utils/database';
    import Warning from '@/components/Warning.vue';

    const repo_path = ref(null);
    const repo_explorer = ref(null);
    const repo_explorer_content = ref([]);

    const update_explorer = async (path) =>
    {
        try
        {
            const repository_list = await api_call('/api/repository/list', 'GET', null, { path: path });
            return repository_list.data.map(({ name, type }) =>
            {
                if(name.toLowerCase().endsWith('.schlib') || name.toLowerCase().endsWith('.pcblib') )
                {
                    console.log("Znaleziono bibliotekę:", name);
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
            });
        }
        catch (error) 
        {
            console.error("Błąd API:", error);
            return [];
        }
    }


    const repo_explorer_enter_folder = async (e) => 
    {
        const folder_name = e.detail.folder.name;
        repo_path.value.add_folder(folder_name);
        let tab = repo_path.value.current_path().slice()
        tab.shift();
        const url_format = '/' + tab.join('/');
        repo_explorer_content.value = await update_explorer(url_format);
    };

    const repo_path_changed = async (event) => 
    {
        const current_path = event.detail.path;
        let tab = current_path.slice()
        tab.shift();
        const url_format = '/' + tab.join('/');
        repo_explorer_content.value = await update_explorer(url_format);
    };

    onMounted(async () => 
    { 
        if (repo_path.value) 
        {
            repo_path.value.add_folder("elements");
        }   

        try 
        {
            repo_explorer_content.value = await update_explorer('/');
        }
        catch (error) 
        {
            console.error("Błąd API:", error);
        }
    });
</script>

<template>
    <PageContent>
        <h1>Repository</h1>
        <Warning/>
        <onyks-path ref="repo_path" @path-changed="repo_path_changed"></onyks-path>
        <onyks-file-explorer ref="repo_explorer" :content.prop="repo_explorer_content" @enter-folder="repo_explorer_enter_folder"></onyks-file-explorer>
    </PageContent>
</template>