import React, { useEffect, useRef, useState } from 'react';
import './index.scss';
import { Customer, Project, User } from '../types';

export const LetteredAvatar = ({
    entity,
    borderRadius,
}: {
    entity: User | Project | Customer;
    borderRadius?: number;
}) => {
    const ref = useRef(null);
    const [fontSize, setFontSize] = useState<number>(0);
    const [defaultBorderRadius, setDefaultBorderRadius] = useState<number>(0);
    const [width, setWidth] = useState<number>(0);
    const [border, setBorder] = useState<boolean>(true);
    useEffect(() => {
        if (ref.current) {
            const { offsetHeight } = ref.current;
            setFontSize(offsetHeight * 0.56);
            setDefaultBorderRadius(offsetHeight * 0.146);
            setWidth(offsetHeight);
            setBorder(offsetHeight > 25);
        }
    }, [ref]);

    const getInitials = (): string => {
        if ((entity as Project).project_id) {
            const project: Project = entity as Project;
            return project.name[0] + project.name[1] || '';
        }
        if ((entity as Customer).customer_id) {
            const customer: Customer = entity as Customer;
            return customer.name[0] + customer.name[1] || '';
        }
        if ((entity as User).staff_id) {
            const user: User = entity as User;
            return user.name[0] + user.surname[0] || '';
        }
        return 'N/A';
    };

    return (
        <div
            className="lettered-avatar-wrapper"
            aria-label={entity.name}
            ref={ref}
            style={{
                borderRadius: borderRadius ? borderRadius : defaultBorderRadius,
                flex: `0 0 ${width}px`,
                width: width,
                border: border ? '' : 'none',
            }}>
            <div className="lettered-avatar" style={{ fontSize: fontSize }}>
                {getInitials()}
            </div>
        </div>
    );
};
