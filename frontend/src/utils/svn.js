import { api_call } from '@/utils/api';

const svn_list = async (path) =>
{
    try
    {
        const repository_list = await api_call('/api/repository/list', 'GET', null, { path: path });
        return repository_list.data.map(({ name, type }) =>
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
        });
    }
    catch (error) 
    {
        console.error("Błąd API:", error);
        return [];
    }
}

export {svn_list};