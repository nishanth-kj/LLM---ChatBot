import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000,
})

export const sendMessage = async (message) => {
    try {
        const response = await apiClient.post('/api/chat', {
            question: message
        })
        return response.data
    } catch (error) {
        console.error('API Error:', error)
        throw new Error(error.response?.data?.detail || 'Failed to send message')
    }
}

export const checkHealth = async () => {
    try {
        const response = await apiClient.get('/health')
        return response.data
    } catch (error) {
        console.error('Health check failed:', error)
        throw error
    }
}

export default apiClient
