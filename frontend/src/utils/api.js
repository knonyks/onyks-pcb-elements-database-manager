import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

api.interceptors.response.use((response) => response, (error) => 
{
  if (error.response && error.response.status === 401) 
  {
    console.log('!E!');
  }
  return Promise.reject(error);
});

export default api;

// REPOSITORY
export const api_repository_name = () => api.get('/repository/name');
export const api_repository_list = (path = "") => 
{
  return api.get('/repository/list', 
  {
    params: 
    {
      path: path
    }
  });
};

// MANUFACTURER
export const api_manufacturer_total = () => api.get('/manufacturer/total');
export const api_manufacturer_create = (name) => 
{
  return api.post('/manufacturer/create', 
  {
    name: name 
  });
};
export const api_manufacturer_list = (page = 1, limit = 20) => 
  {
  return api.get('/manufacturer/list', {
    params: {
      page: page,
      limit: limit,
    }
  });
};


// SUPPLIER
export const api_supplier_total = () => api.get('/supplier/total');
export const api_supplier_list = (page = 1, limit = 20) => {
  return api.get('/supplier/list', {
    params: {
      page: page,
      limit: limit
    }
  });
};
export const api_supplier_create = (name) => 
{
  return api.post('/supplier/create', 
  {
    name: name 
  });
};