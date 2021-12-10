import { GraphData, Project, SingleEntityMap, User } from '../common/types';
import Decimal from 'decimal.js';
import { getEntityById } from '../common/utils';

export const mapMonthNumberToBin = (month: number): string => {
    switch (month) {
        case 0:
            return 'Jan';
        case 1:
            return 'Feb';
        case 2:
            return 'Mar';
        case 3:
            return 'Apr';
        case 4:
            return 'May';
        case 5:
            return 'Jun';
        case 6:
            return 'Jul';
        case 7:
            return 'Aug';
        case 8:
            return 'Sep';
        case 9:
            return 'Oct';
        case 10:
            return 'Nov';
        case 11:
            return 'Dec';
        default:
            return 'NaN';
    }
};

export const getFTEColor = (curLoad: Decimal, targetLoad: number): string => {
    if (curLoad.equals(targetLoad)) return 'exact';
    if (curLoad.comparedTo(targetLoad) === 1) return 'more';
    return 'less';
};

export const calculateCurrentLoad = (load: GraphData): Decimal => {
    if (!load) return new Decimal(0.0); // TODO: Right now there is no LOAD in USER
    const now = new Date();
    const bin = mapMonthNumberToBin(now.getMonth());
    const data = load.data;
    const curLoad = data.find(el => el.bin === bin);
    if (curLoad) {
        let x = new Decimal(0.0);
        for (let el of curLoad.values) {
            if (el.status !== 'book') x = x.plus(el.value);
        }
        return x.dividedBy(100);
    }
    return new Decimal(0.0);
};

export const getProjectRole = (
    project: Project,
    map: SingleEntityMap,
    roleId: number
): User | undefined => {
    const role = project.staff_roles.find(el => el.role_id === roleId);
    if (role) {
        return getEntityById(role.staff_id, map) as User;
    }
    return undefined;
};
