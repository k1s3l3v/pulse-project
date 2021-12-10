import React from 'react';
import { ProjectWithStaff } from '../../common/types';
import './index.scss';
import { useHistory } from 'react-router-dom';

export const ProjectComponent = ({ project }: { project: ProjectWithStaff }) => {
    let history = useHistory();
    return (
        <div className="project-container">
            <div className="project-container__header">
                <span
                    className="text-36 font-ptmono weight-400 backbutton"
                    onClick={() => history.goBack()}>
                    {'⬅️'}
                </span>
                <span className="text-36 font-ptmono weight-400"> {project.name}</span>
            </div>
            Project is: {project.name}
            <br />
            Its description is: {project.description?.toLowerCase()}
        </div>
    );
};
