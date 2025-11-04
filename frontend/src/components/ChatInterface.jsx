import { useState, useRef, useEffect } from 'react'
import { Send, ShoppingBag, Loader2, ThumbsDown, ExternalLink } from 'lucide-react'
import MessageBubble from './MessageBubble'
import ProductCard from './ProductCard'
import PriceComparison from './PriceComparison'
import { useChat } from '../hooks/useChat'

function ChatInterface() {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  const { messages, loading, sessionId, sendMessage } = useChat()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Keep focus on input after message is sent
  useEffect(() => {
    if (!loading && inputRef.current) {
      inputRef.current.focus()
    }
  }, [loading, messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const message = input.trim()
    setInput('')
    
    // Keep focus on input immediately
    setTimeout(() => {
      if (inputRef.current) {
        inputRef.current.focus()
      }
    }, 0)
    
    await sendMessage(message, sessionId)
  }

  const handleNegativeFeedback = async () => {
    if (!sessionId || loading) return
    await sendMessage("je n'aime pas", sessionId)
  }

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <div className="border-b border-gray-200 bg-white px-4 py-3 shadow-sm">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
            <ShoppingBag className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900">BuyBuddy</h1>
            <p className="text-xs text-gray-500">Intelligent Shopping Agent</p>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-4xl mx-auto space-y-6">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                <ShoppingBag className="w-8 h-8 text-blue-600" />
              </div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                Bonjour ! Je suis BuyBuddy
              </h2>
              <p className="text-gray-600 mb-6">
                Dites-moi ce que vous cherchez et je vais trouver les meilleurs produits pour vous.
              </p>
              <div className="flex flex-wrap gap-2 justify-center">
                <button
                  onClick={() => setInput("laptop gaming sous 1500€")}
                  className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 transition-colors"
                >
                  💻 Laptop gaming sous 1500€
                </button>
                <button
                  onClick={() => setInput("smartphone Android avec bonne caméra")}
                  className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 transition-colors"
                >
                  📱 Smartphone Android
                </button>
                <button
                  onClick={() => setInput("écouteurs sans fil")}
                  className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 transition-colors"
                >
                  🎧 Écouteurs sans fil
                </button>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div key={index} className="space-y-4">
              {/* User Message */}
              <MessageBubble isUser={true}>
                {message.text}
              </MessageBubble>

              {/* Assistant Response */}
              {message.response && (
                <>
                  <MessageBubble isUser={false}>
                    <div className="space-y-4">
                      {/* Conversational Response - show only text, no products */}
                      {message.response.conversational_response ? (
                        <div className="text-gray-900 whitespace-pre-line">
                          {message.response.conversational_response}
                        </div>
                      ) : (
                        <>
                          {/* Error message - always show if present */}
                          {message.response.error && (
                            <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 text-sm">
                              <strong>Erreur:</strong> {message.response.error}
                            </div>
                          )}

                          {/* Product Message - contextual message from LLM */}
                          {message.response.product_message && (
                            <div className="text-gray-900 whitespace-pre-line mb-4">
                              {message.response.product_message}
                            </div>
                          )}
                          
                          {/* Show message even if no products but no error */}
                          {!message.response.error && !message.response.product_message && !message.response.products?.length && (
                            <div className="text-gray-600 text-sm italic">
                              Aucun produit trouvé pour cette recherche.
                            </div>
                          )}

                          {/* Price Comparison */}
                          {message.response.price_comparison?.recommendation && (
                            <PriceComparison comparison={message.response.price_comparison} />
                          )}

                          {/* Products Grid */}
                          {message.response.products && message.response.products.length > 0 && (
                        <div className="space-y-4">
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {message.response.products.map((product, idx) => (
                              <ProductCard key={idx} product={product} />
                            ))}
                          </div>

                          {/* Negative Feedback Button */}
                          {index === messages.length - 1 && sessionId && (
                            <div className="flex justify-center pt-2">
                              <button
                                onClick={handleNegativeFeedback}
                                disabled={loading}
                                className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm text-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                <ThumbsDown className="w-4 h-4" />
                                Je n'aime pas ces résultats
                              </button>
                            </div>
                          )}
                        </div>
                      )}
                        </>
                      )}
                    </div>
                  </MessageBubble>
                </>
              )}

              {/* Loading indicator */}
              {index === messages.length - 1 && loading && (
                <MessageBubble isUser={false}>
                  <div className="flex items-center gap-2 text-gray-600">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Recherche en cours...</span>
                  </div>
                </MessageBubble>
              )}
            </div>
          ))}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white px-4 py-4">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Dites-moi ce que vous cherchez..."
              className="flex-1 px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder-gray-500"
              disabled={loading}
              autoFocus
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-lg transition-colors flex items-center gap-2"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface

