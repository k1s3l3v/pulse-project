import {
    BarData,
    DataEntity,
    Entities,
    EntityStatus,
    Filter,
    FilterOptions,
    GraphData,
    ItemData,
    Project,
    ProjectStaffRole,
    ProjectStaffRoleWithStaff,
    ProjectWithStaff,
    SingleEntityMap,
    StaffProjectGraphData,
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

export const convertProjectsToGraphData = (
    entities: Entities,
    project: ProjectWithStaff
): ProjectWithStaff => {
    let staffProjectsGraphData: StaffProjectGraphData[] = [];
    const { projects } = entities;
    const get_name = (
        projects: Project[],
        project_id: number
    ): string => {
        for (let prj of projects) if (prj.project_id === project_id) return prj.name;
        return '';
    };
    const dateToMonth = (date: string): number => {
        return parseInt(date.slice(5, 7))
    };

    for (let staff of project.staff_roles) {
        const dataEntity: DataEntity[] = staff.staff.projects.map(
            el => {
                return {
                    name: get_name(projects, el.project_id),
                    showEntityName: false,
                    showValue: false,
                };
            }
        );
        const bins = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        let new_bins: { [bin: string]: ItemData[] }[] = bins.map(
            el => {
                return {
                    [el]: []
                };
            }
        );
        let item_data_arr: { itemData: ItemData, month_borders: number[] }[] = [];
        let month_range: number[] = [];
        let index = 0;
        for (let prj of staff.staff.projects) {
            const prj_name = dataEntity[index].name;
            if (prj_name !== '') {
                const prj_start = dateToMonth(prj.date_start);
                const prj_end = dateToMonth(prj.date_end);
                month_range.push(prj_start, prj_end);
                const itemData: ItemData = {
                    name: prj_name,
                    value: prj.fte_load,
                    status: prj.type as EntityStatus,
                };
                item_data_arr.push({itemData: itemData, month_borders: month_range.slice(-2)});
            }
            index++;
        }
        for (let bin of item_data_arr) {
            for (let num = bin.month_borders[0] - 1; num < bin.month_borders[1]; num++) {
                new_bins[num][bins[num]].push(bin.itemData);
            }
        }
        const start = Math.min.apply(null, month_range);
        const end = Math.max.apply(null, month_range);
        if (1 <= start && start <= end && end <= bins.length) {
            const barData: BarData[] = new_bins.slice(start - 1, end).map(
                el => {
                    let value = Object.entries(el)[0];
                    return {
                        bin: value[0],
                        values: value[1]
                    };
                }
            );
            const staffProjectGraphData: StaffProjectGraphData = staff as StaffProjectGraphData;
            staffProjectGraphData.graphData = {data: barData, entities: dataEntity} as GraphData;
            staffProjectsGraphData.push(staffProjectGraphData);
        }
    }
    const projectWithConvertedStaff = project as Project & {staff_roles: StaffProjectGraphData[]};
    projectWithConvertedStaff.staff_roles = staffProjectsGraphData;
    return projectWithConvertedStaff;
}
