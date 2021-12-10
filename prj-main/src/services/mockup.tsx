import { Customer, Project, Location } from '../common/types';

const getRandomInt = (max: number): number => {
    return Math.floor(Math.random() * max);
};

const capitalize = (s: string) => {
    return s.charAt(0).toUpperCase() + s.slice(1);
};

const rndGenStr = (len: number): string => {
    let text = '';
    const chars = 'abcdefghijklmnopqrstuvwxyz';
    for (let i = 0; i < len; ++i) text += chars.charAt(Math.floor(Math.random() * chars.length));
    return capitalize(text);
};

const rndGenDate = (): string => {
    return `${getRandomInt(31)}.${getRandomInt(12)}.${getRandomInt(2021)}`;
};

const rndGenBool = (): boolean => {
    return Math.random() > 0.5;
};

export const locationMockup: Location[] = [
    {
        name: rndGenStr(8),
        location_id: getRandomInt(100),
    },
    {
        name: rndGenStr(8),
        location_id: getRandomInt(100),
    },
    {
        name: rndGenStr(8),
        location_id: getRandomInt(100),
    },
    {
        name: rndGenStr(8),
        location_id: getRandomInt(100),
    },
    {
        name: rndGenStr(8),
        location_id: getRandomInt(100),
    },
    {
        name: rndGenStr(8),
        location_id: getRandomInt(100),
    },
    {
        name: rndGenStr(8),
        location_id: getRandomInt(100),
    },
    {
        name: rndGenStr(8),
        location_id: getRandomInt(100),
    },
];

export const customerMockup: Customer[] = [
    {
        name: rndGenStr(5),
        customer_id: getRandomInt(10),
        akaunting_customer_id: getRandomInt(10),
        description: rndGenStr(10),
        avatar: null,
        contact_person: null,
        location: locationMockup[getRandomInt(locationMockup.length)].name,
        email: null,
        phone: null,
    },
    {
        name: rndGenStr(5),
        customer_id: getRandomInt(10),
        akaunting_customer_id: getRandomInt(10),
        description: rndGenStr(10),
        avatar: null,
        contact_person: null,
        location: locationMockup[getRandomInt(locationMockup.length)].name,
        email: null,
        phone: null,
    },
    {
        name: rndGenStr(5),
        customer_id: getRandomInt(10),
        akaunting_customer_id: getRandomInt(10),
        description: rndGenStr(10),
        avatar: null,
        contact_person: null,
        location: locationMockup[getRandomInt(locationMockup.length)].name,
        email: null,
        phone: null,
    },
    {
        name: rndGenStr(5),
        customer_id: getRandomInt(10),
        akaunting_customer_id: getRandomInt(10),
        description: rndGenStr(10),
        avatar: null,
        contact_person: null,
        location: locationMockup[getRandomInt(locationMockup.length)].name,
        email: null,
        phone: null,
    },
    {
        name: rndGenStr(5),
        customer_id: getRandomInt(10),
        akaunting_customer_id: getRandomInt(10),
        description: rndGenStr(10),
        avatar: null,
        contact_person: null,
        location: locationMockup[getRandomInt(locationMockup.length)].name,
        email: null,
        phone: null,
    },
];

// https://developer.mozilla.org/en/docs/Web/JavaScript/Guide/Regular_Expressions#Using_Special_Characters
export function escapeRegexCharacters(str: string) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
