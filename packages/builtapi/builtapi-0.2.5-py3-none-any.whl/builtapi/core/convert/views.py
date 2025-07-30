from typing import Union

from builtapi.core.schemas.views import View, ViewsList, ViewSchema, ViewSchemaField


def views_list(method):
    """ Validation wrap output from List views endpoint """

    def inner(*args, **kwargs) -> ViewsList:
        obtained_views = method(*args, **kwargs)
        if obtained_views.get('items') is None:
            items = []
        else:
            # Generate entities
            items = [View(id=i.get('id'), created_at=i.get('createdAt'),
                          updated_at=i.get('updatedAt'), name=i.get('name'),
                          pipeline=i.get('pipeline'), entity_id=i.get('entityId')) for i in obtained_views['items']]
        return ViewsList(take=obtained_views.get('take'), count=obtained_views.get('take'),
                         total=obtained_views.get('total'), items=items)

    return inner


def view(method):
    """ Validation wrap output for view objects """

    def inner(*args, **kwargs) -> Union[View, None]:
        obtained_view = method(*args, **kwargs)
        if obtained_view is None:
            return None
        else:
            return View(id=obtained_view.get('id'), created_at=obtained_view.get('createdAt'),
                        updated_at=obtained_view.get('updatedAt'), name=obtained_view.get('name'),
                        pipeline=obtained_view.get('pipeline'), entity_id=obtained_view.get('entityId'))

    return inner


def view_schema(method):
    """ Validation wrap output for view schema objects """

    def inner(*args, **kwargs) -> Union[ViewSchema, None]:
        obtained_schema = method(*args, **kwargs)
        if obtained_schema is None:
            return None
        else:
            if obtained_schema.get('fields') is None:
                fields = []
            else:
                fields = [ViewSchemaField(name=field.get('name'), path=field.get('path'),
                                          count=field.get('count'), type=field.get('type'),
                                          probability=field.get('probability'),
                                          has_duplicates=field.get('hasDuplicates'),
                                          types=field.get('types'),) for field in obtained_schema['fields']]
            return ViewSchema(count=obtained_schema.get('count'), fields=fields)

    return inner
