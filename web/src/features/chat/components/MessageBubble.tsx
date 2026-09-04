interface MessageBubbleProps {
    role: "user" | "assistant";
    content: string;
}

function MessageBubble({
    role,
    content,
} : MessageBubbleProps) {
    const isUser = role === "user";

    return (
        <div
            className={`flex ${isUser ? "justify-end" : "justify-start"}`}
        >
            <div 
                className={`max-w-2xl rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                    isUser ? "bg-gray-900 text-white" : "bg-gray-100 text-gray-900"
                }`}
            >
                {content}
            </div>
        </div>
    );
}

export default MessageBubble;