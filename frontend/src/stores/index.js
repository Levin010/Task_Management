import { defineStore } from 'pinia'
import { ref, reactive, computed } from 'vue'
import axios from 'axios'

export const useMainStore = defineStore('main', () => {
  // 🔐 Auth state
  const user = ref(null)
  const isAuthenticated = computed(() => !!user.value)
  
  // ⏳ Loading state
  const isLoading = ref(false)
  
  // 💬 Message state for cross-route notifications
  const successMessage = ref(null)
  const errorMessage = ref(null)
  
  // 📝 Form state
  const formErrors = ref([])

  // === TOKEN METHODS ===
  function getAccessToken() {
    return localStorage.getItem('access_token')
  }

  function getRefreshToken() {
    return localStorage.getItem('refresh_token')
  }

  function setTokens(accessToken, refreshToken) {
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
  }

  function clearTokens() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  // === LOADING METHODS ===
  function setIsLoading(status) {
    isLoading.value = status
  }

  // === MESSAGE METHODS ===
  function setSuccessMessage(message) {
    successMessage.value = message
    errorMessage.value = null // Clear any existing error
  }

  function setErrorMessage(message) {
    errorMessage.value = message
    successMessage.value = null // Clear any existing success
  }

  function clearMessages() {
    successMessage.value = null
    errorMessage.value = null
  }

  // === FORM ERROR METHODS ===
  function setFormErrors(errors) {
    formErrors.value = errors
  }

  function clearFormErrors() {
    formErrors.value = []
  }

  // === AUTH METHODS ===
  function setUser(userData) {
    user.value = userData
  }

  function clearUser() {
    user.value = null
    clearTokens()
  }

  // Check if user is authenticated by trying to get user info
  async function checkAuth() {
    const accessToken = getAccessToken()
    
    if (!accessToken) {
      clearUser()
      return false
    }

    try {
      const response = await axios.get('/api/v1/me/', {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      })
      
      if (response.data.user) {
        setUser(response.data.user)
        return true
      }
    } catch (error) {
      console.log('Not authenticated:', error)
      
      // Try to refresh token if request failed
      if (error.response?.status === 401) {
        const refreshed = await refreshToken()
        if (refreshed) {
          // Retry the original request
          try {
            const retryResponse = await axios.get('/api/v1/me/', {
              headers: {
                'Authorization': `Bearer ${getAccessToken()}`
              }
            })
            
            if (retryResponse.data.user) {
              setUser(retryResponse.data.user)
              return true
            }
          } catch (retryError) {
            console.log('Retry failed:', retryError)
          }
        }
      }
      
      clearUser()
    }
    return false
  }

  // Sign up user
  async function signup(userData) {
    setIsLoading(true)
    clearFormErrors()
    
    try {
      const response = await axios.post('/api/v1/signup/', userData, {
        headers: {
            'Content-Type': 'application/json',
        }
      })
      
      if (response.data.user && response.data.access_token) {
        setTokens(response.data.access_token, response.data.refresh_token)
        setUser(response.data.user)
        setSuccessMessage('Account created successfully! Welcome aboard!')
        return { success: true, data: response.data }
      }
    } catch (error) {
      const errorData = handleAuthError(error)
      return { success: false, error: errorData }
    } finally {
      setIsLoading(false)
    }
  }

  // Login user
  async function login(credentials) {
    setIsLoading(true)
    clearFormErrors()
    
    try {
      const response = await axios.post('/api/v1/login/', credentials)
      
      if (response.data.user && response.data.access_token) {
        setTokens(response.data.access_token, response.data.refresh_token)
        setUser(response.data.user)
        setSuccessMessage('Login successful! Welcome back!')
        return { success: true, data: response.data }
      }
    } catch (error) {
      const errorData = handleAuthError(error)
      return { success: false, error: errorData }
    } finally {
      setIsLoading(false)
    }
  }

  // Logout user
  async function logout() {
    setIsLoading(true)
    
    try {
      const refreshToken = getRefreshToken()
      
      await axios.post('/api/v1/logout/', {
        refresh_token: refreshToken
      }, {
        headers: {
          'Authorization': `Bearer ${getAccessToken()}`
        }
      })
      
      clearUser()
      clearMessages()
      setSuccessMessage('Logged out successfully!')
      return { success: true }
    } catch (error) {
      console.error('Logout error:', error)
      // Even if logout fails on server, clear local state
      clearUser()
      return { success: false, error: 'Logout failed' }
    } finally {
      setIsLoading(false)
    }
  }

  // Handle authentication errors
  function handleAuthError(error) {
    const errors = []
    
    console.log('Full error:', error)
    console.log('Response status:', error.response?.status)
    console.log('Response data type:', typeof error.response?.data)
    console.log('Response data:', error.response?.data)
    
    if (error.response) {
        if (error.response.data) {
        // Check if response is JSON (object) or HTML (string)
        if (typeof error.response.data === 'object' && error.response.data !== null) {
            // Handle JSON error response from Django REST Framework
            for (const property in error.response.data) {
            if (Array.isArray(error.response.data[property])) {
                error.response.data[property].forEach(errorMsg => {
                errors.push(`${property}: ${errorMsg}`)
                })
            } else {
                errors.push(`${property}: ${error.response.data[property]}`)
            }
            }
        } else {
            // Handle HTML error response (what you're getting now)
            console.error('Received HTML instead of JSON:', error.response.data.substring(0, 200))
            
            if (error.response.status === 400) {
            errors.push('Bad request. Please check your input and try again.')
            } else if (error.response.status === 500) {
            errors.push('Server error. Please try again later.')
            } else if (error.response.status === 404) {
            errors.push('API endpoint not found. Please check your configuration.')
            } else {
            errors.push(`Server error (${error.response.status}). Please try again.`)
            }
        }
        } else {
        errors.push('Server error occurred. Please try again.')
        }
        
        setErrorMessage('Authentication failed. Please check the errors below.')
        
    } else if (error.request) {
        errors.push('Network error. Please check your connection and try again.')
        setErrorMessage('Network error. Please check your connection.')
        
    } else {
        errors.push('An unexpected error occurred. Please try again.')
        setErrorMessage('Something went wrong. Please try again.')
    }
    
    setFormErrors(errors)
    return { errors, message: errorMessage.value }
    }

  // Refresh token 
  async function refreshToken() {
    const refreshTokenValue = getRefreshToken()
    
    if (!refreshTokenValue) {
      clearUser()
      return false
    }

    try {
      const response = await axios.post('/api/v1/token/refresh/', {
        refresh_token: refreshTokenValue
      })

      if (response.data.access_token) {
        // Update access token (and refresh token if rotated)
        setTokens(
          response.data.access_token, 
          response.data.refresh_token || refreshTokenValue
        )
        
        console.log('Token refreshed successfully')
        return true
      }
    } catch (error) {
      console.error('Token refresh failed:', error)
      clearUser()
      return false
    }
  }

  return {
    // State
    user,
    isAuthenticated,
    isLoading,
    successMessage,
    errorMessage,
    formErrors,
    
    // Loading methods
    setIsLoading,
    
    // Message methods
    setSuccessMessage,
    setErrorMessage,
    clearMessages,
    
    // Form error methods
    setFormErrors,
    clearFormErrors,
    
    // Auth methods
    setUser,
    clearUser,
    checkAuth,
    signup,
    login,
    logout,
    refreshToken,
    handleAuthError,
    
    // Token methods
    getAccessToken,
    getRefreshToken,
    setTokens,
    clearTokens
  }
})