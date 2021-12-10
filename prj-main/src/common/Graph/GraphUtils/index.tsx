/* ReCharts uses specific format for input data */
import { GraphData, RechartsDataType } from '../../types';

export const convertGraphDataToRechartsData = (d: GraphData): RechartsDataType[] => {
    let arr: RechartsDataType[] = new Array<RechartsDataType>();
    for (let bar of d.data) {
        const toPush = {
            bin: bar.bin,
        };
        for (let barValue of bar.values) {
            Object.defineProperty(toPush, barValue.name, {
                value: barValue.value,
                enumerable: true,
            });
        }
        arr.push(toPush);
    }
    return arr;
};

/* Standard method, offered by ReCharts */
export const valueAccessor =
    (attribute: string) =>
    ({ payload }: { payload: any }) => {
        return payload[attribute];
    };
