import axios from 'axios'

const request = axios.create({
  baseURL: '/api/admin',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('admin_token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    if (error.response) {
      console.error('Response data:', error.response.data)
      console.error('Response status:', error.response.status)
    }
    return Promise.reject(error)
  }
)

export const adminLogin = (data) => request.post('/login', data)

export const getAdminInfo = () => request.get('/info')

export const getInviteCodes = () => request.get('/invite-codes')

export const createInviteCode = (data) => request.post('/invite-codes', data)

export const updateInviteCode = (id, data) => request.put(`/invite-codes/${id}`, data)

export const deleteInviteCode = (id) => request.delete(`/invite-codes/${id}`)

export const batchCreateInviteCodes = (data) => request.post('/invite-codes/batch', data)

export const getWorks = () => request.get('/works')

export const createWork = (data) => request.post('/works', data)

export const updateWork = (id, data) => request.put(`/works/${id}`, data)

export const deleteWork = (id) => request.delete(`/works/${id}`)

export const getUsers = () => request.get('/users')

export const getStats = () => request.get('/stats')
