const API_BASE_URL = 'http://localhost:5000/api'

// Get auth token from localStorage (sanitize common invalid values)
const getToken = (): string | null => {
  const t = localStorage.getItem('token')
  if (!t || t === 'null' || t === 'undefined') {
    // remove invalid sentinel values so we don't send "Bearer null"
    localStorage.removeItem('token')
    return null
  }
  return t
}

// API request helper
async function apiRequest<T = any>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getToken()
  const headers = new Headers(options.headers)
  headers.set('Content-Type', 'application/json')

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    let body: any = null
    try {
      body = await response.json()
    } catch { }
    const serverMsg = body?.error || body?.message || body?.msg || null
    throw new Error(serverMsg || `HTTP error! status: ${response.status}`)
  }

  if (response.status === 204) return null as any

  return response.json()
}

// ===== Auth API =====
interface LoginResponse {
  access_token: string
  user: Record<string, any>
}

export const authAPI = {
  login: async (email: string, password: string) => {
    const data = await apiRequest<LoginResponse>('/auth/login', {
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

  getCurrentUser: async () => apiRequest<Record<string, any>>('/auth/me'),
}

// ===== Agents API =====
export const agentsAPI = {
  getAll: (status?: string) => {
    const params = status ? `?status=${encodeURIComponent(status)}` : ''
    return apiRequest(`/agents${params}`)
  },

  getById: (id: number) => apiRequest(`/agents/${id}`),

  create: (data: Record<string, any>) => apiRequest('/agents', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  update: (id: number, data: Record<string, any>) => apiRequest(`/agents/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),

  delete: (id: number) => apiRequest(`/agents/${id}`, {
    method: 'DELETE',
  }),
}

// ===== Clients API =====
export const clientsAPI = {
  getAll: (status?: string) => {
    const params = status ? `?status=${encodeURIComponent(status)}` : ''
    return apiRequest(`/clients${params}`)
  },

  getById: (id: number) => apiRequest(`/clients/${id}`),

  create: (data: Record<string, any>) => apiRequest('/clients', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  update: (id: number, data: Record<string, any>) => apiRequest(`/clients/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),

  delete: (id: number) => apiRequest(`/clients/${id}`, {
    method: 'DELETE',
  }),
}

// ===== Sites API =====
export const sitesAPI = {
  getAll: (clientId?: number, status?: string) => {
    const params = new URLSearchParams()
    if (clientId !== undefined) params.append('client_id', clientId.toString())
    if (status) params.append('status', status)
    const query = params.toString()
    return apiRequest(`/sites${query ? `?${query}` : ''}`)
  },

  getById: (id: number) => apiRequest(`/sites/${id}`),

  create: (data: Record<string, any>) => apiRequest('/sites', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  update: (id: number, data: Record<string, any>) => apiRequest(`/sites/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),

  delete: (id: number) => apiRequest(`/sites/${id}`, {
    method: 'DELETE',
  }),
}

// ===== Attendances API =====
export const attendancesAPI = {
  getAll: (params?: { agent_id?: number; site_id?: number; start_date?: string; end_date?: string }) => {
    const query = new URLSearchParams()
    if (params?.agent_id !== undefined) query.append('agent_id', params.agent_id.toString())
    if (params?.site_id !== undefined) query.append('site_id', params.site_id.toString())
    if (params?.start_date) query.append('start_date', params.start_date)
    if (params?.end_date) query.append('end_date', params.end_date)
    const queryString = query.toString()
    return apiRequest(`/attendances${queryString ? `?${queryString}` : ''}`)
  },

  getById: (id: number) => apiRequest(`/attendances/${id}`),

  create: (data: Record<string, any>) => apiRequest('/attendances', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  update: (id: number, data: Record<string, any>) => apiRequest(`/attendances/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),

  delete: (id: number) => apiRequest(`/attendances/${id}`, {
    method: 'DELETE',
  }),
}

// ===== Corrections API =====
export const correctionsAPI = {
  getAll: (agentId?: number, status?: string) => {
    const params = new URLSearchParams()
    if (agentId !== undefined) params.append('agent_id', agentId.toString())
    if (status) params.append('status', status)
    const query = params.toString()
    return apiRequest(`/corrections${query ? `?${query}` : ''}`)
  },

  getById: (id: number) => apiRequest(`/corrections/${id}`),

  create: (data: Record<string, any>) => apiRequest('/corrections', {
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

// ===== Payrolls API =====
export const payrollsAPI = {
  getAll: (agentId?: number, status?: string) => {
    const params = new URLSearchParams()
    if (agentId !== undefined) params.append('agent_id', agentId.toString())
    if (status) params.append('status', status)
    const query = params.toString()
    return apiRequest(`/payrolls${query ? `?${query}` : ''}`)
  },

  getById: (id: number) => apiRequest(`/payrolls/${id}`),

  create: (data: Record<string, any>) => apiRequest('/payrolls', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  update: (id: number, data: Record<string, any>) => apiRequest(`/payrolls/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),

  delete: (id: number) => apiRequest(`/payrolls/${id}`, {
    method: 'DELETE',
  }),
}
