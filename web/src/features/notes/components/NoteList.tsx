import type { NoteListItem } from "../types/note.types"
import NoteListCard from "./NoteListCard"

interface NoteListProps {
    notes: NoteListItem[];
    onNoteClick: (noteId: number) => void;
}

function NoteList({ notes, onNoteClick }: NoteListProps) {
    if (notes.length === 0) {
        return (
            <div className="flex min-h-[300px] items-center justify-center rounded-xl border border-dashed border-gray-300">
                <div className="text-center">
                    <h3 className="text-lg font-medium text-gray-900">
                        No notes yet
                    </h3>

                    <p className="mt-1 text-sm text-gray-500">
                        Create your first note to get started.
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {notes.map( (note) => (
                <NoteListCard
                    key={note.id}
                    note={note}
                    onClick={() => onNoteClick(note.id)}
                />
            ))}
        </div>
    );
}

export default NoteList;