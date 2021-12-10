import React, { useEffect, useState } from 'react';
import { BioItem, Emoji, Entity, SingleEntityArray, SingleEntityMap } from '../types';
import { components, DropdownIndicatorProps, GroupBase } from 'react-select';
import downindicator from '../assets/person_menu_blue.svg';

export const useKeyPress = (targetKey: string) => {
    const [keyPressed, setKeyPressed] = useState<boolean>(false);
    function downHandler({ key }: { key: string }) {
        if (key === targetKey) {
            setKeyPressed(true);
        }
    }

    const upHandler = ({ key }: { key: string }) => {
        if (key === targetKey) {
            setKeyPressed(false);
        }
    };

    useEffect(() => {
        window.addEventListener('keydown', downHandler);
        window.addEventListener('keyup', upHandler);
        return () => {
            window.removeEventListener('keydown', downHandler);
            window.removeEventListener('keyup', upHandler);
        };
    }, []);
    return keyPressed;
};

export const unfocusALl = () => {
    const tmp = document.createElement('input');
    document.body.appendChild(tmp);
    tmp.focus();
    document.body.removeChild(tmp);
};

export const EmojiWrapper = ({
    symbol,
    label,
    style,
}: {
    symbol: string;
    label: string;
    style?: Object;
}) => (
    <span
        className="emoji"
        role="img"
        aria-label={label ? label : ''}
        aria-hidden={label ? 'false' : 'true'}
        style={Object.assign(
            { marginRight: '9px', marginBottom: '3px', textAlign: 'center' as 'center' }, //https://github.com/typestyle/typestyle/issues/281
            style
        )}>
        {symbol}
    </span>
);

const wrapWithLink = (link: string, children: JSX.Element): JSX.Element => {
    return <a href={link}>{children}</a>;
};

const renderEmojiOrIcon = (elem: BioItem) => {
    if ((elem.icon as Emoji).symbol)
        return (
            <EmojiWrapper
                symbol={(elem.icon as Emoji).symbol}
                label={(elem.icon as Emoji).label}
                style={elem.iconStyle}
            />
        );
    return <img src={elem.icon as string} alt="" style={elem.iconStyle} />;
};

export const renderWithIcon = (elem: BioItem) => {
    const defaultStyle = { display: 'flex', alignItems: 'center' };
    return (
        <div key={elem.text} style={Object.assign(defaultStyle, elem.additionalGlobalStyle)}>
            {renderEmojiOrIcon(elem)}
            {elem.clickable ? (
                wrapWithLink(
                    elem.link as string,
                    <span className={elem.textClass}>{elem.text}</span>
                )
            ) : (
                <span className={elem.textClass}>{elem.text}</span>
            )}
            {elem.additionalJSX}
        </div>
    );
};

export const DropdownIndicator = (
    props: JSX.IntrinsicAttributes & DropdownIndicatorProps<unknown, boolean, GroupBase<unknown>>
) => {
    return (
        <components.DropdownIndicator {...props}>
            <img src={downindicator} alt="" style={{ width: '100%' }} />
        </components.DropdownIndicator>
    );
};

export const makeEntityMapFromArray = (
    array: SingleEntityArray,
    idField: string
): SingleEntityMap => {
    return Object.fromEntries(
        new Map(array.map(el => [+el[idField as keyof Entity], el]))
    ) as SingleEntityMap;
};

export const getEntityNameById = (id: number | null, map: SingleEntityMap): string => {
    if (!id) return 'N/A';
    const entity = map[id];
    if (!entity) return 'N/A';
    return entity.name;
};

export const getEntityById = (id: number | null, map: SingleEntityMap): Entity => {
    if (!id) return 'N/A';
    const entity = map[id];
    if (!entity) return 'N/A';
    return entity;
};
