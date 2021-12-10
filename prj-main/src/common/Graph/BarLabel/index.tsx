import React from 'react';
import { color_black, color_white } from '../../utils/constants';

type CustomBarLabel = {
    value?: number;
    name?: string;
    status?: string;
};

const renderText = (
    x: number,
    y: number,
    width: number,
    text: string,
    color: string,
    fontSize: number,
    height: number
) => {
    return (
        <text
            x={x}
            y={y}
            dy={height}
            dx={0.5 * width}
            fill={color}
            fontSize={fontSize}
            fontFamily={'PT Mono'}
            textAnchor="middle">
            {text}
        </text>
    );
};

const textsToShowOnBar = (status: string, showEntityName: boolean, showValue: boolean): number => {
    let ret = 3;
    if (!status) ret--;
    if (!showValue) ret--;
    if (!showEntityName) ret--;
    return ret;
};

// No specs on official docs provided for this props
export const BarLabel = (props: any) => {
    const { x, y, value, width, height, entityName, showEntityName, showValue } = props;
    const values = props.data.data[props.index].values;
    const idx = values.findIndex((el: { name: string }) => el.name === entityName);
    let status = '';
    if (idx !== -1) status = values[idx].status;

    const label: CustomBarLabel = {};
    const defaultFontSize = document.body.clientWidth > 1200 ? 18 : 16;
    const textContainerHeight = defaultFontSize + 2; // Heuristic 2

    /* If we dont have ANY place to render anything - return nothing */
    if (!width || !height) return <></>;
    if (height < textContainerHeight) return <></>;

    /* If we cannot render all information - we render MAIN attribute by priority : NAME -> VALUE -> STATUS*/
    const renderedItems = textsToShowOnBar(status, showEntityName, showValue);
    if (height < textContainerHeight * renderedItems) {
        const localHeight = (height + defaultFontSize) / 2;
        if (!showEntityName) {
            if (!showValue)
                return renderText(x, y, width, status, color_black, defaultFontSize, localHeight);
            return renderText(x, y, width, value, color_white, defaultFontSize, localHeight);
        }
        return renderText(x, y, width, entityName, color_white, defaultFontSize, localHeight);
    }

    /* We have place to render everything */
    if (showEntityName) {
        Object.defineProperty(label, 'entityName', {
            value: entityName,
            enumerable: true,
        });
    }
    if (showValue) {
        Object.defineProperty(label, 'value', {
            value: value,
            enumerable: true,
        });
    }
    if (status) {
        Object.defineProperty(label, 'status', {
            value: status,
            enumerable: true,
        });
    }

    const mult = renderedItems === 3 ? 1 : renderedItems === 2 ? 0.5 : 0;

    return (
        <>
            {Object.entries(label).map((el, index) => {
                return (
                    <text
                        key={index}
                        x={x}
                        y={y}
                        dy={(height + defaultFontSize) / 2 + textContainerHeight * (index - mult)}
                        dx={0.5 * width}
                        fill={el[0] === 'status' ? color_black : color_white}
                        fontSize={defaultFontSize}
                        fontFamily={'PT Mono'}
                        textAnchor="middle">
                        {el[1]}
                    </text>
                );
            })}
        </>
    );
};
