import { ChatInterface } from "./components/ChatInterface"
import { ConversationSidebar } from "./components/ConversationSidebar"
import { useChat } from "./hooks/useChat"
import { Toaster } from "./components/ui/toaster"

function App() {
  const chatHook = useChat()

  return (
    <div className="flex w-full h-screen bg-background overflow-hidden">
      <Toaster />
      <ConversationSidebar
        onNewConversation={chatHook.startNewConversation}
        onLoadConversation={chatHook.loadConversation}
        currentSessionId={chatHook.sessionId}
      />
      <ChatInterface chatHook={chatHook} />
    </div>
  )
}

export default App
