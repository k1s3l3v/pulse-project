import React from 'react';
import { ViewProjectsComponent } from '../../components/ViewProjectsComponent';
import './index.scss';
import { Filter, Theme } from '../../common/types';

export const ViewProjectsPage = (props: {
    globalStore: string;
    filters: Filter[];
    theme: Theme;
}) => {
    return (
        <div className={`viewprojects-container`}>
            <ViewProjectsComponent
                searchString={props.globalStore}
                filters={props.filters}
                theme={props.theme}
            />
        </div>
    );
};
