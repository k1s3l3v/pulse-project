import { FetchError } from '../types';

export default class BaseService {
    static logout() {
        localStorage.removeItem('mado_token');
        localStorage.removeItem('mado_staff');
    }

    static async parseResponse(response: Response): Promise<any | FetchError> {
        const { status }: { status: number } = response;
        const realResp = await response.json();
        if (status < 200 || status >= 300) {
            if (status === 401) {
                console.log('logging out');
                this.logout();
                window.location.replace('/auth');
            }
            return { error: { status, message: JSON.stringify(realResp.detail) } };
        }
        return realResp;
    }

    static request(url: string, options?: object) {
        return fetch(url, options).then(response => this.parseResponse(response));
    }
}
