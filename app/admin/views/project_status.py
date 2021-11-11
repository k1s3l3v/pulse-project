from .permissions import AdminView


class ProjectStatusView(AdminView):
    can_create = False

    can_edit = False
