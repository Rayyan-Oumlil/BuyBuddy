import { Plus, MessageSquare } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useEffect, useState } from "react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { toast } from "@/hooks/use-toast"
import axios from "axios"

const API_BASE_URL = "/api/v1"

export const ConversationSidebar = ({
  onNewConversation,
  onLoadConversation,
  currentSessionId,
}) => {
  const [conversations, setConversations] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    loadConversations()
  }, [])

  const loadConversations = async () => {
    setIsLoading(true)
    try {
      const response = await axios.get(`${API_BASE_URL}/history/conversations?limit=50`)
      const data = response.data || []
      
      // Group by session_id and keep only the first message of each session
      const uniqueConversations = Object.values(
        data.reduce((acc, conv) => {
          if (!acc[conv.session_id]) {
            acc[conv.session_id] = conv
          }
          return acc
        }, {})
      )
      
      setConversations(uniqueConversations)
    } catch (error) {
      console.error("Error loading conversations:", error)
      toast({
        title: "Erreur",
        description: "Impossible de charger l'historique",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const formatDate = (timestamp) => {
    if (!timestamp) return ""
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))

    if (days === 0) return "Aujourd'hui"
    if (days === 1) return "Hier"
    if (days < 7) return `Il y a ${days} jours`
    return date.toLocaleDateString("fr-FR", { day: "numeric", month: "short" })
  }

  const generateTitle = (message) => {
    if (!message) return "Nouvelle conversation"
    
    // Extract product keywords
    const productKeywords = ["laptop", "phone", "dress", "robe", "shoes", "chaussures", "air force", "nike", "iphone", "smartphone"]
    const lowerMessage = message.toLowerCase()
    
    for (const keyword of productKeywords) {
      if (lowerMessage.includes(keyword)) {
        const index = lowerMessage.indexOf(keyword)
        const start = Math.max(0, index - 10)
        const end = Math.min(message.length, index + keyword.length + 20)
        return message.substring(start, end).trim() || message.substring(0, 30) + "..."
      }
    }
    
    return message.length > 30 ? message.substring(0, 30) + "..." : message
  }

  return (
    <div className="w-64 bg-sidebar border-r border-sidebar-border flex flex-col h-full dark:bg-[#121212] flex-shrink-0">
      {/* Logo */}
      <div className="w-full p-4">
        <img 
          src="/logo.png" 
          alt="BuyBuddy Logo" 
          className="w-full h-auto rounded-lg object-contain"
        />
      </div>
      
      <div className="p-4 border-b border-sidebar-border">
        <Button
          onClick={onNewConversation}
          className="w-full"
          size="sm"
        >
          <Plus className="w-4 h-4 mr-2" />
          Nouvelle conversation
        </Button>
      </div>

      <ScrollArea className="flex-1 p-2">
        <div className="space-y-1">
          {isLoading ? (
            <div className="p-4 text-center text-sm text-muted-foreground">
              Chargement...
            </div>
          ) : conversations.length === 0 ? (
            <div className="p-4 text-center text-sm text-muted-foreground">
              Aucune conversation
            </div>
          ) : (
            conversations.map((conv) => (
              <button
                key={conv.session_id}
                onClick={() => onLoadConversation(conv.session_id)}
                className={`w-full text-left p-3 rounded-lg transition-colors hover:bg-sidebar-accent group ${
                  currentSessionId === conv.session_id ? "bg-sidebar-accent" : ""
                }`}
              >
                <div className="flex items-start gap-2">
                  <MessageSquare className="w-4 h-4 mt-0.5 text-muted-foreground group-hover:text-sidebar-primary transition-colors flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium line-clamp-2 mb-1">
                      {generateTitle(conv.user_message)}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {formatDate(conv.timestamp || conv.created_at)}
                    </p>
                  </div>
                </div>
              </button>
            ))
          )}
        </div>
      </ScrollArea>
    </div>
  )
}
