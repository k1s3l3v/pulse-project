from .permissions import AdminView


class ProjectSpecificCriterionView(AdminView):
    extra_columns = ('project_criterion',)

    extra_pk_fields = ('project_id',)
