import json

from datetime import datetime
from flask import flash
from flask_admin import helpers
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import BaseForm
from flask_admin.model import typefmt
from markupsafe import Markup
from typing import List, Tuple, Type

from ...models import BaseORM
from ...services import cruds
from ...utils import run_asyncio_coroutine


def json_formatter(view: 'BaseView', value: dict):
    json_value = json.dumps(value, ensure_ascii=False, indent=2)
    return Markup('<pre>{}</pre>'.format(json_value))


def datetime_formatter(view: 'BaseView', value: datetime):
    return value.strftime('%d.%m.%Y %H:%M')


TYPE_FORMATTERS = typefmt.BASE_FORMATTERS.copy()
TYPE_FORMATTERS[dict] = json_formatter
TYPE_FORMATTERS[datetime] = datetime_formatter


class BaseView(ModelView):
    can_export = True
    can_set_page_size = True
    column_display_pk = True
    column_type_formatters = TYPE_FORMATTERS
    extra_columns = []

    def __init__(self, model: Type[BaseORM], *args, **kwargs):
        if self.form_excluded_columns is None:
            self.form_excluded_columns = ('created_at', 'updated_at')
        else:
            self.form_excluded_columns += ('created_at', 'updated_at')

        if self.column_list is None:
            self.column_list = list(model.__table__.columns.keys())

        self.form_overrides = self.form_overrides or {}

        kwargs['name'] = kwargs.get('name', helpers.prettify_class_name(model.__name__[:-3]))
        kwargs['url'] = kwargs.get('url', model.__tablename__)
        super(BaseView, self).__init__(model, *args, **kwargs)

    def get_column_names(self, only_columns: List[str], excluded_columns: List[str]) -> List[Tuple[str, str]]:
        only_columns += self.extra_columns
        return super(BaseView, self).get_column_names(only_columns, excluded_columns)

    def create_model(self, form: BaseForm):
        crud = getattr(cruds, self.model.__name__[:-3], None)
        if crud is None:
            return super(BaseView, self).create_model(form)
        else:
            crud: Type[cruds.Base]
            try:
                data = {field_name: field_data for field_name, field_data in form.data.items()}
                model = run_asyncio_coroutine(crud.create(self.session, data))
                crud.commit(self.session)
                self._on_model_change(form, model, True)
            except Exception as ex:
                if not self.handle_view_exception(ex):
                    flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
                return False
            else:
                self.after_model_change(form, model, True)
            return model

    def update_model(self, form: BaseForm, model: BaseORM):
        crud = getattr(cruds, self.model.__name__[:-3], None)
        if crud is None:
            return super(BaseView, self).update_model(form, model)
        else:
            crud: Type[cruds.Base]
            try:
                self._on_model_change(form, model, False)
                data = {field_name: field_data for field_name, field_data in form.data.items()}
                for pk_name in crud.model.get_pk_names():
                    data[pk_name] = getattr(model, pk_name)
                model = run_asyncio_coroutine(crud.update(self.session, data))
                crud.commit(self.session)
            except Exception as ex:
                if not self.handle_view_exception(ex):
                    flash(gettext('Failed to update record. %(error)s', error=str(ex)), 'error')
                return False
            else:
                self.after_model_change(form, model, False)
            return True

    def delete_model(self, model: BaseORM):
        crud = getattr(cruds, self.model.__name__[:-3], None)
        if crud is None:
            return super(BaseView, self).delete_model(model)
        else:
            crud: Type[cruds.Base]
            try:
                self.on_model_delete(model)
                run_asyncio_coroutine(crud.delete(self.session, *model.get_pk_values()))
                crud.commit(self.session)
            except Exception as ex:
                if not self.handle_view_exception(ex):
                    flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')
                return False
            else:
                self.after_model_delete(model)
            return True
