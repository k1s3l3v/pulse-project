from typing import Optional

from .base import Base, DictStrAny, Session
from ...config import settings
from ...exceptions import CreationError
from ...models import ProjectCriterionValueORM, ProjectStatusORM
from ...schemas import ProjectStatusCreate, ProjectStatusLatestGrade, ProjectStatusLatestLogRecord


class ProjectStatus(Base):
    model = ProjectStatusORM

    @classmethod
    def get_by_project_id(cls, db: Session, project_id: int) -> Optional[ProjectStatusORM]:
        return db.query(cls.model).filter_by(project_id=project_id).first()

    @classmethod
    async def _before_create(cls, db: Session, data: DictStrAny) -> ProjectStatusORM:
        project_status: ProjectStatusORM = cls.create_object(data)

        db_project_status = cls.get_by_id(db, project_status.project_id)
        if db_project_status is not None:
            raise CreationError('ProjectStatus',
                                f"Project status with project id '{project_status.project_id}' already exists")

        return project_status

    @classmethod
    async def update_status(cls, db: Session, project_criterion_value: ProjectCriterionValueORM):
        db_project_status = cls.get_by_project_id(db, project_criterion_value.project_id)
        project_criterion_id = str(project_criterion_value.project_criterion_id)

        latest_grade = ProjectStatusLatestGrade(project_criterion_id=project_criterion_value.project_criterion_id,
                                                date=project_criterion_value.date, value=project_criterion_value.value,
                                                comment=project_criterion_value.comment,
                                                author_id=project_criterion_value.author_id)

        latest_log_record = ProjectStatusLatestLogRecord(
            project_criterion_id=project_criterion_value.project_criterion_id, date=project_criterion_value.date,
            new_value=project_criterion_value.value, comment=project_criterion_value.comment,
            author_id=project_criterion_value.author_id)

        iso_date = project_criterion_value.date.isoformat()

        if db_project_status is not None:
            if project_criterion_id in db_project_status.latest_grades:
                latest_log_record.old_value = db_project_status.latest_grades[project_criterion_id]['value']

            latest_log_record_dict = latest_log_record.dict()
            latest_log_record_dict['date'] = iso_date
            db_project_status.latest_log.insert(0, latest_log_record_dict)
            if len(db_project_status.latest_log) > settings.LATEST_PULSE_LOG_MAX_SIZE:
                db_project_status.latest_log.pop()
            latest_grade_dict = latest_grade.dict()
            latest_grade_dict['date'] = iso_date
            db_project_status.latest_grades[project_criterion_id] = latest_grade_dict
            db_project_status.latest_updater_id = project_criterion_value.author_id
            db_project_status.latest_updated_at = project_criterion_value.date
            db_project_status.aggregated_value = min(value['value']
                                                     for value in db_project_status.latest_grades.values())
            db.add(db_project_status)
        else:
            project_status_dict = ProjectStatusCreate(project_id=project_criterion_value.project_id,
                                                      aggregated_value=project_criterion_value.value,
                                                      latest_updated_at=project_criterion_value.date,
                                                      latest_updater_id=project_criterion_value.author_id,
                                                      latest_grades={project_criterion_id: latest_grade},
                                                      latest_log=[latest_log_record]).dict()
            project_status_dict['latest_grades'][project_criterion_id]['date'] = iso_date
            project_status_dict['latest_log'][0]['date'] = iso_date
            await cls.create(db, project_status_dict)
