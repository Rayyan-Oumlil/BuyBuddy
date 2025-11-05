import { Plus, MessageSquare } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DarkModeToggle } from "./DarkModeToggle";
import { useEffect, useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { toast } from "@/hooks/use-toast";

interface Conversation {
  session_id: string;
  user_message: string;
  timestamp: string;
}

interface ConversationSidebarProps {
  onNewConversation: () => void;
  onLoadConversation: (sessionId: string) => void;
  currentSessionId: string | null;
}

export const ConversationSidebar = ({
  onNewConversation,
  onLoadConversation,
  currentSessionId,
}: ConversationSidebarProps) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("/api/v1/history/conversations?limit=50");
      if (!response.ok) throw new Error("Erreur lors du chargement");
      const data = await response.json();
      
      // Group by session_id and keep only the first message of each session
      const uniqueConversations = Object.values(
        data.reduce((acc: any, conv: Conversation) => {
          if (!acc[conv.session_id]) {
            acc[conv.session_id] = conv;
          }
          return acc;
        }, {})
      ) as Conversation[];
      
      setConversations(uniqueConversations);
    } catch (error) {
      console.error("Error loading conversations:", error);
      toast({
        title: "Erreur",
        description: "Impossible de charger l'historique",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days === 0) return "Aujourd'hui";
    if (days === 1) return "Hier";
    if (days < 7) return `Il y a ${days} jours`;
    return date.toLocaleDateString("fr-FR", { day: "numeric", month: "short" });
  };

  return (
    <div className="w-64 bg-sidebar border-r border-sidebar-border flex flex-col h-screen">
      <div className="p-4 border-b border-sidebar-border space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
              <span className="text-white font-bold text-sm">BB</span>
            </div>
            <span className="font-bold text-lg">BuyBuddy</span>
          </div>
          <DarkModeToggle />
        </div>
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
                      {conv.user_message}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {formatDate(conv.timestamp)}
                    </p>
                  </div>
                </div>
              </button>
            ))
          )}
        </div>
      </ScrollArea>
    </div>
  );
};

