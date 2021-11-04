from wtforms.validators import DataRequired

from .permissions import AdminView


class ProjectCriterionValueView(AdminView):
    extra_columns = ('project_specific_criterion',)

    extra_pk_fields = ('date',)

    form_args = {
        'author_id': {
            'validators': [DataRequired()]
        }
    }
