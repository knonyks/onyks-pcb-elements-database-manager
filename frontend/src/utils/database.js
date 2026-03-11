import axios from "axios";

async function api_call(endpoint, method = 'GET', data = null, params = null) 
{
    try 
    {
        const response = await axios({
            method: method,
            url: endpoint,
            data: data,
            params: params
        });
        return {data: response.data, status: response.status};
    } 
    catch (err) 
    {
        console.error(`ERROR ${endpoint}:`, err);
        return {data: null, status: err.status};
    }
}

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

export {api_call, db_inifnite_scroll_query};