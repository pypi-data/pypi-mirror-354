from typing import Union

from builtapi.core.schemas.views import View


def _collect_set_of_conditions(obtained_view: View):
    is_id_string = isinstance(obtained_view.id, str)
    is_created_at_string = isinstance(obtained_view.created_at, str)
    is_updated_at_string = isinstance(obtained_view.updated_at, str)
    is_name_string = isinstance(obtained_view.name, str)
    is_pipeline_list = isinstance(obtained_view.pipeline, list)
    is_entity_id_string = isinstance(obtained_view.pipeline, str)

    return [is_id_string, is_created_at_string, is_updated_at_string, is_name_string, is_pipeline_list, is_entity_id_string]


def view_fields_not_empty(method):
    """ Check that all fields have some records """

    def inner(*args, **kwargs):
        obtained_view: Union[View, None] = method(*args, **kwargs)
        if obtained_view is None:
            return obtained_view
        else:
            # Validate output
            try:
                conditions = _collect_set_of_conditions(obtained_view)
            except Exception as ex:
                raise ValueError(f'View validation failed due to unexpected error: {ex}')

            if all(conditions) is False:
                raise ValueError('Latest view validation failed due to incompatibility')
            return obtained_view

    return inner
