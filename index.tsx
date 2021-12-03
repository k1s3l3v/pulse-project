import React, { createContext, ReactNode, useContext, useEffect, useMemo, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { User } from '../types';
import AuthService, { parseQueryString } from '../services/AuthService';
import { color_light_blue } from '../utils/constants';
import Loader from 'react-loader-spinner';
import './index.scss';

interface AuthContextType {
    user?: User;
    token?: string;
    isAuthenticated?: boolean;
    error?: any;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export function AuthProvider({ children }: { children: ReactNode }): JSX.Element {
    const [user, setUser] = useState<User>();
    const [error, setError] = useState<any>();
    const [token, setToken] = useState<string>('');
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [loadingInitial, setLoadingInitial] = useState<boolean>(true);
    const location = useLocation();

    useEffect(() => {
        if (AuthService.getUserLocal() === null || AuthService.getAuthToken() === null) {
            if (location.pathname === '/auth') {
                if (location.search === '') AuthService.authorize();
                if (location.search !== '') {
                    const query = parseQueryString(location.search);
                    if (query.code) {
                        AuthService.getTokenRequest(
                            query.code,
                            () => window.location.replace('/'),
                            e => setError(e)
                        );
                    } else if (query.error) {
                        setError(query.error);
                    } else AuthService.authorize();
                }
            } else AuthService.authorize();
        }
        setUser(AuthService.getUserLocal() as User);
        setToken(AuthService.getAuthToken() as string);
        setIsAuthenticated(AuthService.isAuthenticated);
        setLoadingInitial(false);
    }, [location.pathname]);

    const memoedValue = useMemo(
        () => ({
            user,
            token,
            isAuthenticated,
            error,
        }),
        [user, token, isAuthenticated, error]
    );

    return (
        <AuthContext.Provider value={memoedValue}>
            {!loadingInitial && children}
        </AuthContext.Provider>
    );
}

export default function useAuth() {
    return useContext(AuthContext);
}

export const AuthPage = () => {
    return (
        <div className="auth-page">
            <Loader type="TailSpin" color={color_light_blue} height={80} width={80} />
        </div>
    );
};
