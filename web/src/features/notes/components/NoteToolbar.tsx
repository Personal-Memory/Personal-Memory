import type { Editor } from "@tiptap/react";
import {useEditorState} from "@tiptap/react";

interface NoteToolbarProps {
    editor: Editor | null;
}

function NoteToolbar({ editor }: NoteToolbarProps) {
    if (!editor) {
        return null;
    }

    const active = useEditorState({
        editor,
        selector: ({editor}) => ({
            bold: editor.isActive("bold"),
            italic: editor.isActive("italic"),
            strike: editor.isActive("strike"),
            h1: editor.isActive("heading", { level: 1 }),
            h2: editor.isActive("heading", { level: 2 }),
            h3: editor.isActive("heading", { level: 3 }),
            bulletList: editor.isActive("bulletList"),
            orderedList: editor.isActive("orderedList"),
            blockquote: editor.isActive("blockquote"),
            codeBlock: editor.isActive("codeBlock"),
        })
    })

    return (
        <div className="flex items-center gap-1 border-b border-gray-200 px-3 py-2">
            {/* Bold */}
            <button
                type="button"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() => editor.chain().focus().toggleBold().run()}
                className={`rounded px-3 py-1.5 text-sm font-bold hover:bg-gray-100 ${
                    active.bold ? "bg-gray-200" : ""
                }`}
            >
                B
            </button>

            {/* Italic */}
            <button
                type="button"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() => editor.chain().focus().toggleItalic().run()}
                className={`rounded px-3 py-1.5 text-sm italic hover:bg-gray-100 ${
                    active.italic ? "bg-gray-200" : ""
                }`}
            >
                I
            </button>

            {/* Strike */}
            <button
                type="button"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() => editor.chain().focus().toggleStrike().run()}
                className={`rounded px-3 py-1.5 text-sm line-through hover:bg-gray-100 ${
                    active.strike ? "bg-gray-200" : ""
                }`}
            >
                S
            </button>

            <div className="mx-1 h-6 w-px bg-gray-200" />

            {/* Heading 1 */}
            <button
                type="button"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() =>
                    editor.chain().focus().toggleHeading({ level: 1 }).run()
                }
                className={`rounded px-3 py-1.5 text-sm font-semibold hover:bg-gray-100 ${
                    active.h1 ? "bg-gray-200" : ""
                }`}
            >
                H1
            </button>

            {/* Heading 2 */}
            <button
                type="button"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() =>
                    editor.chain().focus().toggleHeading({ level: 2 }).run()
                }
                className={`rounded px-3 py-1.5 text-sm font-semibold hover:bg-gray-100 ${
                    active.h2 ? "bg-gray-200" : ""
                }`}
            >
                H2
            </button>

            {/* Heading 3 */}
            <button
                type="button"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() =>
                    editor.chain().focus().toggleHeading({ level: 3 }).run()
                }
                className={`rounded px-3 py-1.5 text-sm font-semibold hover:bg-gray-100 ${
                    active.h3 ? "bg-gray-200" : ""
                }`}
            >
                H3
            </button>

            <div className="mx-1 h-6 w-px bg-gray-200" />

            {/* Bullet list */}
            <button
                type="button"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() =>
                    editor.chain().focus().toggleBulletList().run()
                }
                className={`rounded px-3 py-1.5 text-sm hover:bg-gray-100 ${
                    active.bulletList ? "bg-gray-200" : ""
                }`}
            >
                • List
            </button>

            {/* Ordered list */}
            <button
                type="button"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() =>
                    editor.chain().focus().toggleOrderedList().run()
                }
                className={`rounded px-3 py-1.5 text-sm hover:bg-gray-100 ${
                    active.orderedList ? "bg-gray-200" : ""
                }`}
            >
                1. List
            </button>

            <div className="mx-1 h-6 w-px bg-gray-200" />

            {/* Blockquote */}
            <button
                type="button"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() =>
                    editor.chain().focus().toggleBlockquote().run()
                }
                className={`rounded px-3 py-1.5 text-sm hover:bg-gray-100 ${
                    active.blockquote ? "bg-gray-200" : ""
                }`}
            >
                Quote
            </button>

            {/* Code block */}
            <button
                type="button"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() =>
                    editor.chain().focus().toggleCodeBlock().run()
                }
                className={`rounded px-3 py-1.5 text-sm font-mono hover:bg-gray-100 ${
                    active.codeBlock ? "bg-gray-200" : ""
                }`}
            >
                Code
            </button>
        </div>
    );
}

export default NoteToolbar;