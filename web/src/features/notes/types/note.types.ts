export interface NoteListItem {
    id: number;
    title: string;
    content_text: string;
    created_at: string;
    updated_at: string;
}

export interface NoteCreateRequest {
    title: string;
    content_json: Record<string, unknown>;
}

export interface NoteResponse {
    id: number;
    user_id: number;
    title: string;
    content_json: Record<string, unknown>;
    content_text: string;
    created_at: string;
    updated_at: string;
}