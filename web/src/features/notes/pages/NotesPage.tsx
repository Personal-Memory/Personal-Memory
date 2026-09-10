import { useEffect, useState }  from 'react';
import { useNavigate } from "react-router-dom";

import { getNotes } from '../services/noteService';
import type { NoteListItem } from '../types/note.types';
import NoteList from '../components/NoteList';

function NotesPage() {
    const navigate = useNavigate();

    const [notes, setNotes] = useState<NoteListItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function loadNotes() {
            try {
                const data = await getNotes();
                setNotes(data);
            } catch (error) {
                setError(
                    error instanceof Error
                        ? error.message
                        : "Failed to load notes.",
                );
            } finally {
                setLoading(false);
            }
        }

        loadNotes();
    }, []);

    const handleNewNote = () => {
        navigate("/notes/new");
    }

    const handleNoteClick = (noteId: number) => {
        navigate(`/notes/${noteId}`);
    };
    
    if (loading) {
        return (
            <div className="p-8">
                <p className="text-sm text-gray-500">Loading notes...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-8">
                <p className="text-sm text-red-500">{error}</p>
            </div>
        );
    }

    return (
        <div className="p-8">
            <div className="mb-8 flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">
                        Notes
                    </h1>

                    <p className="mt-1 text-sm text-gray-500">
                        Your personal knowledge and memories.
                    </p>
                </div>

                <button
                    type="button"
                    onClick={handleNewNote}
                    className="rounded-lg bg-black px-4 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800 hover:cursor-pointer"
                >
                    + New Note
                </button>
            </div>

            <NoteList
                notes={notes}
                onNoteClick={handleNoteClick}
            />
        </div>
    );
}

export default NotesPage;