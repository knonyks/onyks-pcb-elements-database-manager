import axios from "axios";

async function api_call(endpoint, method = 'GET', data = null) 
{
    try 
    {
        const response = await axios({
            method: method,
            url: endpoint,
            data: data
        });
        return {data: response.data, status: response.status};
    } 
    catch (err) 
    {
        console.error(`ERROR ${endpoint}:`, err);
        return {data: null, status: err.status};
    }
}
export {api_call};