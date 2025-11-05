import { useState, useCallback, useEffect } from "react";
import { toast } from "@/hooks/use-toast";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  products?: Product[];
  priceComparison?: PriceComparison;
  productMessage?: string;
  timestamp: Date;
}

interface Product {
  name: string;
  price: number;
  link: string;
  platform: string;
  image?: string;
  description?: string;
}

interface PriceComparison {
  best_deal: {
    name: string;
    price: number;
    platform: string;
  };
  price_range: {
    min: number;
    max: number;
  };
  total_compared: number;
}

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (content: string) => {
      const userMessage: Message = {
        id: Date.now().toString(),
        role: "user",
        content,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);

      try {
        const response = await fetch("/api/v1/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: content,
            session_id: sessionId,
          }),
        });

        if (!response.ok) {
          throw new Error("Erreur lors de la communication avec le serveur");
        }

        const data = await response.json();

        if (data.error) {
          throw new Error(data.error);
        }

        setSessionId(data.session_id);

        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: data.conversational_response || "",
          products: data.products || [],
          priceComparison: data.price_comparison,
          productMessage: data.product_message,
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (error) {
        console.error("Error sending message:", error);
        toast({
          title: "Erreur",
          description:
            error instanceof Error
              ? error.message
              : "Une erreur est survenue lors de l'envoi du message",
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    },
    [sessionId]
  );

  const loadConversation = useCallback(async (conversationSessionId: string) => {
    try {
      setIsLoading(true);
      const [historyResponse, productsResponse] = await Promise.all([
        fetch(`/api/v1/history/conversations?session_id=${conversationSessionId}&limit=100`),
        fetch(`/api/v1/history/conversation/${conversationSessionId}/products`),
      ]);

      if (!historyResponse.ok || !productsResponse.ok) {
        throw new Error("Erreur lors du chargement de la conversation");
      }

      const history = await historyResponse.json();
      const products = await productsResponse.json();

      const loadedMessages: Message[] = [];

      history.forEach((item: any) => {
        loadedMessages.push({
          id: `${item.timestamp}-user`,
          role: "user",
          content: item.user_message,
          timestamp: new Date(item.timestamp),
        });

        const messageProducts = products.filter(
          (p: any) => p.search_query === item.structured_query
        );

        loadedMessages.push({
          id: `${item.timestamp}-assistant`,
          role: "assistant",
          content: item.assistant_response,
          products: messageProducts,
          timestamp: new Date(item.timestamp),
        });
      });

      setMessages(loadedMessages);
      setSessionId(conversationSessionId);
    } catch (error) {
      console.error("Error loading conversation:", error);
      toast({
        title: "Erreur",
        description: "Impossible de charger la conversation",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  }, []);

  const startNewConversation = useCallback(() => {
    setMessages([]);
    setSessionId(null);
  }, []);

  return {
    messages,
    isLoading,
    sessionId,
    sendMessage,
    loadConversation,
    startNewConversation,
  };
};
