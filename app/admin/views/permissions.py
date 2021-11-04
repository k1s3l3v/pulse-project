from flask import redirect, Response, url_for
from flask_security import current_user
from typing import Optional

from .base import BaseView
from ..models import AdminAccessRuleORM


class UserView(BaseView):
    deletable = False

    def has_user_access(self, permission: str):
        access_rules = {access_rule.role: access_rule.tables
                        for access_rule in self.session.query(AdminAccessRuleORM).all()}
        for role in self.roles:
            if permission in access_rules.get(role.name, {}).get(self.name, []):
                return True
        return False

    def is_accessible(self) -> bool:
        return current_user.is_active and current_user.is_authenticated and (current_user.has_role('admin')
                                                                             or self.has_user_access('read'))

    def _handle_view(self, name: str, **kwargs) -> Optional[Response]:
        if not self.is_accessible():
            return redirect(url_for('security.login'))

        self.can_delete = current_user.has_role('admin') or self.has_user_access('delete')
        self.can_edit = current_user.has_role('admin') or self.has_user_access('edit')
        self.can_create = self.can_edit
        if current_user.has_role('read_only'):
            self.can_delete = False
            self.can_edit = False

    def is_action_allowed(self, name: str) -> bool:
        if name == 'delete':
            return current_user.has_role('admin')
        return super(UserView, self).is_action_allowed(name)


class AdminView(BaseView):
    def is_accessible(self) -> bool:
        return current_user.is_active and current_user.is_authenticated and current_user.has_role('admin')

    def _handle_view(self, name: str, **kwargs) -> Optional[Response]:
        if not self.is_accessible():
            return redirect(url_for('security.login'))
