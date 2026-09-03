import RegisterForm from "../components/RegisterForm";
function RegisterPage(){
    return (
        <main className="min-h-screen bg-gray-50 px-6 py-12">
            <div className="mx-auto max-w-md">
                <div className="mb-8 text-center">
                    <h1 className="text-3xl font-semibold tracking-tight">
                        Create your account
                    </h1>

                    <p className="mt-2 text-gray-600">
                        Start building your personal memory.
                    </p>
                </div>

                <RegisterForm />
            </div>
        </main>
    );
}
export default RegisterPage;