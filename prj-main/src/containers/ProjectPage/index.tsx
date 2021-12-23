import React, { useEffect, useState } from 'react';
import {
    Customer,
    Entities,
    EntityAlias,
    FetchError, MultipleSingleEntityMap,
    ProjectCriterion, ProjectPulse, ProjectsMainRoles,
    ProjectWithStaff, SingleEntityArray,
    Title
} from '../../common/types';
import { ProjectComponent } from '../../components/ProjectComponent';
import { StaticContext } from 'react-router';
import './index.scss';
import { RouteComponentProps } from 'react-router-dom';
import ProjectsService from '../../services/ProjectsService';
import EntityService from "../../common/services/EntityService";
import {makeEntityMapFromArray} from "../../common/utils";

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
    const [entities, setEntities] = useState<MultipleSingleEntityMap>(
        {} as MultipleSingleEntityMap
    );
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
    const [titles, setTitles] = useState<Title[]>([]);
    const [project_criteria, setCriteria] = useState<ProjectCriterion[]>([]);
    const [project_pulse, setPulse] = useState<ProjectPulse>({
        status: {
            project_status_id: 0,
            project_id: 0,
            aggregated_value: 0,
            latest_updated_at: '',
            latest_updater_id: null,
            latest_grades: {
                '': {
                    project_criterion_id: 0,
                    date: '',
                    value: 0,
                    comment: '',
                    author_id: 0,
                }
            },
            latest_log: [],
        },
        criteria: [],
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
        if (project.project_id !== 0 && typeof(project.project_id) !== "undefined")
            Promise.all([ProjectsService.getProjectPulse(project.project_id)]).then(([pulseResp]) => {
                setPulse(pulseResp as ProjectPulse);
            });
    }, [props.match.params]);
    useEffect(() => {
        setIsLoading(true);
        const entityAliases: EntityAlias[] = [
            'titles',
            'customers',
        ];
        const entityPromise = EntityService.getStaffEntities(entityAliases);
        const criteriaPromise = EntityService.getCriteria();
        Promise.all([entityPromise, criteriaPromise]).then((
            [entityResp, criteriaResp]) => {
            setTitles((entityResp as Entities).titles);
            setCriteria((criteriaResp as { project_criteria: ProjectCriterion[] }).project_criteria);
            const res: MultipleSingleEntityMap = Object.fromEntries(
                entityAliases.map(el => [
                    el,
                    makeEntityMapFromArray(
                        (entityResp as Entities)[el] as SingleEntityArray,
                        el.slice(0, -1) + '_id'
                    ),
                ])
            );
            setEntities(res as MultipleSingleEntityMap);
            setIsLoading(false);
        });
    }, []);
    return (
        <div className="App">
            {!isLoading ? <ProjectComponent entities = {entities} project={project} titles={titles} project_criteria={project_criteria} project_pulse={project_pulse}/> : <div>LOADING</div>}
        </div>
    );
};