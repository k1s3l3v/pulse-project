import { Link, matchPath, useLocation } from 'react-router-dom';
import mado_logo from '../assets/mado_logo.svg';
import person_menu from '../assets/person_menu.svg';
import { CustomRoute, SingleEntityMap, User } from '../types';
import './index.scss';
import { Avatar } from '../Avatar';

export const Header = ({
    websiteName,
    backgroundColor,
    user,
    routes,
    loading,
    titles,
}: {
    websiteName: string;
    backgroundColor: string;
    user: User;
    routes?: CustomRoute[];
    loading: boolean;
    titles: SingleEntityMap;
}) => {
    const location = useLocation();

    const checkMatchingUrls = (route: CustomRoute): boolean => {
        if (route.matchingUrls) {
            for (let matchingUrl of route.matchingUrls) {
                if (
                    matchPath(location.pathname, {
                        path: matchingUrl,
                        exact: true,
                        strict: false,
                    })
                )
                    return true;
            }
        }
        return !!matchPath(location.pathname, {
            path: route.url,
            exact: true,
            strict: false,
        });
    };

    return (
        <div className="header-container" style={{ backgroundColor: backgroundColor }}>
            <div className="header-container__website">
                <img src={mado_logo} alt="MaDo Logo" />
                <span className="text-24 font-arialBlack weight-900">{`MaDo`}</span>
                <span className="text-14 font-ptmono weight-400 header-container__website_name">{`//${websiteName}`}</span>
            </div>
            {routes && routes.length && (
                <div className="header-container__routes">
                    {routes.map(route => {
                        return (
                            <Link to={route.url} key={route.url}>
                                <span
                                    className={`text-18 font-ptmono weight-400 route-item ${
                                        checkMatchingUrls(route) ? 'route-active' : ''
                                    }`}>
                                    {route.name}
                                </span>
                            </Link>
                        );
                    })}
                </div>
            )}
            <div className="header-container__user">
                <div className="header-container__user_personal">
                    {!loading ? (
                        <span className="text-24 font-ptmono weight-400 header-container__user_personal_fullName">
                            {`${user.name} ${user.surname}`}
                        </span>
                    ) : (
                        <div className="loading-pulsar" />
                    )}
                    {!loading ? (
                        <span className="text-14 font-ptmono weight-400 header-container__user_personal_title">
                            {user.title_id && user.title_id in titles
                                ? titles[user.title_id].name
                                : ''}
                        </span>
                    ) : (
                        <div className="loading-pulsar" />
                    )}
                </div>
                <div className="header-container__user_avatar">
                    {!loading ? (
                        <Avatar entity={user} borderRadius={25} />
                    ) : (
                        <div className="loading-pulsar imagepulsar" />
                    )}
                </div>
            </div>
            <div className="header-container__menu">
                <img src={person_menu} alt="menu" />
            </div>
        </div>
    );
};
