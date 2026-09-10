import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import type { NoteResponse } from "../types/note.types";
import { getNote } from "../services/noteService";
import NoteEditor from "../components/NoteEditor";


function NoteDetailPage() {
    const { noteId } = useParams<{ noteId: string }>();
    const navigate = useNavigate();
    
    const [note, setNote] = useState<NoteResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!noteId) {
            setError("Note ID is missing.");
            setLoading(false);
            return;
        }

        async function loadNote() {
            try {
                const data = await getNote(Number(noteId));
                setNote(data);
            } catch (error) {
                setError(
                    error instanceof Error 
                        ? error.message
                        : "Failed to fetch note details."
                );
            } finally {
                setLoading(false);
            }
        }

        loadNote();
    }, [noteId]);

    if (loading) {
        return (
            <div className="p-8">
                <p>Loading note details...</p> 
            </div>
        );
    }

    if (error || !note) {
        return (
            <div className="p-8">
                <button
                    type="button"
                    onClick={() => navigate("/notes")}
                    className="mb-6 text-sm text-gray-500 hover:text-gray-900"
                >
                    ← Back to notes
                </button>

                <p className="text-sm text-red-500">
                    {error ?? "Note not found."}
                </p>
            </div>
        );
    }

    return (
        <div className="p-8">
            <div className="mb-6">
                <button
                    type="button"
                    onClick={() => navigate("/notes")}
                    className="text-sm text-gray-500 hover:text-gray-900"
                >
                    ← Back to notes
                </button>
            </div>

            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900">
                    {note.title}
                </h1>

                <p className="mt-2 text-sm text-gray-400">
                    Updated{" "}
                    {new Date(note.updated_at).toLocaleDateString()}
                </p>
            </div>

            <NoteEditor
                initialContent={note.content_json}
                editable={false}
            />
        </div>
    );
}

export default NoteDetailPage;