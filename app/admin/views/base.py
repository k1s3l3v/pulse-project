import json

from datetime import datetime
from flask import flash
from flask_admin import helpers
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import BaseForm
from flask_admin.form.fields import fields
from flask_admin.model import typefmt
from markupsafe import Markup
from sqlalchemy import inspect
from typing import List, Optional, Tuple, Type, Union
from wtforms.validators import DataRequired, InputRequired

from ...models import BaseORM
from ...services import cruds
from ...utils import run_asyncio_coroutine


def json_formatter(view: 'BaseView', value: dict) -> Markup:
    json_value = json.dumps(value, ensure_ascii=False, indent=2)
    return Markup('<pre>{}</pre>'.format(json_value))


def datetime_formatter(view: 'BaseView', value: datetime) -> str:
    return value.strftime('%d.%m.%Y %H:%M')


TYPE_FORMATTERS = typefmt.BASE_FORMATTERS.copy()
TYPE_FORMATTERS[dict] = json_formatter
TYPE_FORMATTERS[datetime] = datetime_formatter


class BaseView(ModelView):
    can_export = True

    can_set_page_size = True

    column_display_pk = True

    column_type_formatters = TYPE_FORMATTERS

    extra_columns = ()

    extra_pk_fields = ()

    required_fields_on_create = ()

    def __init__(self, model: Type[BaseORM], session, *args, **kwargs):
        if self.form_excluded_columns is None:
            self.form_excluded_columns = ('created_at', 'updated_at')
        else:
            self.form_excluded_columns += ('created_at', 'updated_at')

        if self.column_list is None:
            self.column_list = list(model.__table__.columns.keys())

        self.model = model

        self.form_extra_fields = self.form_extra_fields or {}
        self.form_args = self.form_args or {}
        mapper = inspect(self.model).mapper
        properties = {prop.key: prop for prop in mapper.iterate_properties}
        converter = self.model_form_converter(session, self)
        form_columns = self.form_columns
        self.form_columns = self.extra_pk_fields
        for form_extra_pk_field_name in self.extra_pk_fields:
            if form_extra_pk_field_name not in self.form_extra_fields and form_extra_pk_field_name in properties:
                field = converter.convert(self.model, mapper, form_extra_pk_field_name,
                                          properties[form_extra_pk_field_name],
                                          self.form_args.get(form_extra_pk_field_name), False)
                if field is not None:
                    self.form_extra_fields[form_extra_pk_field_name] = field
        self.form_columns = form_columns

        kwargs['name'] = kwargs.get('name', helpers.prettify_class_name(model.__name__[:-3]))
        kwargs['url'] = kwargs.get('url', model.__tablename__)
        super(BaseView, self).__init__(model, session, *args, **kwargs)

    def get_column_names(self, only_columns: List[str], excluded_columns: List[str]) -> List[Tuple[str, str]]:
        only_columns += self.extra_columns
        return super(BaseView, self).get_column_names(only_columns, excluded_columns)

    def get_create_form(self) -> Type[BaseForm]:
        form = super(BaseView, self).get_create_form()

        for field_name in self.required_fields_on_create:
            field = getattr(form, field_name, None)
            if field is not None:
                field.kwargs['validators'].append(DataRequired())

        return form

    @classmethod
    def _make_form_field_disabled(cls, form: BaseForm, field_name: str):
        field = getattr(form, field_name, None)
        if isinstance(field, fields.Field):
            field.render_kw = field.render_kw or {}
            field.render_kw['readonly'] = True
            field.render_kw['disabled'] = True
            field.validators = list(filter(lambda v: not isinstance(v, InputRequired), field.validators))

    def edit_form(self, obj: Optional[BaseORM] = None) -> BaseForm:
        form = super(BaseView, self).edit_form(obj)

        crud = getattr(cruds, self.model.__name__[:-3], None)
        if crud is not None:
            crud: Type[cruds.Base]
            columns_to_update_names = [column.key for column in crud.columns_to_update]
            for field_name in filter(lambda f: f not in columns_to_update_names, form.data.keys()):
                self._make_form_field_disabled(form, field_name)
        else:
            for pk_name in self.model.get_pk_names():
                not_id_pk_name = pk_name[:-3] if '_id' in pk_name else pk_name
                self._make_form_field_disabled(form, pk_name)
                if not_id_pk_name != pk_name:
                    self._make_form_field_disabled(form, not_id_pk_name)

        return form

    def create_model(self, form: BaseForm) -> Union[BaseORM, bool]:
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
                self.session.rollback()
                return False
            else:
                self.after_model_change(form, model, True)
            return model

    def update_model(self, form: BaseForm, model: BaseORM) -> bool:
        crud = getattr(cruds, self.model.__name__[:-3], None)
        if crud is None:
            return super(BaseView, self).update_model(form, model)
        else:
            crud: Type[cruds.Base]
            try:
                self._on_model_change(form, model, False)
                data = {field_name: field_data for field_name, field_data in form.data.items()}
                model = run_asyncio_coroutine(crud.update(self.session, data, *model.get_pk_values()))
                crud.commit(self.session)
            except Exception as ex:
                if not self.handle_view_exception(ex):
                    flash(gettext('Failed to update record. %(error)s', error=str(ex)), 'error')
                self.session.rollback()
                return False
            else:
                self.after_model_change(form, model, False)
            return True

    def delete_model(self, model: BaseORM) -> bool:
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
                self.session.rollback()
                return False
            else:
                self.after_model_delete(model)
            return True
