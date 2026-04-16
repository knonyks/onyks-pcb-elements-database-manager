import { api_call } from './api';

async function db_inifnite_scroll_query(query, current_settings)
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

export {db_inifnite_scroll_query};