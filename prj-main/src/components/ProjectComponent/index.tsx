import React, {useState} from 'react';
import {
    BioItem,
    Customer,
    MultipleSingleEntityMap,
    ProjectCriterion,
    ProjectPulse,
    ProjectWithStaff,
    SingleEntityMap,
    Title
} from '../../common/types';
import './index.scss';
import { useHistory } from 'react-router-dom';
import {getEntityNameById, renderWithIcon} from "../../common/utils";
import Modal from "./Modal/modal";

export const ProjectComponent = (
    {
        entities,
        project,
        project_criteria,
        project_pulse,
        titles,
    }: {
        entities: MultipleSingleEntityMap;
        project: ProjectWithStaff;
        project_criteria: ProjectCriterion[];
        project_pulse: ProjectPulse;
        titles: Title[];
    }) => {
    const [modalActive, setModalActive] = useState(false);
    const [projectCriterionId, setProjectCriterionId] = useState(0);
    const [projectCriterionName, setProjectCriterionName] = useState('');
    let history = useHistory();
    const staff = (): {[a: number]: string} => {
        let arr: {[a: number]: string} = {};
        if (project.staff_roles) {
            for (let i of project.staff_roles) arr[i.staff_id] = i.staff.name + ' ' + i.staff.surname;
        }
        return arr;
    }
    const staff_ = staff();
    const criteria = (): {[a: number]: string} => {
        let arr: {[a: number]: string} = {};
        if (project_criteria) {
            for (let i of project_criteria) arr[i.project_criterion_id] = i.name;
        }
        return arr;
    }
    const criteria_ = criteria();
    const renderTopEmojiTextLine = (): BioItem[] => {
        const resArr: BioItem[] = [
            {
                text: project.is_active ? 'Active' : 'Not Active',
                textClass: 'text-14 font-arial weight-400 list-stuff',
                icon: {
                    symbol: project.is_active ? '✅' : '🚫',
                    label: 'active',
                },
                clickable: false,
            },
            {
                text: project.pricing_model === 'FIXED_PRICE' ? 'Fixed Price' : 'Time and Material',
                textClass: 'text-14 font-arial weight-400 list-stuff',
                icon: {
                    symbol: project.pricing_model === 'FIXED_PRICE' ? '🛠️' : '🕒️',
                    label: 'pricing',
                },
                clickable: false,
            },
        ];
        return resArr;
    };
    const expandBioList = (): BioItem[] => {
        let customerLocation = 'N/A';
        if (entities.customers && project.customer_id) {
            const loc = (entities.customers[project.customer_id] as Customer).location;
            if (loc) customerLocation = loc;
        }

        const resArr: BioItem[] = [
            {
                text: getEntityNameById(project.customer_id, entities.customers as SingleEntityMap),
                textClass: 'text-14 font-arial weight-700 list-stuff',
                icon: {
                    symbol: '📜',
                    label: 'title',
                },
                clickable: false,
            },
            {
                text: customerLocation,
                textClass: 'text-14 font-arial weight-400 list-stuff',
                icon: {
                    symbol: '📍',
                    label: 'location',
                },
                clickable: false,
            },
            {
                text: `${project.staff_roles.length} / ${project.fte_load} FTE`,
                textClass: `text-14 font-arial weight-400 list-stuff`,
                icon: {
                    symbol: '⌛',
                    label: 'FTE',
                },
                clickable: false,
            },
        ];
        return resArr;
    };

    const project_roles = () => {
        let mas: {[p: number]: string} = {};
        if (project && entities.customers) {
            if (project.customer_id) {
                const customer = (entities.customers[project.customer_id] as Customer);
                mas[9] = customer.name;
                if (customer.contact_person) mas[8] = customer.contact_person;
                else mas[8] = '';
            }
        }
        if (project && project.staff_roles) {
            for (let i of project.staff_roles) {
                console.log(project.staff_roles)
                if (i.role_id === 1) mas[i.role_id] = i.staff.name + ' ' + i.staff.surname;
                if (i.role_id === 2) mas[i.role_id] = i.staff.name + ' ' + i.staff.surname;
            }
        }
        return mas;
    }

    const res = project_roles();

    const assign = (): {[str: string]: string} => {
        let mas: {[str: string]: string} = {};
        if (project.staff_roles && entities.titles) {
            for (let i of project.staff_roles) {
                if (i.staff.title_id)
                    mas[i.staff.name + ' ' + i.staff.surname] = (entities.titles[i.staff.title_id] as Title).name;
            }
        }
        return mas;
    }

    const res_ass = assign();

    const lead = res_ass[res[1]];
    const acc = res_ass[res[2]];

    const bar = (
        {
            name,
            value,
            normal_threshold,
            max_value,
            project_criterion_id,
        } : {
            name: string;
            value: number;
            normal_threshold: number;
            max_value: number;
            project_criterion_id: number;
        } ) => {
        const abs_max = 1.5;
        let color;
        if (value < max_value) {
            if (value < normal_threshold)
                color = '#e24444'
            else
                color = '#ffad3f'
        } else
            color = '#2eb67d'

        return (<tr>
            <td className="text-18 font-ptmono weight-400 edit-button" onClick={() => {
                setModalActive(true);
                setProjectCriterionId(project_criterion_id);
                setProjectCriterionName(criteria_[project_criterion_id]);
            }}>
                {'✏️'}
            </td>
            <td className="text-18 font-ptmono weight-900 b-t-w">
                <div style={{
                    background: color,
                    width: (value / abs_max * 100).toString() + "%",
                    height: 25,
                    paddingLeft: "5%",
                }}>
                    <span className="text-20 font-ptmono weight-900 criterion-name">{name}</span>
                    <span className="text-20 font-ptmono weight-900 value">{value}</span>
                </div>
            </td>
        </tr>);
    }

    const bars = () => {
        let bars_ = [];
        if (project_criteria) {
            for (let i of project_criteria) {
                let criterion_id = (i.project_criterion_id).toString();
                if (project_pulse.status && project_pulse.status.latest_grades[criterion_id]) {
                    bars_.push(
                        bar({
                            name: i.name,
                            value: project_pulse.status.latest_grades[criterion_id].value,
                            normal_threshold: i.normal_threshold,
                            max_value: i.max_value,
                            project_criterion_id: i.project_criterion_id,
                        })
                    )
                }
            }
            return bars_;
        }
    }

    const pulse_value = () => {
        let color;
        if (project_pulse.status && project_pulse.status.aggregated_value) {
            if (project_pulse.status.aggregated_value < 5) {
                if (project_pulse.status.aggregated_value < 3)
                    color = '#e24444'
                else
                    color = '#ffad3f'
            } else
                color = '#2eb67d'
            return (
                <span
                    style={{background: color}} className="text-22 font-ptmono weight-900 b-t-w">
                    {project_pulse.status.aggregated_value}
                </span>
            )
        }
    }


    const logs = () => {
        let arr = [];
        let arrow;
        if (project_pulse.status && project_pulse.status.latest_log) {
            for (let i of project_pulse.status.latest_log) {
                if (i.new_value > i.old_value) {
                    arrow = '⬆️';
                } else {
                    if (i.new_value == i.old_value) arrow = '➡️';
                    else arrow = '⬇️';
                }
                if (i.author_id) {
                    arr.push(
                        <div>
                            <span className="text-18 font-ptmono weight-900 b-t-l">{i.date} </span>
                            <span
                                className="text-18 font-ptmono weight-900 b-t-w">{criteria_[i.project_criterion_id]} {i.old_value} </span>
                            <span className="text-18 font-ptmono weight-900 b-t-l">{arrow} </span>
                            <span className="text-18 font-ptmono weight-900 b-t-w">{i.new_value} </span>
                            <span className="text-18 font-ptmono weight-400 b-t-l">by {staff_[i.author_id]}</span>
                            <br />
                            <span className="text-18 font-ptmono weight-400 b-t-w">{i.comment}</span>
                            <br/>
                        </div>
                    )
                }
            }
            return arr;
        }
    }

    return (
        <div className="project-container">
            <div className="project-container__header">
                <span
                    className="text-36 font-ptmono weight-400 backbutton"
                    onClick={() => history.goBack()}>
                    {'⬅️'}
                </span>
                <span className="text-36 font-ptmono weight-400"> {project.name}</span>
            </div>
            <div className="project-container__dates">
                <span className="text-24 font-ptmono weight-900 project-container__dates_date-1">
                    Date start:
                    <span className="text-20 font-ptmono weight-400 text"> {project.date_start} </span>
                </span>
                <span className="text-24 font-ptmono weight-900 project-container__dates_date-2">
                    Date created:
                    <span className="text-20 font-ptmono weight-400 text"> {project.date_start}</span>
                </span>
                <span className="project-container__dates_date-3">
                    {renderTopEmojiTextLine().map(value => renderWithIcon(value))}
                    {expandBioList().map(value => renderWithIcon(value))}
                </span>
            </div>
            <div className="project-container__des">
                <span className="text-24 font-ptmono weight-900">Description:</span>
                <br />
                <br />
                <span className="text-16 font-ptmono weight-400">{project.description}</span>
            </div>
            <br />
            <br />
            <br />
            <div className="column">
                <span className="text-24 font-ptmono weight-900 b-t-w">Project Customer:</span>
                <br />
                <br />
                <span className="text-24 font-ptmono weight-900 project-container__project_customer">{res[9]} </span>
                <br />
                <br />
                <span className="text-18 font-ptmono weigth 400 b-t-w">Contact person: </span>
                <span className="text-24 font-ptmono weight-900 project-container__project_customer">{res[8]} </span>
            </div>
            <div className="column">
                <span className="text-24 font-ptmono weight-900 b-t-w">Project Account:</span>
                <br />
                <br />
                <span className="text-24 font-ptmono weight-900 project-container__project_account">{res[2]}</span>
                <br />
                <br />
                📜
                <span className="text-22 font-ptmono weight-900 b-t-w"> {acc}</span>
            </div>
            <div className="column">
                <span className="text-24 font-ptmono weight-900 b-t-w">Project Lead:</span>
                <br />
                <br />
                <span className="text-24 font-ptmono weight-900 project-container__project_lead">{res[1]} </span>
                <br />
                <br />
                📜
                <span className="text-22 font-ptmono weight-900 b-t-w"> {lead}</span>
                <br />
                <br />
                <br />
                <br />
            </div>
            <div >
                <div className="column">
                <span className="text-24 font-ptmono weight-900 b-t-w">
                    Pulse: {pulse_value()}
                    <span className="text-24 font-ptmono weight-900">
                    <table>
                        {bars()}
                    </table>
                    </span>
                </span>
                </div>
                <div>
                    <span className="text-24 font-ptmono weight-900 column-2">Latest pulse log:</span>
                </div>
                <div className="column_2">
                    {logs()}
                </div>
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
                <br />
            </div>
            <Modal active={modalActive} setActive={setModalActive} project_criterion_id={projectCriterionId} project_criterion_name={projectCriterionName} project_id={project.project_id}/>
        </div>
    );
};
