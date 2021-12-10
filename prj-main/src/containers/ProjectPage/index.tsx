import React, { useEffect, useState } from 'react';
import { FetchError, ProjectWithStaff } from '../../common/types';
import { ProjectComponent } from '../../components/ProjectComponent';
import { StaticContext } from 'react-router';
import './index.scss';
import { RouteComponentProps } from 'react-router-dom';
import ProjectsService from '../../services/ProjectsService';

type RouteParams = {
    project_id: string;
};

type LocationState = {
    project: ProjectWithStaff;
};

export const ProjectPage = (
    props: RouteComponentProps<RouteParams, StaticContext, LocationState>
) => {
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [project, setProject] = useState<ProjectWithStaff>({
        pricing_model: 'FIXED_PRICE',
        staff_roles: [],
        customer_id: null,
        date_end: null,
        date_start: '',
        description: null,
        fte_load: 0,
        is_active: false,
        name: '',
        avatar: null,
        project_id: 0,
    });
    useEffect(() => {
        if (!props.location.state) {
            setIsLoading(true);
            ProjectsService.getProjectById(+props.match.params.project_id).then(resp => {
                if ((resp as FetchError).error) {
                    console.log((resp as FetchError).error.status);
                    setIsLoading(false);
                    return;
                }
                setProject(resp as ProjectWithStaff);
                setIsLoading(false);
            });
        } else setProject(props.location.state.project);
    }, [props.match.params]);
    return (
        <div className="App">
            {!isLoading ? <ProjectComponent project={project} /> : <div>LOADING</div>}
        </div>
    );
};
