import { useState } from 'react'
import axios from 'axios'

const API_BASE_URL = '/api/v1'

export function useChat() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)

  const sendMessage = async (text, currentSessionId = null) => {
    setLoading(true)

    // Add user message
    const userMessage = { text, response: null }
    setMessages((prev) => [...prev, userMessage])

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message: text,
        session_id: currentSessionId || sessionId,
      })

      // Update session ID if provided
      if (response.data.session_id) {
        setSessionId(response.data.session_id)
      }

      // Update last message with response
      setMessages((prev) => {
        const updated = [...prev]
        // Ensure response exists, even if empty
        const responseData = response.data || {
          error: 'Réponse vide reçue du serveur',
          products: []
        }
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          response: responseData,
        }
        return updated
      })
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage = {
        text,
        response: {
          error: error.response?.data?.detail || error.response?.data?.error || error.message || 'Une erreur est survenue',
          products: [],
        },
      }
      setMessages((prev) => {
        const updated = [...prev]
        updated[updated.length - 1] = errorMessage
        return updated
      })
    } finally {
      setLoading(false)
    }
  }

  return {
    messages,
    loading,
    sessionId,
    sendMessage,
  }
}

