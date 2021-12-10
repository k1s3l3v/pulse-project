import React from 'react';
import './index.scss';
import { User, BioItem, MultipleSingleEntityMap, SingleEntityMap } from '../types';
import { Link } from 'react-router-dom';
import { getEntityNameById, renderWithIcon } from '../utils';
import { Avatar } from '../Avatar';

export const PersonStrip = ({
    user,
    minified,
    entities,
}: {
    user: User;
    minified: boolean;
    entities: MultipleSingleEntityMap;
}) => {
    /* This is meta-settings for ViewStaff Bio */
    const expandBioList = (item: User): BioItem[] => {
        const resArr = [
            {
                text: getEntityNameById(item.title_id, entities.titles as SingleEntityMap),
                textClass: 'text-14 font-arial weight-700 list-skill',
                icon: {
                    symbol: '📜',
                    label: 'title',
                },
                clickable: true,
                link: `/${user.staff_id}`,
                iconStyle: { marginRight: '6px' },
                additionalGlobalStyle: { fontSize: '14px' },
            },
        ];
        if (!minified) {
            resArr.push({
                text: 'write slack',
                textClass: 'text-14 font-arial weight-400 list-skill',
                icon: {
                    symbol: '🌐',
                    label: 'write',
                },
                clickable: true,
                link: '/', //TODO: Temp
                iconStyle: { marginRight: '6px' },
                additionalGlobalStyle: { fontSize: '14px' },
            });
        }
        return resArr;
    };

    return user ? (
        <div className="person-strip-element-container">
            <div className="person-strip-element-container__personal">
                <Link to={{ pathname: `/${user.staff_id}`, state: { user: user } }}>
                    <Avatar
                        entity={user}
                        borderRadius={15}
                        imgClassName="person-strip-element-container__personal_avatar"
                    />
                </Link>
                <div className="person-strip-element-container__personal_info">
                    <div className="person-strip-element-container__personal_info-header">
                        <Link
                            to={{
                                pathname: `/${user.staff_id}`,
                                state: { user: user },
                            }}>
                            <span className="text-24 font-ptmono weight-400 user-name">
                                {user.name} {user.surname}
                            </span>
                        </Link>
                    </div>
                    <div className="person-strip-element-container__personal_info-bio">
                        {expandBioList(user).map(value => renderWithIcon(value))}
                    </div>
                </div>
            </div>
        </div>
    ) : (
        <></>
    );
};
