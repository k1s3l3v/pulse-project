import React from 'react';
import { Customer, Project, User } from '../types';
import { LetteredAvatar } from '../LetteredAvatar';

export const Avatar = ({
    entity,
    borderRadius,
    imgClassName,
}: {
    entity: User | Project | Customer;
    borderRadius?: number;
    imgClassName?: string;
}) => {
    if ((entity as Project).project_id) {
        const project: Project = entity as Project;
        return project.avatar ? (
            <img className={imgClassName} src={project.avatar} alt="" />
        ) : (
            <LetteredAvatar entity={project} borderRadius={borderRadius} />
        );
    }
    if ((entity as Customer).customer_id) {
        const customer: Customer = entity as Customer;
        return customer.avatar ? (
            <img className={imgClassName} src={customer.avatar} alt="" />
        ) : (
            <LetteredAvatar entity={customer} borderRadius={borderRadius} />
        );
    }
    if ((entity as User).staff_id) {
        const user: User = entity as User;
        return user.avatar ? (
            <img className={imgClassName} src={user.avatar} alt="" />
        ) : (
            <LetteredAvatar entity={user} borderRadius={borderRadius} />
        );
    }
    return <></>;
};
