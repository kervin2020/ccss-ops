const API_BASE_URL = 'http://localhost:5000/api'

// Get auth token from localStorage
const getToken = () => localStorage.getItem('token')

// API request helper
async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const token = getToken()
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  }
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Request failed' }))
    throw new Error(error.error || `HTTP error! status: ${response.status}`)
  }
  
  return response.json()
}

// Auth API
export const authAPI = {
  login: async (email: string, password: string) => {
    const data = await apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
    if (data.access_token) {
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
    }
    return data
  },
  
  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },
  
  getCurrentUser: async () => {
    return apiRequest('/auth/me')
  },
}

// Agents API
export const agentsAPI = {
  getAll: (status?: string) => {
    const params = status ? `?status=${status}` : ''
    return apiRequest(`/agents${params}`)
  },
  
  getById: (id: number) => apiRequest(`/agents/${id}`),
  
  create: (data: any) => apiRequest('/agents', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  update: (id: number, data: any) => apiRequest(`/agents/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  
  delete: (id: number) => apiRequest(`/agents/${id}`, {
    method: 'DELETE',
  }),
}

// Clients API
export const clientsAPI = {
  getAll: (status?: string) => {
    const params = status ? `?status=${status}` : ''
    return apiRequest(`/clients${params}`)
  },
  
  getById: (id: number) => apiRequest(`/clients/${id}`),
  
  create: (data: any) => apiRequest('/clients', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  update: (id: number, data: any) => apiRequest(`/clients/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  
  delete: (id: number) => apiRequest(`/clients/${id}`, {
    method: 'DELETE',
  }),
}

// Sites API
export const sitesAPI = {
  getAll: (clientId?: number, status?: string) => {
    const params = new URLSearchParams()
    if (clientId) params.append('client_id', clientId.toString())
    if (status) params.append('status', status)
    const query = params.toString()
    return apiRequest(`/sites${query ? `?${query}` : ''}`)
  },
  
  getById: (id: number) => apiRequest(`/sites/${id}`),
  
  create: (data: any) => apiRequest('/sites', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  update: (id: number, data: any) => apiRequest(`/sites/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  
  delete: (id: number) => apiRequest(`/sites/${id}`, {
    method: 'DELETE',
  }),
}

// Attendances API
export const attendancesAPI = {
  getAll: (params?: { agent_id?: number; site_id?: number; start_date?: string; end_date?: string }) => {
    const query = new URLSearchParams()
    if (params?.agent_id) query.append('agent_id', params.agent_id.toString())
    if (params?.site_id) query.append('site_id', params.site_id.toString())
    if (params?.start_date) query.append('start_date', params.start_date)
    if (params?.end_date) query.append('end_date', params.end_date)
    const queryString = query.toString()
    return apiRequest(`/attendances${queryString ? `?${queryString}` : ''}`)
  },
  
  getById: (id: number) => apiRequest(`/attendances/${id}`),
  
  create: (data: any) => apiRequest('/attendances', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  update: (id: number, data: any) => apiRequest(`/attendances/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  
  delete: (id: number) => apiRequest(`/attendances/${id}`, {
    method: 'DELETE',
  }),
}

// Corrections API
export const correctionsAPI = {
  getAll: (agentId?: number, status?: string) => {
    const params = new URLSearchParams()
    if (agentId) params.append('agent_id', agentId.toString())
    if (status) params.append('status', status)
    const query = params.toString()
    return apiRequest(`/corrections${query ? `?${query}` : ''}`)
  },
  
  getById: (id: number) => apiRequest(`/corrections/${id}`),
  
  create: (data: any) => apiRequest('/corrections', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  approve: (id: number, reviewNotes?: string) => apiRequest(`/corrections/${id}/approve`, {
    method: 'POST',
    body: JSON.stringify({ review_notes: reviewNotes }),
  }),
  
  reject: (id: number, reviewNotes?: string) => apiRequest(`/corrections/${id}/reject`, {
    method: 'POST',
    body: JSON.stringify({ review_notes: reviewNotes }),
  }),
}

// Payrolls API
export const payrollsAPI = {
  getAll: (agentId?: number, status?: string) => {
    const params = new URLSearchParams()
    if (agentId) params.append('agent_id', agentId.toString())
    if (status) params.append('status', status)
    const query = params.toString()
    return apiRequest(`/payrolls${query ? `?${query}` : ''}`)
  },
  
  getById: (id: number) => apiRequest(`/payrolls/${id}`),
  
  create: (data: any) => apiRequest('/payrolls', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  update: (id: number, data: any) => apiRequest(`/payrolls/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  
  delete: (id: number) => apiRequest(`/payrolls/${id}`, {
    method: 'DELETE',
  }),
}

