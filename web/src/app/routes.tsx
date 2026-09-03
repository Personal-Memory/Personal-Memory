import {createBrowserRouter} from "react-router-dom";

import HomePage from "../pages/HomePage";
import RegisterPage from "../features/auth/pages/RegisterPage";
import ChatPage from "../features/chat/pages/ChatPage";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <HomePage />
    },
    {
        path: "/register",
        element: <RegisterPage />
    },
    {
        path: "/dashboard",
        element: <ChatPage />
    }
])