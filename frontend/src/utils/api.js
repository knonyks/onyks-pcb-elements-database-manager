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
    info: async () =>
    {
        try 
        {
            const response = await api.get(`/repository/info`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    content: async (path = '') =>
    {
        try 
        {
            const response = await api.get(`/repository/content`,
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
            throw error
        }
    }
}

export const elements = 
{
    lastAdded: async () =>
    {
        try 
        {
            const response = await api.get(`/elements/last-added`);
            return response
        } 
        catch (error)
        {
            throw error
        }
    },
    count: async () =>
    {
        try 
        {
            const response = await api.get(`/elements/count`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    // create: async (element, datasheet = null) =>
    // {
    //     try 
    //     {
    //         const formData = new FormData();

    //         formData.append('element', JSON.stringify(element));

    //         if (datasheet)
    //         {
    //             formData.append('datasheet', datasheet);
    //         }

    //         const response = await api.post(`/element/create`, formData,
    //         {
    //             headers: {'Content-Type': 'multipart/form-data'} 
    //         });
    //         return response
    //     } 
    //     catch (error) 
    //     {
    //         return error
    //     }
    // },
    // duplicate: async (id, element, datasheet = null) =>
    // {
    //     try 
    //     {
    //         const formData = new FormData();

    //         formData.append('element', JSON.stringify(element));

    //         if (datasheet)
    //         {
    //             formData.append('datasheet', datasheet);
    //         }

    //         const response = await api.post(`/element/duplicate/${id}`, formData,
    //         {
    //             headers: {'Content-Type': 'multipart/form-data'} 
    //         });
    //         return response
    //     } 
    //     catch (error) 
    //     {
    //         return error
    //     }
    // },
    // get: async (id) =>
    // {
    //     try 
    //     {
    //         const response = await api.get(`/element/${id}`);
    //         return response
    //     } 
    //     catch (error) 
    //     {
    //         return error
    //     }
    // },
    // list: async (limit, skip) =>
    // {
    //     try 
    //     {
    //         const response = await api.get(`/element/list`, {
    //             params: {
    //                 limit: limit,
    //                 skip: skip
    //             }
    //         });
    //         return response
    //     } 
    //     catch (error) 
    //     {
    //         return error
    //     }
    // },
    // edit: async (id, element, datasheet = null) =>
    // {
    //     try 
    //     {
    //         const formData = new FormData();
    //         formData.append('element', JSON.stringify(element));

    //         if (datasheet)
    //         {
    //             formData.append('datasheet', datasheet);
    //         }

    //         const response = await api.put(`/element/edit/${id}`, formData,
    //         {
    //             headers: {'Content-Type': 'multipart/form-data'}
    //         });
    //         return response
    //     } 
    //     catch (error) 
    //     {
    //         return error
    //     }
    // },
    // delete: async (id) =>
    // {
    //     try 
    //     {
    //         const response = await api.delete(`/element/delete/${id}`);
    //         return response
    //     } 
    //     catch (error) 
    //     {
    //         return error
    //     }
    // },
    // openDatasheet: (uuid) =>
    // {
    //     window.open(`/files/${uuid}.pdf`, '_blank');
    // }
}

export const tables = 
{
    count: async () =>
    {
        try 
        {
            const response = await api.get(`/tables/count`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    counts: async () =>
    {
        try 
        {
            const response = await api.get(`/tables/counts`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    create: async (name) =>
    {
        try 
        {
            const response = await api.post(`/tables`, name);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    list: async (page = 1, limit = 100, search = '', sortBy = 'id', sortDesc = true) =>
    {
        try 
        {
            const response = await api.get(`/tables`, {
                params: {
                    page: page,
                    limit: limit,
                    search: search,
                    sortBy: sortBy,
                    sortDesc: sortDesc
                }
            });
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    delete: async (id) =>
    {
        try 
        {
            const response = await api.delete(`/tables/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    edit: async (id, supplier) =>
    {
        try 
        {
            const response = await api.patch(`/tables/${id}`, supplier);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    get: async (id) =>
    {
        try 
        {
            const response = await api.get(`/tables/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    }
}

export const manufacturers = 
{
    count: async () =>
    {
        try 
        {
            const response = await api.get(`/manufacturers/count`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    counts: async () =>
    {
        try 
        {
            const response = await api.get(`/manufacturers/counts`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    create: async (name) =>
    {
        try 
        {
            const response = await api.post(`/manufacturers`, name);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    list: async (page = 1, limit = 100, search = '', sortBy = 'id', sortDesc = true) =>
    {
        try 
        {
            const response = await api.get(`/manufacturers`, {
                params: {
                    page: page,
                    limit: limit,
                    search: search,
                    sortBy: sortBy,
                    sortDesc: sortDesc
                }
            });
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    delete: async (id) =>
    {
        try 
        {
            const response = await api.delete(`/manufacturers/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    edit: async (id, supplier) =>
    {
        try 
        {
            const response = await api.patch(`/manufacturers/${id}`, supplier);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    get: async (id) =>
    {
        try 
        {
            const response = await api.get(`/manufacturers/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    }
}

export const suppliers = 
{
    count: async () =>
    {
        try 
        {
            const response = await api.get(`/suppliers/count`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    create: async (name) =>
    {
        try 
        {
            const response = await api.post(`/suppliers`, name);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    list: async (page = 1, limit = 100, search = '', sortBy = 'id', sortDesc = true) =>
    {
        try 
        {
            const response = await api.get(`/suppliers`, {
                params: {
                    page: page,
                    limit: limit,
                    search: search,
                    sortBy: sortBy,
                    sortDesc: sortDesc
                }
            });
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    delete: async (id) =>
    {
        try 
        {
            const response = await api.delete(`/suppliers/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    edit: async (id, supplier) =>
    {
        try 
        {
            const response = await api.patch(`/suppliers/${id}`, supplier);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    get: async (id) =>
    {
        try 
        {
            const response = await api.get(`/suppliers/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    }
}

export const users = 
{
    create: async (name) =>
    {
        try 
        {
            const response = await api.post(`/users`, name);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    list: async (page = 1, limit = 100, search = '', sortBy = 'id', sortDesc = true) =>
    {
        try 
        {
            const response = await api.get(`/users`, {
                params: {
                    page: page,
                    limit: limit,
                    search: search,
                    sortBy: sortBy,
                    sortDesc: sortDesc
                }
            });
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    delete: async (id) =>
    {
        try 
        {
            const response = await api.delete(`/suppliers/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    edit: async (id, supplier) =>
    {
        try 
        {
            const response = await api.patch(`/suppliers/${id}`, supplier);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    get: async (id) =>
    {
        try 
        {
            const response = await api.get(`/suppliers/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    }
}

export const services = 
{
    repository,
    elements,
    tables,
    manufacturers,
    suppliers,
    users
}

// ################################################

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
            throw error
        }
    },
    count: async () =>
    {
        try 
        {
            const response = await api.get(`/elements/count`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    create: async (element, datasheet = null) =>
    {
        try 
        {
            const formData = new FormData();

            formData.append('element', JSON.stringify(element));

            if (datasheet)
            {
                formData.append('datasheet', datasheet);
            }

            const response = await api.post(`/element/create`, formData,
            {
                headers: {'Content-Type': 'multipart/form-data'} 
            });
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    duplicate: async (id, element, datasheet = null) =>
    {
        try 
        {
            const formData = new FormData();

            formData.append('element', JSON.stringify(element));

            if (datasheet)
            {
                formData.append('datasheet', datasheet);
            }

            const response = await api.post(`/element/duplicate/${id}`, formData,
            {
                headers: {'Content-Type': 'multipart/form-data'} 
            });
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
    edit: async (id, element, datasheet = null) =>
    {
        try 
        {
            const formData = new FormData();
            formData.append('element', JSON.stringify(element));

            if (datasheet)
            {
                formData.append('datasheet', datasheet);
            }

            const response = await api.put(`/element/edit/${id}`, formData,
            {
                headers: {'Content-Type': 'multipart/form-data'}
            });
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
    },
    openDatasheet: (uuid) =>
    {
        window.open(`/files/${uuid}.pdf`, '_blank');
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
    create: async (table) =>
    {
        try 
        {
            const response = await api.post(`/table/create`, table);
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
            const response = await api.get(`/table/${id}`);
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
            const response = await api.get(`/table/list`, {
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
    edit: async (id, table) =>
    {
        try 
        {
            const response = await api.put(`/table/edit/${id}`, table);
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
            const response = await api.delete(`/table/delete/${id}`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    }
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
    create: async (element) =>
    {
        try 
        {
            const response = await api.post(`/manufacturer/create`, element);
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
            const response = await api.get(`/manufacturer/${id}`);
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
    edit: async (id, manufacturer) =>
    {
        try 
        {
            const response = await api.put(`/manufacturer/edit/${id}`, manufacturer);
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
            const response = await api.delete(`/manufacturer/delete/${id}`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    }
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
    create: async (element) =>
    {
        try 
        {
            const response = await api.post(`/supplier/create`, element);
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
    delete: async (id) =>
    {
        try 
        {
            const response = await api.delete(`/supplier/delete/${id}`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    edit: async (id, supplier) =>
    {
        try 
        {
            const response = await api.put(`/supplier/edit/${id}`, supplier);
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
            const response = await api.get(`/supplier/${id}`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    }
}

export const other =
{
    updateViews: async () =>
    {
        try 
        {
            const response = await api.post(`/update-views`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    }
}

