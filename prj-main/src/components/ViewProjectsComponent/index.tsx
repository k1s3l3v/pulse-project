import React, { useEffect, useState } from 'react';
import Loader from 'react-loader-spinner';
import {
    Entities,
    EntityAlias,
    Filter,
    MultipleSingleEntityMap,
    Project,
    ProjectsMainRoles,
    SingleEntityArray,
    SingleEntityMap,
    Theme,
    User,
} from '../../common/types';
import './index.scss';
import { ViewProjectsListElement } from './ViewProjectsListElement';
import { color_light_blue } from '../../common/utils/constants';
import EntityService from '../../common/services/EntityService';
import { makeEntityMapFromArray } from '../../common/utils';
import useAuth from '../../common/Auth';
import ProjectsService from '../../services/ProjectsService';

export const ViewProjectsComponent = ({
    searchString,
    filters,
    theme,
}: {
    searchString: string;
    filters: Filter[];
    theme: Theme;
}) => {
    const [projects, setProjects] = useState<Project[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [entities, setEntities] = useState<MultipleSingleEntityMap>(
        {} as MultipleSingleEntityMap
    );
    const [projectStaff, setProjectStaff] = useState<SingleEntityMap>({} as SingleEntityMap);
    const [projectsMainRoles, setProjectsMainRoles] = useState<ProjectsMainRoles>(
        {} as ProjectsMainRoles
    );
    const { user } = useAuth();

    useEffect(() => {
        setIsLoading(true);
        const entityAliases: EntityAlias[] = [
            'titles',
            'locations',
            'skills',
            'projects',
            'social_networks',
            'customers',
            'roles',
        ];
        const entityPromise = EntityService.getStaffEntities(
            entityAliases.concat(['units_hierarchy', 'projects_main_roles'])
        );
        const projectsPromise = ProjectsService.search(searchString, -1, filters); // TODO: Limit
        Promise.all([entityPromise, projectsPromise]).then(([entityResp, projectsResp]) => {
            const prjs: Project[] = (projectsResp as { projects: Project[]; staff: User[] })
                .projects;
            const staff: User[] = (projectsResp as { projects: Project[]; staff: User[] }).staff;
            const res: MultipleSingleEntityMap = Object.fromEntries(
                entityAliases.map(el => [
                    el,
                    makeEntityMapFromArray(
                        (entityResp as Entities)[el] as SingleEntityArray,
                        el.slice(0, -1) + '_id'
                    ),
                ])
            );
            //TODO: ERROR HANDLING with toasts?
            setEntities(res as MultipleSingleEntityMap);
            setProjects(prjs);
            setProjectsMainRoles((entityResp as Entities).projects_main_roles);
            setProjectStaff(makeEntityMapFromArray(staff, 'staff_id'));
            setIsLoading(false);
        });
    }, [searchString, JSON.stringify(filters)]); //TODO: JSON

    return (
        <div className="viewproject-component">
            {!isLoading ? (
                projects.map((el, index) => {
                    return (
                        <ViewProjectsListElement
                            key={index}
                            project={el}
                            entities={entities}
                            staff={projectStaff}
                            roles={projectsMainRoles}
                        />
                    );
                })
            ) : (
                <Loader type="TailSpin" color={color_light_blue} height={80} width={80} />
            )}
        </div>
    );
};
