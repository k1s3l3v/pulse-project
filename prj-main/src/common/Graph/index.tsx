import React, { useCallback, useState } from 'react';
import {
    Bar,
    BarChart,
    CartesianGrid,
    Cell,
    LabelList,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from 'recharts';
import { DataEntity, GraphData, RechartsDataType, Theme } from '../types';
import './index.scss';
import { OverloadTool } from './GraphUtils/overload';
import { BarLabel } from './BarLabel';
import { convertGraphDataToRechartsData, valueAccessor } from './GraphUtils';
import { color_black, color_light_blue, color_white } from '../utils/constants';

export const Graph = ({
    data,
    UserTooltip,
    theme,
}: {
    data: GraphData;
    UserTooltip: JSX.Element;
    theme: Theme;
}) => {
    const marginTop = 25; /* See 'margin.top' prop in <BarChart /> */
    /* useRef doesnt trigger on rerender, so we are forced to use useCallback*/
    const [height, setHeight] = useState(0);
    const measuredRef = useCallback(node => {
        if (node !== null && node.current) {
            setHeight(node.current.clientHeight);
        }
    }, []);

    const rechartsData = convertGraphDataToRechartsData(data);
    const overloadTool = new OverloadTool(rechartsData, data.targetLoad ? data.targetLoad : 0);

    /* Cannot move anywhere (this function need 'rechartsData' in its scope) */
    // No specs provided for this type of props
    const renderQuarterTick = (tickProps: any) => {
        const { x, y, payload } = tickProps;
        const { offset, index } = payload;
        const pathX = Math.floor(x - offset);
        return (
            <>
                <text
                    x={x}
                    y={y + 15}
                    textAnchor="middle"
                    fill={theme === 'light' ? color_black : color_white}>
                    {rechartsData[index].bin}
                </text>
                <path
                    d={`M${pathX},${y + 15}v${-30}`}
                    stroke={theme === 'light' ? color_black : color_white}
                />
            </>
        );
    };

    const calculateDashOffset = (): number => {
        if (!data.targetLoad) return 0;
        /* Background: we need to calculate dash offset (in PIXELS!) */

        let dashOffset = marginTop;
        let max = 0.0;
        for (let bar of rechartsData) {
            const sumArr = overloadTool.isMoreThanTargetLoad(bar);
            max = sumArr > max ? sumArr : max;
        }
        if (max > data.targetLoad) {
            /* We're over bar */
            const graphHeight = height - marginTop - 25; //TODO: why 25?
            dashOffset = graphHeight - graphHeight / (max / data.targetLoad) + marginTop;
        }
        return dashOffset;
    };

    return (
        <ResponsiveContainer width="100%" height="100%" ref={measuredRef}>
            <BarChart
                data={rechartsData}
                margin={{
                    top: marginTop,
                    right: 30,
                    left: -30,
                    bottom: -5,
                }}
                barCategoryGap={1}>
                <CartesianGrid
                    strokeDasharray="7 7"
                    vertical={false}
                    horizontal={!!data.targetLoad}
                    horizontalPoints={[height ? calculateDashOffset() : -1]}
                />
                <XAxis
                    tick={renderQuarterTick}
                    tickSize={0}
                    stroke={theme === 'light' ? color_black : color_white}
                />
                <YAxis
                    tick={false}
                    stroke={theme === 'light' ? color_black : color_white}
                    label={{
                        value: data.targetLoad ? `trg load: ${data.targetLoad.toFixed(1)}` : '',
                        angle: -90,
                        position: 'insideRight',
                        fontFamily: 'PT Mono',
                        fontSize: '18px',
                        offset: 10,
                        dy: -70,
                        fill: theme === 'light' ? color_black : color_white,
                    }}
                    domain={[0, data.targetLoad ? data.targetLoad : 'auto']}
                />
                {data.entities.map((de: DataEntity) => (
                    <Bar key={de.name} dataKey={de.name} stackId="a">
                        {rechartsData.map((entry: RechartsDataType, index: number) => {
                            const idx = data.data[index].values.findIndex(
                                el => el.name === de.name
                            );
                            const elem = idx >= 0 ? data.data[index].values[idx] : undefined;
                            const elemColor = elem
                                ? elem.color
                                    ? elem.color
                                    : color_light_blue
                                : color_light_blue; // TODO: define defaultColor
                            return (
                                <Cell
                                    key={index}
                                    fill={
                                        overloadTool.isMoreThanTargetLoad(entry)
                                            ? overloadTool.setOverColorToRed(entry, elemColor)
                                            : elemColor
                                    }
                                />
                            );
                        })}
                        <LabelList
                            content={
                                <BarLabel
                                    entityName={de.name}
                                    showEntityName={de.showEntityName}
                                    showValue={de.showValue}
                                    data={data}
                                />
                            }
                            valueAccessor={valueAccessor(de.name)}
                        />
                    </Bar>
                ))}
                {<Tooltip content={UserTooltip} cursor={false} />}
            </BarChart>
        </ResponsiveContainer>
    );
};
