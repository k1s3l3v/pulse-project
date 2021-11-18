from wtforms.validators import DataRequired

from .permissions import AdminView


class ProjectCriterionValueView(AdminView):
    extra_columns = ('project_criterion',)

    extra_pk_fields = ('project_id', 'date')

    form_args = {
        'author_id': {
            'validators': [DataRequired()]
        }
    }
