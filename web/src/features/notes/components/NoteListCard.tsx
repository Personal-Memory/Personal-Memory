// this page will be used to display one card of a note list, which will be used in the notes page to display a list of notes
import type { NoteListItem } from "../types/note.types"

interface NoteCardProps {
    note: NoteListItem;
    onClick: () => void;
}

function NoteListCard(
    { note, onClick }: NoteCardProps
) {
    const date = new Date(note.updated_at).toLocaleDateString();

    return (
        <button
            type="button"
            onClick={onClick}
            className="w-full rounded-xl border border-gray-200 bg-white p-5 text-left shadow-sm transition hover:border-gray-300 hover:shadow-md hover:cursor-pointer"    
        >   
            <h3 className="truncate text-lg font-semibold text-gray-900">
               {note.title} 
            </h3>

            <p className="mt-2 line-clamp-2 text-sm leading-6 text-gray-500">
                {note.content_text || "No content"}
            </p>

            <p className="mt-4 text-xs text-gray-400">
                Last Modified: {date}
            </p>
            
        </button>
    );
}

export default NoteListCard;