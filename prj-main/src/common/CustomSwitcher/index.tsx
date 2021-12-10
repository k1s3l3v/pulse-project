import React from 'react';
import './index.scss';

export const CustomSwitcher = ({
    toggleCallback,
    initialState,
}: {
    toggleCallback: () => void;
    initialState: boolean;
}) => {
    return (
        <label id="customswitcher" className="custom-switcher">
            <input type="checkbox" onChange={toggleCallback} id="slider" checked={initialState} />
            <span className="custom-switcher__slider" />
        </label>
    );
};
