import {
    Entities,
    Filter,
    FilterOptions,
    Project,
    ProjectStaffRole,
    ProjectStaffRoleWithStaff,
    ProjectWithStaff,
    SingleEntityMap,
    User,
} from '../common/types';

export const convertFiltersToQuery = (filters: Filter[]): string => {
    let query = '';
    if (filters) {
        for (let filter of filters) {
            if (filter.value && +filter.value.value !== -1) {
                if (filter.name.trim().toLowerCase() === 'lead') {
                    query += `project_lead=${filter.value.value}&`;
                } else {
                    query += `${filter.name.toLowerCase()}=${filter.value.value}&`;
                }
            }
        }
    }
    return query.slice(0, -1);
};

export const convertFilteredEntitiesToFilters = (entities: Entities) => {
    const { customers, projects_leads, projects_sortable_properties } = entities;
    const resArr: Filter[] = [];
    const defaultOption: FilterOptions = { value: '-1', label: 'Any' };
    const defaultSortableOption: FilterOptions = { value: '-1', label: 'Default' };
    if (customers.length) {
        const a = customers.map(el => {
            return {
                value: el.customer_id.toString(),
                label: el.name,
            };
        });
        resArr.push({
            name: 'Customer',
            options: [defaultOption].concat(a),
            defaultValue: defaultOption,
        });
    }
    if (projects_leads.length) {
        const a = projects_leads.map(el => {
            return {
                value: el.staff_id.toString(),
                label: (el.name + ' ' + el.surname).trim(),
            };
        });
        resArr.push({
            name: 'Lead',
            options: [defaultOption].concat(a),
            defaultValue: defaultOption,
        });
    }
    if (projects_sortable_properties.length) {
        const a = projects_sortable_properties.map(el => {
            return {
                value: el,
                label: el,
            };
        });
        resArr.push({
            name: 'Sort',
            options: [defaultSortableOption].concat(a),
            defaultValue: defaultSortableOption,
        });
    }
    return resArr;
};

export const convertProjectToProjectWithStaff = (
    project: Project,
    staffMap: SingleEntityMap
): ProjectWithStaff => {
    const staffRoles: ProjectStaffRole[] & ProjectStaffRoleWithStaff[] = project.staff_roles.map(
        el => {
            return {
                staff: staffMap[el.staff_id] as User,
                role_id: el.role_id,
                staff_id: el.staff_id,
            };
        }
    );
    const projectWithStaff: ProjectWithStaff = project as ProjectWithStaff;
    projectWithStaff.staff_roles = staffRoles;
    return projectWithStaff;
};
