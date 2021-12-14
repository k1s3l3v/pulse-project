import AuthService from '../../../../../../PycharmProjects/prj/src/common/services/AuthService';
import {Entities, EntityAlias, FetchError, ProjectCriterion} from '../../../../../../PycharmProjects/prj/src/common/types';

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

    static async getTitles(entities: EntityAlias[]): Promise<Entities | FetchError> {
        const options: RequestInit = {
            method: 'GET',
        };
        const query = '?' + entities.map(
            el => {
                if (el === 'titles') return el + '=true';
                else return el + '=false';
            }
            ).join('&');
        return await this.authRequest(
            `${process.env.REACT_APP_API_STAFF_BASE}/entity/${query}`,
            options
        );
    }

    static async getCriteria(): Promise<Entities | FetchError> {
        const options: RequestInit = {
            method: 'GET',
        };
        return await this.authRequest(
            `${process.env.REACT_APP_API_PULSE_BASE}/entity/?project_criteria=true`,
            options
        );
    }
}
