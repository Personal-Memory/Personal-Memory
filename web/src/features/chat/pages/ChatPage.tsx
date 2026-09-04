import Sidebar from "../components/Sidebar";
import ChatHeader from "../components/ChatHeader";
import ChatMessages from "../components/ChatMessages";
import ChatInput from "../components/ChatInput";

function ChatPage() {
    return (
        <div className="flex h-screen overflow-hidden bg-white">
            <Sidebar />

            <main className="flex min-w-0 flex-1 flex-col">
                <ChatHeader />

                <ChatMessages />

                <ChatInput />
            </main>
        </div>
    );
}

export default ChatPage;