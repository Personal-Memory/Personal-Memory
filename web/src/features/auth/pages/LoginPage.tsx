import React from "react";
import LoginForm from "../components/LoginForm";

function LoginPage() {
  return (
    <main className="min-h-screen bg-gray-50 px-x py-12">
      <div className=" mx-auto max-w-md">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-semibold tracking-tight">Sign in</h1>

          <p className="mt-2 text-gray-600">
            Start building your personal memory.
          </p>
        </div>
        <LoginForm />
      </div>
    </main>
  );
}

export default LoginPage;
