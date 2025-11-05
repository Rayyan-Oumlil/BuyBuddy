import { useState, useCallback } from "react"
import { toast } from "@/hooks/use-toast"
import axios from "axios"

const API_BASE_URL = "/api/v1"

export const useChat = () => {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)

  const parsePrice = (price) => {
    if (!price) return 0
    if (typeof price === "number") return price
    // Remove currency symbols and parse
    const cleaned = String(price).replace(/[€$,\s]/g, "").replace(",", ".")
    const parsed = parseFloat(cleaned)
    return isNaN(parsed) ? 0 : parsed
  }

  const sendMessage = useCallback(
    async (content) => {
      const userMessage = {
        id: Date.now().toString(),
        role: "user",
        content,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, userMessage])
      setIsLoading(true)

      try {
        const response = await axios.post(`${API_BASE_URL}/chat`, {
          message: content,
          session_id: sessionId,
        })

        const data = response.data

        if (data.error) {
          throw new Error(data.error)
        }

        if (data.session_id) {
          setSessionId(data.session_id)
        }

        // Products - keep as is (price is string from backend)
        const products = data.products || []

        // Price comparison - parse from backend if available
        let priceComparison = null
        if (data.price_comparison) {
          priceComparison = {
            best_deal: {
              ...data.price_comparison.best_deal,
              price: parsePrice(data.price_comparison.best_deal?.price),
            },
            price_range: {
              min: parsePrice(data.price_comparison.price_range?.min),
              max: parsePrice(data.price_comparison.price_range?.max),
            },
            total_compared: data.price_comparison.total_compared || 0,
          }
        }

        const assistantMessage = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: data.conversational_response || data.product_message || "",
          products: products,
          priceComparison: priceComparison,
          productMessage: data.product_message,
          timestamp: new Date(),
        }

        setMessages((prev) => [...prev, assistantMessage])
      } catch (error) {
        console.error("Error sending message:", error)
        toast({
          title: "Erreur",
          description:
            error.response?.data?.error || error.message || "Une erreur est survenue lors de l'envoi du message",
          variant: "destructive",
        })
      } finally {
        setIsLoading(false)
      }
    },
    [sessionId]
  )

  const loadConversation = useCallback(async (conversationSessionId) => {
    try {
      setIsLoading(true)
      const [historyResponse, productsResponse] = await Promise.all([
        axios.get(`${API_BASE_URL}/history/conversations?session_id=${conversationSessionId}&limit=100`),
        axios.get(`${API_BASE_URL}/history/conversation/${conversationSessionId}/products`),
      ])

      const history = historyResponse.data
      const products = productsResponse.data

      const loadedMessages = []

      history.forEach((item) => {
        loadedMessages.push({
          id: `${item.timestamp || item.created_at}-user`,
          role: "user",
          content: item.user_message,
          timestamp: new Date(item.timestamp || item.created_at),
        })

        // Find products for this conversation
        let structuredQuery = null
        try {
          structuredQuery = item.structured_query ? JSON.parse(item.structured_query) : null
        } catch (e) {
          // Ignore parse errors
        }

        const queryText = structuredQuery?.query_text || item.user_message
        const messageProducts = products.filter((p) => {
          if (!p.search_query || !queryText) return false
          return p.search_query.toLowerCase().includes(queryText.toLowerCase()) ||
            queryText.toLowerCase().includes(p.search_query.toLowerCase().substring(0, 20))
        })

        // Price comparison from products if available
        let priceComparison = null
        if (messageProducts.length > 0) {
          const productPrices = messageProducts.map((p) => parsePrice(p.price)).filter((p) => p > 0)
          if (productPrices.length > 0) {
            const bestProduct = messageProducts.reduce((best, current) => {
              const currentPrice = parsePrice(current.price)
              const bestPrice = parsePrice(best.price)
              return currentPrice < bestPrice ? current : best
            }, messageProducts[0])

            priceComparison = {
              best_deal: {
                name: bestProduct?.name || "",
                price: Math.min(...productPrices),
                platform: bestProduct?.platform || "",
              },
              price_range: {
                min: Math.min(...productPrices),
                max: Math.max(...productPrices),
              },
              total_compared: productPrices.length,
            }
          }
        }

        loadedMessages.push({
          id: `${item.timestamp || item.created_at}-assistant`,
          role: "assistant",
          content: item.assistant_response || "",
          products: messageProducts,
          priceComparison: priceComparison,
          productMessage: item.assistant_response,
          timestamp: new Date(item.timestamp || item.created_at),
        })
      })

      // Clear messages first, then set new ones to ensure proper update
      setMessages([])
      setSessionId(null)
      
      // Use requestAnimationFrame to ensure state updates properly
      requestAnimationFrame(() => {
        setMessages(loadedMessages)
        setSessionId(conversationSessionId)
      })
    } catch (error) {
      console.error("Error loading conversation:", error)
      toast({
        title: "Erreur",
        description: "Impossible de charger la conversation",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }, [])

  const startNewConversation = useCallback(() => {
    setMessages([])
    setSessionId(null)
  }, [])

  return {
    messages,
    isLoading,
    sessionId,
    sendMessage,
    loadConversation,
    startNewConversation,
    setMessages,
    setSessionId,
  }
}
