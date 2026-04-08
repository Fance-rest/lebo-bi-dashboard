import axios from 'axios'

const http = axios.create({
  baseURL: '',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Response interceptor — log errors
http.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error(
      '[API Error]',
      error.config?.method?.toUpperCase(),
      error.config?.url,
      error.response?.status || error.message
    )
    return Promise.reject(error)
  }
)

export default http
