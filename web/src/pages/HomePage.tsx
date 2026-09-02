import { Link } from "react-router-dom";

function HomePage() {
    return (
        <div className="min-h-screen bg-white text-gray-900">
            <header className="border-b border-gray-200">
                <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
                    <Link to="/" className="text-xl font-semibold">
                        Personal Memory
                    </Link>

                    <div className="flex items-center gap-3">
                        <Link
                            to="/login"
                            className="rounded-lg px-4 py-2 text-sm font-medium hover:bg-gray-100"
                        >
                            Sign in
                        </Link>

                        <Link
                            to="/register"
                            className="rounded-lg px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 bg-gray-900"
                        >
                            Sign up
                        </Link>
                    </div>
                </nav>
            </header>

            <main className = "mx-auto flex min-h-[calc(100vh-73px)] max-w-7xl items-center px-6">
                <div className="max-w-3xl">
                    <h1 className="text-5xl font-semibold tracking-tight sm:text-6xl">
                        Your memory, always with you.
                    </h1>

                    <p className="mt-6 max-w-2xl text-lg leading-8 text-gray-600">
                        Capture what you learn, experience, and remember. Then talk to your memories with AI.
                    </p>

                    <div className="mt-8">
                        <Link
                            to="/register"
                            className="rounded-lg bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                        >
                            Get started
                        </Link>
                    </div>
                </div>
            </main>
        </div>
    )
}

export default HomePage;