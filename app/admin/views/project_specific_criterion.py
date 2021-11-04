<<<<<<< HEAD
from .permissions import AdminView


class ProjectSpecificCriterionView(AdminView):
    extra_columns = ('project_criterion',)

    extra_pk_fields = ('project_id',)
=======
from .permissions import AdminView


class ProjectSpecificCriterionView(AdminView):
    extra_columns = ['project_criterion']
>>>>>>> dabb50d7e5639e890a96ccdc69e3f6e42dd98f2d
