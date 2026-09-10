import { apiRequestWithAuth } from "../../../lib/api"
import type { NoteCreateRequest, NoteResponse, NoteListItem } from "../types/note.types"

export async function createNote(
    data: NoteCreateRequest,
): Promise<NoteResponse> {
    return apiRequestWithAuth<NoteResponse>("/notes", {
        method: "POST",
        body: JSON.stringify(data)
    })
}

export async function getNotes(): Promise<NoteListItem[]> {
    return apiRequestWithAuth<NoteListItem[]>("/notes");
}

export async function getNote(noteId: number): Promise<NoteResponse> {
    return apiRequestWithAuth<NoteResponse>(`/notes/${noteId}`);
}