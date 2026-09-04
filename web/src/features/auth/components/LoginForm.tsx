import React, { type FormEvent } from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/authService";

function LoginForm() {
  const [identifier, setIdentifier] = useState("");
  // const[email, setEmail] = useState("")
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();
  const isEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(identifier);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);
    try {
      const loggedUser = await login({
        username: isEmail ? null : identifier,
        email: isEmail ? identifier : null,
        password,
      });
      localStorage.setItem("access_token", loggedUser.access_token);
      navigate("/dashboard");
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <form
      className="space-y-5 rounded-2xl border border-gray-200 bg-white p-6 shadow-md"
      onSubmit={handleSubmit}
    >
      <div>
        <label
          htmlFor="identifier"
          className="mb-2 block text-sm font-medium text-gray-700"
        >
          Email or Username
        </label>
        <input
          id="identifier"
          name="identifier"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          type="text"
          required
          className="w-full rounded-lg border border-gray-300 px-3 py-2.5 outline-none focus:border-black"
        />
      </div>
      <div>
        <label
          htmlFor="password"
          className="mb-2 block text-sm font-medium text-gray-700"
        >
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full rounded-lg border border-gray-300 px-3 py-2.5 outline-none focus:border-black"
        />
      </div>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full rounded-lg bg-black px-4 py-2.5 font-medium text-white hover:bg-gray-800"
      >
        {isLoading ? "Logging in ..." : "Login"}
      </button>
    </form>
  );
}

export default LoginForm;
