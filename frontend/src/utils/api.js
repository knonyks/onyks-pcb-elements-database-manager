import axios from 'axios';

const api = axios.create(
{
  baseURL: '/api',
  timeout: 5000,
  headers: 
  {
    'Content-Type': 'application/json',
    // 'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
});

export const repository = 
{
    name: async () =>
    {
        try 
        {
            const response = await api.get(`/repository/name`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    list: async (path) =>
    {
        try 
        {
            const response = await api.get(`/repository/list`,
            {
                params: 
                {
                    path: path
                }
            });
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    statistics: async () => 
    {
        try 
        {
            const response = await api.get(`/repository/statistics`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    }
}

export const element = 
{
    lastAdded: async () =>
    {
        try 
        {
            const response = await api.get(`/element/last-added`);
            return response
        } 
        catch (error)
        {
            console.dir(error)
            return error
        }
    },
    number: async () =>
    {
        try 
        {
            const response = await api.get(`/element/number`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    create: async (details) =>
    {
        try 
        {
            const response = await api.post(`/element/create`, details);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    get: async (id) =>
    {
        try 
        {
            const response = await api.get(`/element/${id}`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    list: async (limit, skip) =>
    {
        try 
        {
            const response = await api.get(`/element/list`, {
                params: {
                    limit: limit,
                    skip: skip
                }
            });
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    edit: async (id, element) =>
    {
        try 
        {
            const response = await api.put(`/element/edit/${id}`, element);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    delete: async (id) =>
    {
        try 
        {
            const response = await api.delete(`/element/delete/${id}`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    }
}

export const table = 
{
    number: async () =>
    {
        try 
        {
            const response = await api.get(`/table/number`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    numbers: async () =>
    {
        try 
        {
            const response = await api.get(`/table/numbers`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
}

export const manufacturer = 
{
    number: async () =>
    {
        try 
        {
            const response = await api.get(`/manufacturer/number`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    numbers: async () =>
    {
        try 
        {
            const response = await api.get(`/manufacturer/numbers`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    create: async (name) =>
    {
        try 
        {
            const response = await api.post(`/manufacturer/create`, name);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    list: async (limit, skip) =>
    {
        try 
        {
            const response = await api.get(`/manufacturer/list`, {
                params: {
                    limit: limit,
                    skip: skip
                }
            });
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
}

export const supplier = 
{
    number: async () =>
    {
        try 
        {
            const response = await api.get(`/supplier/number`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    create: async (name) =>
    {
        try 
        {
            const response = await api.post(`/supplier/create`, name);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    list: async (limit, skip) =>
    {
        try 
        {
            const response = await api.get(`/supplier/list`, {
                params: {
                    limit: limit,
                    skip: skip
                }
            });
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
}