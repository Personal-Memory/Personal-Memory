const conversations = [
    "My Machine Learning Course",
    "Personal Memory Project",
    "Ethiopian Travel",
    "Portfolio ideas",
]

function Sidebar() {
    return (
        <aside className="flex h-full w-64 flex-col border-r border-gray-200 bg-gray-50">
            {/* Logo */}
            <div className="border-b border-gray-200 px-5 py-4">
                <h1 className="text-lg font-semibold text-gray-900">
                    Personal Memory
                </h1>
            </div>

            {/* New Chat */}
            <div className="p-4">
                <button className="w-full rounded-lg bg-gray-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800">
                    + New Chat
                </button>
            </div>

            {/* Navigation */}
            <nav className="px-3">
                <button className="w-full rounded-lg px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-200">
                    Notes
                </button>

                <button className="mt-1 w-full rounded-lg px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-200">
                    Chat History
                </button>
            </nav>

            {/* Conversations */}
            <div className="mt-6 flex-1 overflow-y-auto px-3">
                <p className="px-3 pb-2 text-xs font-medium uppercase tracking-wide text-gray-400">
                    Recent Chats
                </p>

                <div className="space-y-1">
                    {conversations.map((conversation) => (
                        <button
                            key={conversation}
                            className="w-full truncate rounded-lg px-3 py-2 text-left text-sm text-gray-600 hover:bg-gray-200"
                        >
                            {conversation}
                        </button>
                    ))}
                </div>
            </div>

            {/* Bottom section */}
            <div className="border-t border-gray-200 p-3">
                <button className="w-full rounded-lg px-3 py-2 text-left text-sm text-gray-600 hover:bg-gray-200">
                    Settings
                </button>
            </div>
        </aside>
    );
}

export default Sidebar;