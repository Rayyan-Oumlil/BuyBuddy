import { useState, useRef, useEffect } from "react"
import { Send, Loader2, ThumbsDown, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { MessageBubble } from "./MessageBubble"
import { ProductCard } from "./ProductCard"
import { PriceComparison } from "./PriceComparison"
import { DarkModeToggle } from "./DarkModeToggle"
import { useChat } from "@/hooks/useChat"

export const ChatInterface = ({ chatHook }) => {
  const [input, setInput] = useState("")
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  
  // Use chatHook from props or fallback to useChat
  const { messages, isLoading, sessionId, sendMessage } = chatHook || useChat()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (!isLoading && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isLoading, messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    await sendMessage(input)
    setInput("")
    setTimeout(() => {
      inputRef.current?.focus()
    }, 0)
  }

  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion)
    inputRef.current?.focus()
  }

  const handleNegativeFeedback = async () => {
    if (!sessionId || isLoading) return
    await sendMessage("je n'aime pas")
  }

  const suggestions = [
    "laptop gaming sous 1500€",
    "smartphone Android",
    "écouteurs sans fil",
  ]

  return (
    <div className="flex-1 flex flex-col h-full bg-background dark:bg-[#2a2a2a] overflow-hidden">
      {/* Header with dark mode toggle */}
      <div className="border-b border-border bg-background/95 backdrop-blur-sm px-4 py-3 flex justify-end">
        <DarkModeToggle />
      </div>
      
      <div className="flex-1 overflow-y-auto pb-24">
        <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-8 animate-fade-in">
              <div className="relative">
                <div className="w-20 h-20 rounded-full bg-gradient-primary flex items-center justify-center shadow-hover">
                  <Sparkles className="w-10 h-10 text-white" />
                </div>
                <div className="absolute -inset-4 bg-gradient-primary opacity-20 blur-xl rounded-full animate-pulse"></div>
              </div>
              <div className="text-center space-y-2">
                <h1 className="text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent">
                  BuyBuddy
                </h1>
                <p className="text-muted-foreground max-w-md">
                  Votre assistant intelligent pour trouver les meilleurs prix et comparer les
                  produits en un instant
                </p>
              </div>
              <div className="space-y-2 w-full max-w-md">
                <p className="text-sm text-muted-foreground text-center">Essayez par exemple :</p>
                <div className="space-y-2">
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => handleSuggestionClick(suggestion)}
                      className="w-full text-left p-3 rounded-lg bg-muted hover:bg-muted/80 transition-all duration-200 text-sm hover:shadow-card"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <div key={message.id} className="space-y-4">
                <MessageBubble role={message.role} content={message.content || ""} />
                {message.priceComparison && (
                  <div className="ml-11">
                    <PriceComparison
                      bestDeal={message.priceComparison.best_deal}
                      priceRange={message.priceComparison.price_range}
                      totalCompared={message.priceComparison.total_compared}
                    />
                  </div>
                )}
                {message.productMessage && message.role === "assistant" && (
                  <div className="ml-11 text-sm text-muted-foreground dark:text-white animate-fade-in">
                    {message.productMessage}
                  </div>
                )}
                {message.products && message.products.length > 0 && (
                  <div className="ml-11 space-y-3">
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                      {message.products.map((product, index) => (
                        <ProductCard key={index} {...product} />
                      ))}
                    </div>
                    {message.role === "assistant" && (
                      <Button variant="ghost" size="sm" className="text-muted-foreground" onClick={handleNegativeFeedback} disabled={isLoading}>
                        <ThumbsDown className="w-4 h-4 mr-2" />
                        Je n'aime pas ces résultats
                      </Button>
                    )}
                  </div>
                )}
                {message.error && (
                  <div className="ml-11 bg-destructive/10 border border-destructive/20 rounded-lg p-3 text-sm text-destructive">
                    {message.error}
                  </div>
                )}
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex gap-3 justify-start animate-fade-in">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-primary flex items-center justify-center shadow-card">
                <Loader2 className="w-5 h-5 text-white animate-spin" />
              </div>
              <div className="bg-chat-assistant text-chat-assistant-foreground px-4 py-3 rounded-2xl shadow-card">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
                  <div
                    className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                    style={{ animationDelay: "0.1s" }}
                  ></div>
                  <div
                    className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  ></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="fixed bottom-0 left-0 right-0 bg-background/95 backdrop-blur-sm pb-6 dark:bg-[#171717]/95">
        <div className="max-w-4xl mx-auto px-4">
          <form onSubmit={handleSubmit} className="flex gap-3 items-end justify-center">
            <div className="flex-1 max-w-2xl transition-all duration-500 ease-out">
              <Input
                ref={inputRef}
                type="text"
                placeholder="Que recherchez-vous aujourd'hui ?"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={isLoading}
                className="w-full border-0 bg-muted/50 dark:bg-[#2a2a2a] focus:bg-muted dark:focus:bg-[#3a3a3a] focus:ring-0 rounded-full px-6 py-5 text-base transition-all duration-500 shadow-lg hover:shadow-xl focus:shadow-2xl"
              />
            </div>
            <Button 
              type="submit" 
              disabled={!input.trim() || isLoading} 
              size="icon"
              className="h-11 w-11 rounded-full bg-primary hover:bg-primary/90 transition-all duration-300 shadow-lg hover:shadow-xl shrink-0"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
