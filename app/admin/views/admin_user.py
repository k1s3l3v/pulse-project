from .permissions import AdminView


class AdminUserView(AdminView):
    extra_columns = ['roles']
