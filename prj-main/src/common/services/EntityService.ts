import AuthService from './AuthService';
import { Entities, EntityAlias, FetchError } from '../types';

export default class EntityService extends AuthService {
    static async getStaffEntities(entities: EntityAlias[]): Promise<Entities | FetchError> {
        const options: RequestInit = {
            method: 'GET',
        };
        const query = '?' + entities.map(el => el + '=true').join('&');
        return await this.authRequest(
            `${process.env.REACT_APP_API_STAFF_BASE}/entity/${query}`,
            options
        );
    }
}
