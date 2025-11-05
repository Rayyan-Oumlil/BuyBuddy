import { ChatInterface } from "@/components/ChatInterface";
import { ConversationSidebar } from "@/components/ConversationSidebar";
import { useChat } from "@/hooks/useChat";

const Index = () => {
  const { sessionId, loadConversation, startNewConversation } = useChat();

  return (
    <div className="flex w-full min-h-screen">
      <ConversationSidebar
        onNewConversation={startNewConversation}
        onLoadConversation={loadConversation}
        currentSessionId={sessionId}
      />
      <ChatInterface />
    </div>
  );
};

export default Index;
