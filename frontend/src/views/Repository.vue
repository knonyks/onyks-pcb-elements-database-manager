<script setup lang="js">
    import PageContent from '@/components/PageContent.vue';
    import Warning from '@/components/Warning.vue';
    import { ref, onMounted } from 'vue';
    import { svn_list } from '@/utils/svn';
    import { api_call } from '@/utils/api';

    const repo_path = ref(null);
    const repo_path_content = ref([]);
    const repo_explorer_content = ref([]);

    const repo_explorer_enter_folder = async (e) => 
    {
        const folder_name = e.detail.folder.name;
        repo_path.value.add_folder(folder_name);
        let tab = repo_path.value.current_path().slice()
        tab.shift();
        const url_format = '/' + tab.join('/');
        repo_explorer_content.value = await svn_list(url_format);
    };

    const repo_path_changed = async (event) => 
    {
        const current_path = event.detail.path;
        let tab = current_path.slice()
        tab.shift();
        const url_format = '/' + tab.join('/');
        repo_explorer_content.value = await svn_list(url_format);
    };

    onMounted(async () => 
    { 
        let repo_name = await api_call('/api/repository/name')
        if (repo_path.value) 
        {
            repo_path.value.add_folder(repo_name.data.name);
        }
        try 
        {
            repo_explorer_content.value = await svn_list('/');
        }
        catch (error) 
        {}
    });
</script>

<template>
    <PageContent>
        <h1>Repository</h1>
        <Warning/>
        <onyks-path ref="repo_path" @path-changed="repo_path_changed" :content.prop="repo_path_content"></onyks-path>
        <onyks-file-explorer :content.prop="repo_explorer_content" @enter-folder="repo_explorer_enter_folder"></onyks-file-explorer>
    </PageContent>
</template>