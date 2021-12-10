import React from 'react';
import { Link } from 'react-router-dom';
import {
    BioItem,
    Customer,
    MultipleSingleEntityMap,
    Project,
    ProjectsMainRoles,
    ProjectWithStaff,
    SingleEntityMap,
} from '../../../common/types';
import { getEntityNameById, renderWithIcon } from '../../../common/utils';
import './index.scss';
import { Avatar } from '../../../common/Avatar';
import { getProjectRole } from '../../../utils/ViewProjects';
import { convertProjectToProjectWithStaff } from '../../../utils/Converters';

export const ViewProjectsListElement = ({
    project,
    entities,
    staff,
    roles,
}: {
    project: Project;
    entities: MultipleSingleEntityMap;
    staff: SingleEntityMap;
    roles: ProjectsMainRoles;
}) => {
    const projectLeader = getProjectRole(project, staff, roles.project_lead.role_id);
    const projectAccountant = getProjectRole(project, staff, roles.project_accountant.role_id);

    const renderTopEmojiTextLine = (): BioItem[] => {
        const resArr: BioItem[] = [
            {
                text: project.is_active ? 'Active' : 'Not Active',
                textClass: 'text-14 font-arial weight-400 list-stuff',
                icon: {
                    symbol: project.is_active ? '✅' : '🚫',
                    label: 'active',
                },
                clickable: false,
            },
            {
                text: project.pricing_model === 'FIXED_PRICE' ? 'Fixed Price' : 'Time and Material',
                textClass: 'text-14 font-arial weight-400 list-stuff',
                icon: {
                    symbol: project.pricing_model === 'FIXED_PRICE' ? '🛠️' : '🕒️',
                    label: 'pricing',
                },
                clickable: false,
            },
        ];
        if (projectAccountant) {
            resArr.push({
                text: `${projectAccountant.name} ${projectAccountant.surname}`,
                textClass: 'text-14 font-arial weight-400 list-stuff',
                icon: {
                    symbol: '💰',
                    label: 'contacts',
                },
                clickable: true,
                link: `${process.env.REACT_APP_PEOPLE_BASE}/staff/${projectAccountant.staff_id}`,
            });
        }
        return resArr;
    };

    const expandBioList = (): BioItem[] => {
        let customerLocation = 'N/A';
        if (entities.customers && project.customer_id) {
            const loc = (entities.customers[project.customer_id] as Customer).location;
            if (loc) customerLocation = loc;
        }

        const resArr: BioItem[] = [
            {
                text: getEntityNameById(project.customer_id, entities.customers as SingleEntityMap),
                textClass: 'text-14 font-arial weight-700 list-stuff',
                icon: {
                    symbol: '📜',
                    label: 'title',
                },
                clickable: false,
            },
            {
                text: customerLocation,
                textClass: 'text-14 font-arial weight-400 list-stuff',
                icon: {
                    symbol: '📍',
                    label: 'location',
                },
                clickable: false,
            },
            {
                text: `? / ${project.fte_load / 100} FTE`,
                textClass: `text-14 font-arial weight-400 list-stuff`,
                icon: {
                    symbol: '⌛',
                    label: 'FTE',
                },
                clickable: false,
            },
        ];
        if (projectLeader) {
            resArr.push({
                text: `${projectLeader.name} ${projectLeader.surname}`,
                textClass: 'text-14 font-arial weight-400 list-stuff',
                icon: {
                    symbol: '🎖️',
                    label: 'location',
                },
                clickable: true,
                link: `${process.env.REACT_APP_PEOPLE_BASE}/staff/${projectLeader.staff_id}`,
            });
        }
        return resArr;
    };

    const projectWithStaff: ProjectWithStaff = convertProjectToProjectWithStaff(project, staff);
    return (
        <div className="project-list-element-container">
            <div className="project-list-element-container__personal">
                <Link
                    to={{
                        pathname: `/project/${project.project_id}`,
                        state: { project: projectWithStaff },
                    }}>
                    <Avatar
                        entity={project}
                        borderRadius={15}
                        imgClassName="project-list-element-container__personal_avatar"
                    />
                </Link>
                <div className="project-list-element-container__personal_info">
                    <div className="project-list-element-container__personal_info-header">
                        <Link
                            to={{
                                pathname: `/project/${project.project_id}`,
                                state: {
                                    project: projectWithStaff,
                                },
                            }}>
                            <span className="text-24 font-ptmono weight-400 project-name">
                                {project.name}
                            </span>
                        </Link>
                        {renderTopEmojiTextLine().map(value => renderWithIcon(value))}
                    </div>
                    <div className="project-list-element-container__personal_info-bio">
                        {expandBioList().map(value => renderWithIcon(value))}
                    </div>
                </div>
            </div>
        </div>
    );
};
