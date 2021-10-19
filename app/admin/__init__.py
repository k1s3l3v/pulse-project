from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, url_for
from flask_admin import Admin, helpers
from flask_security import Security, SQLAlchemySessionUserDatastore
from sqlalchemy.orm import Session
from sqlalchemy.orm.base import manager_of_class
from typing import Optional, Type, Union

from . import views
from .models import AdminAccessRuleORM, AdminBaseORM, AdminUserORM, AdminRoleORM
from ..config import settings
from ..db import create_session
from ..models import orms
from ..templates import TEMPLATES_DIR
from ..utils import commit_transaction, get_db_initialization_data


_admin_session: Optional[Session]


def _get_view(model_name: str, is_public: bool) -> Type[Union[views.AdminView, views.UserView]]:
    view = getattr(views, model_name + 'View', None)
    if view is None:
        view = views.UserView if is_public else views.AdminView
    return view


def init_admin_tables():
    AdminBaseORM.connect_db(_admin_session)

    if _admin_session.query(AdminUserORM).filter_by(email=settings.ADMIN_USER_NAME).first() is None:
        admin_user = AdminUserORM(email=settings.ADMIN_USER_NAME, password=settings.ADMIN_USER_PASSWORD, active=True)
        _admin_session.add(admin_user)
        commit_transaction(_admin_session, False)

    initialization_data = get_db_initialization_data()
    for role_data in initialization_data['admin_roles']:
        if _admin_session.query(AdminRoleORM).filter_by(name=role_data['name']).first() is None:
            role = AdminRoleORM(name=role_data['name'], description=role_data['description'])
            _admin_session.add(role)
            commit_transaction(_admin_session, False)

    admin_user = _admin_session.query(AdminUserORM).filter_by(email=settings.ADMIN_USER_NAME).first()
    admin_role = _admin_session.query(AdminRoleORM).filter_by(name='admin').first()
    if admin_user is not None and admin_role is not None and admin_role not in admin_user.roles:
        admin_user.roles.append(admin_role)
        _admin_session.add(admin_user)
        commit_transaction(_admin_session, False)


def init_app(fast_app: FastAPI):
    global _admin_session

    admin_app = Flask(__name__, template_folder=f'../../{TEMPLATES_DIR}')
    admin_url = f'{settings.ADMIN_URL_PREFIX}/admin'

    admin_app.secret_key = settings.SECRET_KEY
    admin_app.config['FLASK_ADMIN_SWATCH'] = settings.FLASK_ADMIN_SWATCH
    admin_app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
    admin_app.config['SECURITY_REGISTERABLE'] = settings.SECURITY_REGISTERABLE
    admin_app.config['SECURITY_PASSWORD_SALT'] = settings.SECURITY_PASSWORD_SALT
    admin_app.config['SECURITY_REGISTER_URL'] = '/register'
    admin_app.config['SECURITY_POST_REGISTER_VIEW'] = admin_url
    admin_app.config['SECURITY_LOGIN_URL'] = '/login'
    admin_app.config['SECURITY_POST_LOGIN_VIEW'] = admin_url
    admin_app.config['SECURITY_LOGOUT_URL'] = '/logout'
    admin_app.config['SECURITY_POST_LOGOUT_VIEW'] = admin_url

    _admin_session = create_session()

    user_datastore = SQLAlchemySessionUserDatastore(_admin_session, AdminUserORM, AdminRoleORM)
    security = Security(admin_app, user_datastore)

    admin = Admin(admin_app, name='MADO pulse admin', base_template='master.html', template_mode='bootstrap3', url='/')
    admin.brand_url = admin_url

    admin.add_view(views.AdminUserView(AdminUserORM, _admin_session))
    admin.add_view(views.AdminView(AdminRoleORM, _admin_session))
    admin.add_view(views.AdminAccessRuleView(AdminAccessRuleORM, _admin_session))

    for class_name in dir(orms):
        cls = getattr(orms, class_name)
        try:
            if issubclass(cls, orms.BaseORM) and manager_of_class(cls) is not None:
                admin.add_view(_get_view(class_name[:-3], cls.is_public)(cls, _admin_session))
        except TypeError:
            pass

    @security.context_processor
    def security_context_processor():
        return dict(admin_base_template=admin.base_template, admin_view=admin.index_view, get_url=url_for, h=helpers)

    admin_app_wsgi = WSGIMiddleware(admin_app)
    admin_fast_app = FastAPI()

    admin_fast_app.mount(path='/', app=admin_app_wsgi, name='admin_app')
    fast_app.mount(path=admin_url, app=admin_fast_app)


def disconnect_db():
    _admin_session.close()
