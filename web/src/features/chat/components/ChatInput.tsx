import {useState} from "react";

function ChatInput() {
    
    const [message, setMessage] = useState("");

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        
        event.preventDefault();
    
        if (!message.trim()) {
            return;
        }

        console.log("Message:", message);

        setMessage("");
    };

    return (
        <div className="border-t border-gray-200 p-4">
            <form
                onSubmit={handleSubmit}
                className="mx-auto flex max-w-3xl items-end gap-3"
            >
                <textarea
                    value={message}
                    onChange={(event) => setMessage(event.target.value)}
                    placeholder="Type your message here..."
                    rows={1}
                    className="max-h-32 min-h-12 flex-1 resize-none rounded-xl border border-gray-300 px-4 py-3 text-sm outline-none transition focus:border-gray-500 focus:ring-2 focus:ring-gray-200"
                />

                <button
                    type="submit"
                    disabled={!message.trim()}
                    className="rounded-xl bg-gray-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-40"
                >
                    Send
                </button>
                
            </form>
        </div>
    )

}

export default ChatInput;
