const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001';

export const API_ENDPOINTS = {
  GENERATE: `${API_BASE_URL}/api/generate`,
  INPAINT: `${API_BASE_URL}/api/inpaint`,
  EXTEND: `${API_BASE_URL}/api/extend`,
  SUPER_RESOLUTION: `${API_BASE_URL}/api/super-resolution`,
  COMPUTE_POWER: `${API_BASE_URL}/api/compute-power`,
  WORKS: `${API_BASE_URL}/api/works`,
  ORDERS: `${API_BASE_URL}/api/orders`,
};

export const getApiUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`;
};

export default API_BASE_URL;
