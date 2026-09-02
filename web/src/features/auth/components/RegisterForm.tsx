import { useState } from "react";
import type { FormEvent } from "react";

import { useNavigate } from "react-router-dom";

import { register } from "../services/authService";

function RegisterForm() {
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    
    const navigate = useNavigate();
    
    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        setError("");

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        if (password.length < 8) {
            setError("Password must be at least 8 characters long.");
            return;
        }

        setIsLoading(true);

        try {
            const user = await register({
                username,
                email,
                password,
                first_name: firstName,
                last_name: lastName,
            });

            navigate("/");
        } catch (error) {
            if (error instanceof Error) {
                setError(error.message)
            } else {
                setError("Something went wrong. Please try again.")
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <form 
            onSubmit={handleSubmit}
            className="space-y-5 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm"
        >
            <div>
                <label
                    htmlFor="firstName"
                    className="mb-2 block text-sm font-medium text-gray-700"
                >
                    First Name
                </label>
                <input
                    id="firstName"
                    name="firstName"
                    type="text"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    required
                    className="w-full rounded-lg border border-gray-300 px-3 py-2.5 outline-none focus:border-black"
                />
            </div>

            <div>
                <label
                    htmlFor="lastName"
                    className="mb-2 block text-sm font-medium text-gray-700"
                >
                    Last Name
                </label>
                <input
                    id="lastName"
                    name="lastName"
                    type="text"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    required
                    className="w-full rounded-lg border border-gray-300 px-3 py-2.5 outline-none focus:border-black"
                />                     
            </div>

            <div>
                <label
                    htmlFor="username"
                    className="mb-2 block text-sm font-medium text-gray-700"
                >
                    Username
                </label>

                <input
                    id="username"
                    name="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    className="w-full rounded-lg border border-gray-300 px-3 py-2.5 outline-none focus:border-black"
                />
            </div>

            <div>
                <label
                    htmlFor="email"
                    className="mb-2 block text-sm font-medium text-gray-700"
                >
                    Email
                </label>

                <input
                    id="email"
                    name="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
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

            <div>
                <label
                    htmlFor="confirmPassword"
                    className="mb-2 block text-sm font-medium text-gray-700"
                >
                    Confirm Password
                </label>

                <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    className="w-full rounded-lg border border-gray-300 px-3 py-2.5 outline-none focus:border-black"
                />
            </div>

            {error && (
                <p className="text-sm text-red-600">
                    {error}
                </p>
            )}

            <button
                type="submit"
                disabled={isLoading}
                className="w-full rounded-lg bg-black px-4 py-2.5 font-medium text-white hover:bg-gray-800"
            >
                {isLoading ? "Creating Account..." : "Create Account"}
            </button>
        </form>

    );
}

export default RegisterForm;