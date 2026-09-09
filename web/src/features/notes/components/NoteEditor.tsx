import { useEditor, EditorContent } from "@tiptap/react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import StarterKit from "@tiptap/starter-kit";

import NoteToolbar from "./NoteToolbar";
import "./note-editor.css";
import { createNote } from "../services/noteService";

interface NoteEditorProps {
    initialContent?: Record<string, unknown>;
    editable?: boolean;
    initialTitle?: string;
}



function NoteEditor({ initialContent, editable, initialTitle }: NoteEditorProps) {
    const [title, setTitle] = useState(initialTitle ?? "");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const editor = useEditor({
        extensions: [
            StarterKit,
        ],

        editable: editable,
        content: initialContent ??  `<p> Start Writing...</p>`,
    });

    const handleSave = () => {
        console.log(editor.getJSON());
        try{
            createNote({
                title: title,
                content_json: editor.getJSON(),
            })
        
            navigate("/notes", {
                state: { refresh: true }
            });
        } catch (error) {
            if (error instanceof Error) {
                setError(error.message)
            } else {
                setError("Something went wrong. Please try again.")
            }
        } finally {
            setError("");
        }
    }

    return (
        <div className="min-h-full">
            
            {editable && 
            <button
                type="button"
                onClick={handleSave}
                // the button should be on the right side, so on classname we 
                className="mb-4 rounded-lg bg-gray-900 px-4 py-2 text-sm text-white hover:bg-gray-800 float-right hover:cursor-pointer"
            >
                Save
            </button>
            }
            

            {error && <p className="text-red-500">{error}</p>}
            
            {editable &&
                <div className="border-b p-4">
                    <input 
                        id="title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        type="text"
                        placeholder="Enter note title"
                        required
                        name="title"
                        className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:ring focus:ring-blue-200"
                    />
                </div>
            }

            {editable && <NoteToolbar editor={editor} />}
            <EditorContent editor={editor} />
        </div>
    );
}

export default NoteEditor;