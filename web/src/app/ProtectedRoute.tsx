import { Navigate, Outlet, useLocation } from "react-router-dom";
import { getCurrentUser } from "../features/auth/services/authService";
import { useEffect, useState } from "react";

function ProtectedRoute() {
    const location = useLocation();

    const [loading, setLoading] = useState(true);
    const [authenticated, setAuthenticated] = useState(false);

    
    useEffect(() => {
        async function checkAuth() {
            const access_token = localStorage.getItem("access_token");
            
            if (!access_token) {
                setAuthenticated(false);
                setLoading(false);
                return;
            }

            try {
                await getCurrentUser();
                setAuthenticated(true);
            } catch (error) {
                setAuthenticated(false);
            } finally {
                setLoading(false);
            }
        }

        checkAuth();
    }, []);

    if (loading) {
        return (
            <div className="flex min-h-screen items-center justify-center">
                <p className="text-sm text-gray-500">
                    Loading...
                </p>
            </div>
        );
    }

    if (!authenticated) {
        return (
            <Navigate
                to="/login"
                replace
                state={{ from: location }}
            />
        );
    }

    return <Outlet />;
}

export default ProtectedRoute;