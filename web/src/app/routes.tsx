import {createBrowserRouter} from "react-router-dom";

import HomePage from "../pages/HomePage";
import RegisterPage from "../features/auth/pages/RegisterPage";
import ChatPage from "../features/chat/pages/ChatPage";
import LoginPage from "../features/auth/pages/LoginPage";
import NotesPage from "../features/notes/pages/NotesPage";
import NewNotePage from "../features/notes/pages/NewNote";
import NoteDetailPage from "../features/notes/pages/NoteDetail";

import ProtectedRoute from "./ProtectedRoute";

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
        path: "/login",
        element: <LoginPage />
    },
    {
        element: <ProtectedRoute />,
        children: [
            {
                path: "/dashboard",
                element: <ChatPage />
            },
            {
                path: "/notes",
                element: <NotesPage />
            },
            {
                path: "/notes/new",
                element: <NewNotePage />
            },
            {
                path: "/notes/:noteId",
                element: <NoteDetailPage />
            }
        ]
    }
    

])