import React, { useEffect, useState } from 'react';
import {
    Link,
    Route,
    Switch,
    useHistory,
    useLocation,
    matchPath,
    Redirect,
} from 'react-router-dom';
import { Header } from '../../common/Header';
import { SearchBar } from '../../common/SearchBar';
import {
    Entities,
    EntityAlias,
    FetchError,
    Filter,
    GraphData,
    MultipleSingleEntityMap,
    Project,
    ProjectWithStaff,
    Searchable,
    SingleEntityArray,
    SingleEntityMap,
    Theme,
    User,
} from '../../common/types';

import './index.scss';
import { color_light_blue } from '../../common/utils/constants';
import { CustomSwitcher } from '../../common/CustomSwitcher';
import { Avatar } from '../../common/Avatar';
import useAuth, { AuthPage } from '../../common/Auth';
import EntityService from '../../common/services/EntityService';
import { makeEntityMapFromArray } from '../../common/utils';
import { NotFoundPage } from '../NotFoundPage';
import { ViewProjectsPage } from '../ViewProjectsPage';
import ProjectsService from '../../services/ProjectsService';
import {
    convertFilteredEntitiesToFilters,
    convertProjectToProjectWithStaff,
} from '../../utils/Converters';
import { ProjectPage } from '../ProjectPage';

function App() {
    const { user, isAuthenticated } = useAuth();
    let history = useHistory();
    const location = useLocation();
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [me, setMe] = useState<User>({
        staff_id: 0,
        name: '',
        surname: '',
        title_id: null,
        unit_id: null,
        load: {} as GraphData,
        birthdate: '',
        email: '',
        fte_load: 0,
        is_active: false,
        location_id: null,
        login_id: '',
        login_type: '',
        nickname: '',
        patronymic: '',
        phone: '',
        primary_skill_id: null,
        projects: [],
        social_networks: [],
        avatar: null,
    });
    const [theme, setTheme] = useState<Theme>(localStorage.getItem('theme') as Theme);
    const [searchString, setSearchString] = useState<string>('');
    const [titles, setTitles] = useState<SingleEntityMap>({} as SingleEntityMap);
    const [filters, setFilters] = useState<Filter[]>([]);

    const fetchCallback = (
        sString: string,
        filters?: Filter[]
    ): Promise<ProjectWithStaff[] | FetchError> => {
        return ProjectsService.search(sString, 4, filters).then(resp => {
            if ((resp as FetchError).error) {
                console.log((resp as FetchError).error.status);
                return resp as FetchError;
            }
            const projects: Project[] = (resp as { projects: Project[]; staff: User[] }).projects;
            const staff: SingleEntityMap = makeEntityMapFromArray(
                (resp as { projects: Project[]; staff: User[] }).staff,
                'staff_id'
            );
            return projects.map(el => convertProjectToProjectWithStaff(el, staff));
        });
    };

    const renderSuggestion = (s: Searchable): JSX.Element => {
        const project = s as Project;
        return (
            <Link to={{ pathname: `/project/${project.project_id}`, state: { project: project } }}>
                <div className="suggestion-searchbar">
                    <Avatar
                        entity={project}
                        borderRadius={15}
                        imgClassName="suggestion-searchbar__avatar"
                    />
                    <span className="text-14 weight-400 font-ptmono suggestion-item">
                        {project.name}
                    </span>
                </div>
            </Link>
        );
    };

    const getSuggestionValue = (s: Searchable): string => {
        return (s as Project).name;
    };

    const opposingTheme = (theme: Theme): Theme => {
        if (theme === 'dark') return 'light';
        return 'dark';
    };

    const applyTheme = (theme: Theme) => {
        document.body.classList.remove(opposingTheme(theme));
        setTheme(theme);
        document.body.classList.add(theme);
    };

    const toggleTheme = () => {
        applyTheme(opposingTheme(theme));
    };

    useEffect(() => {
        setIsLoading(true);
        let lsTheme = localStorage.getItem('theme');
        if (lsTheme) {
            applyTheme(lsTheme as Theme);
        } else {
            applyTheme('light'); // as default theme
        }
    }, []);

    useEffect(() => {
        if (isAuthenticated) {
            setMe(user as User);
            const entityAliases: EntityAlias[] = ['titles', 'customers'];
            EntityService.getStaffEntities(
                entityAliases.concat(['projects_leads', 'projects_sortable_properties'])
            ).then(entityResp => {
                const res: MultipleSingleEntityMap = Object.fromEntries(
                    entityAliases.map(el => [
                        el,
                        makeEntityMapFromArray(
                            (entityResp as Entities)[el] as SingleEntityArray,
                            el.slice(0, -1) + '_id'
                        ),
                    ])
                );
                setTitles(res.titles as SingleEntityMap);
                setFilters(convertFilteredEntitiesToFilters(entityResp as Entities));
                setIsLoading(false);
            });
        }
    }, [isAuthenticated]);

    useEffect(() => {
        localStorage.setItem('theme', theme);
    }, [theme]);

    const prjMatchingUrls = ['/projects', '/project/:project_id(\\d+)'];
    const searchbarMatchingUrls = ['/projects'];
    if (location.pathname === '/') return <Redirect to="/projects" />;
    return (
        <>
            <Header
                websiteName={'project'}
                backgroundColor={color_light_blue}
                user={me}
                routes={[{ name: 'Projects', url: '/projects', matchingUrls: prjMatchingUrls }]}
                loading={isLoading}
                titles={titles}
            />
            {searchbarMatchingUrls.some(el =>
                matchPath(location.pathname, {
                    path: el,
                    exact: true,
                    strict: false,
                })
            ) && (
                <div className="app__controls">
                    <div className="app__controls_searchbar">
                        <SearchBar
                            fetchCallback={fetchCallback}
                            renderSuggestionCallback={renderSuggestion}
                            getSuggestionValueCallback={getSuggestionValue}
                            searchCompleted={(v, fs?) => {
                                setSearchString(v);
                                if (fs) {
                                    setFilters(fs);
                                }
                                history.push('/projects');
                            }}
                            filters={filters}
                        />
                    </div>
                </div>
            )}
            <CustomSwitcher toggleCallback={() => toggleTheme()} initialState={theme === 'light'} />
            <Switch>
                <Route
                    exact
                    path="/projects"
                    render={props => (
                        <ViewProjectsPage
                            theme={theme}
                            globalStore={searchString}
                            filters={filters}
                            {...props}
                        />
                    )}
                />
                <Route exact path="/project/:project_id(\d+)" component={ProjectPage} />
                <Route exact path="/auth" component={AuthPage} />
                <Route component={NotFoundPage} />
            </Switch>
        </>
    );
}

export default App;
