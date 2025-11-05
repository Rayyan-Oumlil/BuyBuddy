import { User, Bot } from "lucide-react"

export const MessageBubble = ({ role, content }) => {
  const isUser = role === "user"

  // Always show the bubble, even if content is empty (for user messages)
  const displayContent = content || (isUser ? "" : "")

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
            ? "bg-chat-user text-chat-user-foreground dark:bg-white dark:text-black"
            : "bg-chat-assistant text-chat-assistant-foreground dark:text-white dark:bg-[#3a3a3a]"
        }`}
      >
        <p className="text-sm leading-relaxed whitespace-pre-wrap">{displayContent}</p>
      </div>
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-muted flex items-center justify-center shadow-card">
          <User className="w-5 h-5 text-muted-foreground" />
        </div>
      )}
    </div>
  )
}
