import React, {useEffect, useState} from 'react';
import "./index.scss"
import ProjectsService from "../../../services/ProjectsService";


// @ts-ignore
const Modal = ({active, setActive, project_criterion_id, project_criterion_name, project_id}) => {
    let today = new Date();
    let dd = String(today.getDate()).padStart(2, '0');
    let mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    let yyyy = today.getFullYear();

    const date = yyyy + '-' + mm + '-' + dd;
    const [value, setValue] = useState('');
    const [comment, setComment] = useState('');
    const sendRequest = () => {
        if (parseInt(value) >= 0 && comment !== '' && parseInt(value) <= 5) {
            const prj_c = {'project_criterion_id': project_criterion_id, 'date': date, 'value': parseInt(value), 'comment': comment};
            const criterionResp = ProjectsService.putCriterion(prj_c, project_id)
            Promise.all([criterionResp]).then(el => {window.location.reload()})
        }
    }
    return (
        <div className={active ? "modal active": 'modal'} onClick={() => setActive(false)}>
            <div className={active ? "modal__content active": "modal__content"} onClick={e => e.stopPropagation()}>
                <span className="text-24 font-ptmono weight-900">Add new log for {project_criterion_name}</span>
                <br/>
                <br/>
                <span className="text-20 font-ptmono weight 400">Input new value for criterion:</span>
                <br/>
                <input
                    name="value"
                    type="string"
                    value={value}
                    onChange={(e) => {setValue(e.target.value)}}
                    placeholder="Input in [0;5]"/>
                <br/>
                <br/>
                <br/>
                <span className="text-20 font-ptmono weight 400">Input comment for adding:</span>
                <input
                    name="comment"
                    type="string"
                    value={comment}
                    onChange={(e) => {setComment(e.target.value)}}
                    placeholder="Some comment"/>
                <button className="button" onClick={() => sendRequest()}>SAVE</button>
            </div>
        </div>
    )
}

export default Modal;
