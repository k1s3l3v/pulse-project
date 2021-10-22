from .permissions import AdminView


class AdminAccessRuleView(AdminView):
    extra_columns = ['role']
