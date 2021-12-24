import BaseService from './BaseService';
import { User } from '../types';

export const parseQueryString = (str: string) => {
    if (!str) return {};
    const arr = str.split('&');
    arr.forEach((v, i, _arr) => {
        _arr[i] = `"${v.replace('=', '":"')}"`;
    });
    return str
        ? JSON.parse(`{${arr.join()}}`, (key, value) =>
              key === '' ? value : decodeURIComponent(value)
          )
        : {};
};

export default class AuthService extends BaseService {
    static get isAuthenticated() {
        return !!localStorage.getItem('mado_token');
    }

    static getUserLocal(): User | null {
        const userStr = localStorage.getItem('mado_staff');
        if (userStr === null) {
            return null;
        }
        try {
            const res = JSON.parse(userStr as string);
            return res;
        } catch (e) {
            return null;
        }
    }

    static logout() {
        localStorage.removeItem('mado_token');
    }

    static authorize() {
        const curUrl = encodeURIComponent(window.location.origin + '/auth');
        window.location.replace(
            `${process.env.REACT_APP_API_STAFF_BASE}/auth/code?service=PM&redirect_uri=${curUrl}`
        );
    }

    static getTokenRequest(code: string, cb: () => void, errorCb: (e: any) => void) {
        const curUrl = encodeURIComponent(window.location.origin + '/auth');
        const tokenUrl = `${process.env.REACT_APP_API_STAFF_BASE}/auth/token?service=PM&grant_type=authorization_code&code=${code}&redirect_uri=${curUrl}`;
        const options = {
            method: 'POST',
            mode: 'cors',
        };
        this.request(tokenUrl, options)
            .then(resp => {
                if (!resp.error) {
                    localStorage.setItem('mado_token', resp.access_token);
                    localStorage.setItem('mado_staff', JSON.stringify(resp.user));
                    cb();
                } else errorCb(resp.error);
            })
            .catch(err => {
                errorCb(err.message);
            });
    }

    static async authRequest(url: RequestInfo, options: RequestInit) {
        const token = `Bearer ${this.getAuthToken()}`;
        let { headers } = options;
        if (headers) {
            headers = {
                ...headers,
                Authorization: token,
            };
        } else {
            headers = {
                Authorization: token,
                'Content-Type': 'application/json',
            };
        }
        options.headers = headers;
        options.mode = 'cors';
        const response = await fetch(url, options);
        return await this.parseResponse(response);
    }

    static getAuthToken(): string | null {
        return localStorage.getItem('mado_token');
    }
}
