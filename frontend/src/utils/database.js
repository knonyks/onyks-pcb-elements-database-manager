const fetch_data = async (endpoint, data = null) => 
{
    try 
    {
        let response;
        if(data)
        {
            response = await fetch(`/api${endpoint}`, 
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
        }
        else
        {
            response = await fetch(`/api${endpoint}`)
            if (!response.ok) 
            {
                throw new Error(`ERROR: ${response.status}`)
            }
        }
        return await response.json()
    } 
    catch (err) 
    {
        console.error("ERROR:", err)
    }
}

export {fetch_data};