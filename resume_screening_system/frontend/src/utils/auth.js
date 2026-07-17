// Auth utils
export const isAuthenticated = () => {
  const token = localStorage.getItem('token');
  return !!token;
};

export const getToken = () => localStorage.getItem('token');

export const logout = () => {
  localStorage.removeItem('token');
  window.location.href = '/login';
};

export const apiFetch = async (url, options = {}) => {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
const res = await fetch(`/api${url.startsWith('/') ? '' : '/'}${url}`, { ...options, headers });
  if (res.status === 401) {
    logout();
  }
  return res;
};
