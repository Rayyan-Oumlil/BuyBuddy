import { useState, useRef, useEffect } from "react";
import { Send, Loader2, ThumbsDown, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { MessageBubble } from "./MessageBubble";
import { ProductCard } from "./ProductCard";
import { PriceComparison } from "./PriceComparison";
import { useChat } from "@/hooks/useChat";

export const ChatInterface = () => {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { messages, isLoading, sendMessage } = useChat();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    await sendMessage(input);
    setInput("");
    inputRef.current?.focus();
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
    inputRef.current?.focus();
  };

  const suggestions = [
    "Trouve-moi un iPhone 15 Pro au meilleur prix",
    "Comparaison PS5 sur différentes plateformes",
    "Écouteurs sans fil moins de 100€",
  ];

  return (
    <div className="flex-1 flex flex-col h-screen bg-background">
      <div className="flex-1 overflow-y-auto">
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
                <MessageBubble role={message.role} content={message.content} />
                {message.priceComparison && (
                  <div className="ml-11">
                    <PriceComparison
                      bestDeal={message.priceComparison.best_deal}
                      priceRange={message.priceComparison.price_range}
                      totalCompared={message.priceComparison.total_compared}
                    />
                  </div>
                )}
                {message.productMessage && (
                  <div className="ml-11 text-sm text-muted-foreground animate-fade-in">
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
                    <Button variant="ghost" size="sm" className="text-muted-foreground">
                      <ThumbsDown className="w-4 h-4 mr-2" />
                      Je n'aime pas ces résultats
                    </Button>
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

      <div className="border-t border-border bg-background/95 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto p-4">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              ref={inputRef}
              type="text"
              placeholder="Que recherchez-vous aujourd'hui ?"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
              className="flex-1"
            />
            <Button type="submit" disabled={!input.trim() || isLoading} size="icon">
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};
