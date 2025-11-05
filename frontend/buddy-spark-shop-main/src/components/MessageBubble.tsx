import { User, Bot } from "lucide-react";

interface MessageBubbleProps {
  role: "user" | "assistant";
  content: string;
}

export const MessageBubble = ({ role, content }: MessageBubbleProps) => {
  const isUser = role === "user";

  return (
    <div className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"} animate-fade-in`}>
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-primary flex items-center justify-center shadow-card">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}
      <div
        className={`max-w-[80%] px-4 py-3 rounded-2xl shadow-card transition-all duration-200 hover:shadow-hover ${
          isUser
            ? "bg-chat-user text-chat-user-foreground"
            : "bg-chat-assistant text-chat-assistant-foreground"
        }`}
      >
        <p className="text-sm leading-relaxed whitespace-pre-wrap">{content}</p>
      </div>
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-muted flex items-center justify-center shadow-card">
          <User className="w-5 h-5 text-muted-foreground" />
        </div>
      )}
    </div>
  );
};
