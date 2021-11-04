<<<<<<< HEAD
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
=======
from .permissions import AdminView


class ProjectCriterionValue(AdminView):
    extra_columns = ['project_criterion']
>>>>>>> dabb50d7e5639e890a96ccdc69e3f6e42dd98f2d
