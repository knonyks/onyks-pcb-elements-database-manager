import { api_call } from './api';

async function db_get_list(query, current_settings)
{
    let data = {}
    if(current_settings.cursor != null)
    {
        data.cursor = current_settings.cursor
    }
    data.limit = current_settings.limit
    const response = await api_call(query, "GET",  null, data)
    return response
}

export {db_get_list};