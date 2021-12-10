import { FetchError, Filter, Project, ProjectWithStaff, User } from '../common/types';
import AuthService from '../common/services/AuthService';
import { convertFiltersToQuery } from '../utils/Converters';

export default class ProjectsService extends AuthService {
    static async search(
        value: string,
        limit?: number,
        filters?: Filter[]
    ): Promise<{ projects: Project[]; staff: User[] } | FetchError> {
        const options: RequestInit = {
            method: 'GET',
        };
        const filt = convertFiltersToQuery(filters as Filter[]);
        return await this.authRequest(
            `${process.env.REACT_APP_API_STAFF_BASE}/project/search?` +
                (value ? `query=${value}` : '') +
                `${value ? '&' + filt : filt}` +
                (limit && limit > 0 ? `&limit=${limit}` : ''),
            options
        );
    }

    static async getProjectById(project_id: number): Promise<ProjectWithStaff | FetchError> {
        const options: RequestInit = {
            method: 'GET',
        };

        return await this.authRequest(
            `${process.env.REACT_APP_API_STAFF_BASE}/project/${project_id}`,
            options
        );
    }
}
