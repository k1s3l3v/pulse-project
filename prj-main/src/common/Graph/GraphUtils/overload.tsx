import { RechartsDataType } from '../../types';
import { color_pink } from '../../utils/constants';

export class OverloadTool {
    private _rechartsData: RechartsDataType[];
    private readonly _targetLoad: number;
    private readonly _binCounter: Array<number>;
    constructor(rechartsData: RechartsDataType[], targetLoad: number) {
        this._rechartsData = rechartsData;
        this._targetLoad = targetLoad;
        this._binCounter = new Array<number>(rechartsData.length).fill(0);
    }

    isMoreThanTargetLoad = (elem: RechartsDataType): number => {
        if (!this._targetLoad) return 0;
        const arrWithoutBin: number[] = Object.keys(elem).map(key => {
            if (key !== 'bin') return elem[key] as number; // 'as number' coming from 'number | string' in RechartsDataType
            return 0; // Neutral element for addition
        });
        const sumArr: number = arrWithoutBin.reduce((a, b): number => a + b, 0);
        if (sumArr > this._targetLoad) return sumArr;
        return 0;
    };

    mapBinsToNumber = (bin: string): number => {
        return this._rechartsData.findIndex((el: { bin: string }) => el.bin === bin);
    };

    howManyEntitiesAreOverTargetLoad = (entry: RechartsDataType): number => {
        if (!this._targetLoad) return 0;
        const arrWithoutBin = Object.keys(entry).map(key => {
            if (key !== 'bin') return entry[key];
            return 0; // Neutral element for '+'
        });
        let count = 0;
        let tmpSum = 0;
        for (let i = 1; i < arrWithoutBin.length; i++) {
            tmpSum += arrWithoutBin[i] as number;
            if (tmpSum > this._targetLoad) {
                count = arrWithoutBin.length - i;
                break;
            }
        }
        return count;
    };

    setOverColorToRed = (elem: RechartsDataType, defaultColor: string): string => {
        const numElems = Object.keys(elem).length - 1; /* Cos first is 'bin' */
        const overElements = this.howManyEntitiesAreOverTargetLoad(elem);
        const binIndex = this.mapBinsToNumber(elem.bin);
        if (this._binCounter[binIndex] > numElems - overElements - 1) {
            this._binCounter[binIndex]++;
            return color_pink;
        }
        this._binCounter[binIndex]++;
        return defaultColor;
    };
}
