export type staffViewStyle = 'list' | 'grid';

export type User = {
    avatar: string | null;
    birthdate: string | null;
    email: string;
    fte_load: number;
    is_active: boolean;
    location_id: number | null;
    login_id: string;
    login_type: string;
    name: string;
    nickname: string;
    patronymic: string;
    phone: string | null;
    primary_skill_id: number | null;
    projects: StaffProject[];
    social_networks: StaffSocialNetwork[];
    staff_id: number;
    surname: string;
    title_id: number | null;
    unit_id: number | null;

    //bio: UserBio;
    load: GraphData; //TODO: Remove
};

export type StaffProject = {
    project_id: number;
    date_start: string;
    date_end: string;
    fte_load: number;
    type: string;
    assigner_id: number | null;
};

export type UserBio = {
    active: boolean;
    primary_skill: { name: string } | null;
    location: { name: string } | null;
    birthdate: string;
    slack: string;
    email: string;
    phone: string;
};

export type FilterOptions = {
    value: string;
    label: string;
};

export type Filter = {
    name: string;
    options: FilterOptions[];
    defaultValue: FilterOptions;
    value?: FilterOptions;
};

/* Types for fetch-related stuff */
export type StatusError = {
    message: string;
    status: number;
};

export type FetchError = {
    error: StatusError;
};
/*-------------------------------*/

/* Types for Bio on various pages */
export type Emoji = {
    symbol: string;
    label: string;
};

export type BioItem = {
    //This type describing single element in User's Bio: e.g. location
    text: string;
    textClass: string;
    icon: string | Emoji;
    clickable: boolean;
    iconStyle?: object;
    link?: string;
    additionalJSX?: JSX.Element;
    additionalGlobalStyle?: object;
};
/*--------------------------------*/

/* Type for graph data */
export type GraphData = {
    data: BarData[];
    targetLoad?: number;
    entities: DataEntity[]; // Made JUST for simplicity purposes!
};

export type DataEntity = {
    name: string;
    showEntityName?: boolean;
    showValue?: boolean;
};

export type BarData = {
    bin: string /* e.g. Jan, Feb, Mar */;
    values: ItemData[];
};

export type EntityStatus = 'book' | 'ass';

export type ItemData = {
    name: string /* e.g. DPCP */;
    value: number /* e.g. 0.5 */;
    status?: EntityStatus;
    color?: string;
};
/*---------------------*/

export type RechartsDataType = {
    bin: string;
    [key: string]: number | string; // 'string' wont break anything, but that will not be use-case ever
};

export type CustomRoute = {
    name: string;
    url: string;
    matchingUrls?: string[];
};

export type Theme = 'dark' | 'light';

export type Tree = {
    head: TreeNode;
    isAbstract: boolean;
};

export type TreeNode = {
    children: TreeNode[];
    parent_id: number;
    parent: TreeNode | null;
    name: string | JSX.Element;
    id: number;
    addable: boolean;
};

export type Searchable = User | Project;

/* Backend compatibility stuff */
export type Location = {
    location_id: number;
    name: string;
};

export type PricingModel = 'TIME_AND_MATERIAL' | 'FIXED_PRICE';

export type Role = {
    role_id: number;
    name: string;
};

export type ProjectStaffRole = {
    staff_id: number;
    role_id: number;
};

export type Project = {
    project_id: number;
    customer_id: number | null;
    name: string;
    description: string | null;
    date_start: string;
    date_end: string | null;
    is_active: boolean;
    fte_load: number;
    pricing_model: PricingModel;
    staff_roles: ProjectStaffRole[];
    avatar: string | null;
};

export type ProjectStaffRoleWithStaff = {
    staff: User;
    role_id: number;
};

export type ProjectWithStaff = Project & {
    staff_roles: ProjectStaffRoleWithStaff[];
};

export type Skill = {
    skill_id: number;
    name: string;
    description: string | null;
};

export type StaffSocialNetwork = {
    social_network_id: number;
    link: string;
};

export type SocialNetwork = {
    social_network_id: number;
    name: string;
};

export type Title = {
    title_id: number;
    name: string;
};

export type Entities = {
    locations: Location[];
    projects: Project[];
    skills: Skill[];
    social_networks: SocialNetwork[];
    subordinate_staff: User[];
    titles: Title[];
    units_hierarchy: UnitsHierarchy;
    customers: Customer[];
    projects_leads: User[];
    projects_sortable_properties: string[];
    roles: Role[];
    projects_main_roles: ProjectsMainRoles;
};

export type EntityAlias =
    | 'locations'
    | 'projects'
    | 'skills'
    | 'social_networks'
    | 'subordinate_staff'
    | 'titles'
    | 'units_hierarchy'
    | 'customers'
    | 'projects_leads'
    | 'projects_sortable_properties'
    | 'roles'
    | 'projects_main_roles';

export type UnitsHierarchy = {
    unit_id: number;
    name: string;
    owner: {
        staff_id: number;
        name: string;
        surname: string;
    } | null;
    head_department_id: number | null;
    subordinate_departments: UnitsHierarchy[];
};

export type Entity =
    | User
    | Project
    | Title
    | Location
    | Skill
    | SocialNetwork
    | UnitsHierarchy
    | Customer
    | string
    | Role;

export type SingleEntityArray =
    | User[]
    | Project[]
    | Title[]
    | Location[]
    | Skill[]
    | SocialNetwork[]
    | Customer[]
    | Role[];

export type SingleEntityMap =
    | {
          [key: number]: User;
      }
    | {
          [key: number]: Project;
      }
    | {
          [key: number]: Title;
      }
    | {
          [key: number]: Location;
      }
    | {
          [key: number]: Skill;
      }
    | {
          [key: number]: SocialNetwork;
      }
    | {
          [key: number]: Customer;
      }
    | {
          [key: number]: Role;
      };

export type MultipleSingleEntityMap = {
    [key in EntityAlias]?: SingleEntityMap;
};

export type Unit = {
    unit_id: number;
    name: string;
    description: string | null;
    owner: User | null;
    location_id: number | null;
    head_department_id: number | null;
    team: User[];
};

export type CreateUnit = {
    owner_id: number;
    name: string;
    description?: string;
    location_id?: number;
    head_department_id: number;
};

export type Customer = {
    customer_id: number;
    name: string;
    akaunting_customer_id: number;
    avatar: string | null;
    phone: string | null;
    email: string | null;
    contact_person: string | null;
    description: string | null;
    location: string | null;
};

export type ProjectsMainRoles = {
    project_lead: Role;
    project_accountant: Role;
};
