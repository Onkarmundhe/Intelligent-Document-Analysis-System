import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth headers here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
    }
    return Promise.reject(error)
  }
)

// Document API
export const documentAPI = {
  // Upload document
  upload: async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // List all documents
  list: async () => {
    const response = await api.get('/api/documents/')
    return response.data
  },

  // Get document by ID
  get: async (documentId) => {
    const response = await api.get(`/api/documents/${documentId}`)
    return response.data
  },

  // Delete document
  delete: async (documentId) => {
    const response = await api.delete(`/api/documents/${documentId}`)
    return response.data
  },

  // Generate summary
  summarize: async (documentId) => {
    const response = await api.post(`/api/documents/${documentId}/summarize`)
    return response.data
  },

  // Find similar documents
  findSimilar: async (documentId, topK = 3) => {
    const response = await api.get(`/api/documents/${documentId}/similar?top_k=${topK}`)
    return response.data
  },

  // Compare documents
  compare: async (documentIds) => {
    const response = await api.post('/api/documents/compare', documentIds)
    return response.data
  },

  // Get system stats
  getStats: async () => {
    const response = await api.get('/api/documents/stats/system')
    return response.data
  },
}

// Chat API
export const chatAPI = {
  // Ask question
  ask: async (question, documentIds = null, maxSources = 5) => {
    const response = await api.post('/api/chat/ask', {
      question,
      document_ids: documentIds,
      max_sources: maxSources,
    })
    return response.data
  },

  // Get chat history
  getHistory: async (documentId) => {
    const response = await api.get(`/api/chat/history/${documentId}`)
    return response.data
  },

  // Clear chat history
  clearHistory: async (documentId) => {
    const response = await api.delete(`/api/chat/history/${documentId}`)
    return response.data
  },

  // Ask multiple documents
  askMultiple: async (question, documentIds = null, maxSources = 5) => {
    const response = await api.post('/api/chat/ask-multiple', null, {
      params: {
        question,
        document_ids: documentIds?.join(','),
        max_sources: maxSources,
      },
    })
    return response.data
  },
}

export default api 