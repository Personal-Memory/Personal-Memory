import NoteEditor from "../components/NoteEditor";

function NewNotePage() {
    return (
        <div className="flex h-screen flex-col">
            
            <header className="border-b p-4">
                <h1 className="text-2xl font-bold">New Note</h1>
            </header>

            <main className="flex-1 overflow-y-auto px-8 py-6">
                <NoteEditor editable={true} />
            </main> 
        </div>
    );
}

export default NewNotePage;