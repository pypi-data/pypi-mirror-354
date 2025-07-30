from typing import Union

from builtapi.core.schemas.entities import EntitiesList, Entity, RemovedEntities


def entities_list(method):
    """ Validation wrap output from List entities endpoint """

    def inner(*args, **kwargs) -> EntitiesList:
        obtained_entities = method(*args, **kwargs)
        if obtained_entities.get('items') is None:
            items = []
        else:
            # Generate entities
            items = [Entity(id=i.get('id'), created_at=i.get('createdAt'),
                            updated_at=i.get('updatedAt'), name=i.get('name'),
                            workspace_id=i.get('workspaceId'), date_settings=i.get('dateSettings'),
                            geo_settings=i.get('geoSettings'), json_schema=i.get('jsonSchema')) for i in obtained_entities['items']]
        return EntitiesList(take=obtained_entities.get('take'), count=obtained_entities.get('take'),
                            total=obtained_entities.get('total'), items=items)

    return inner


def removed_entities_list(method):
    """ Validation wrap output from List entities remove all endpoint """

    def inner(*args, **kwargs) -> RemovedEntities:
        deleted_entities = method(*args, **kwargs)
        return RemovedEntities(count=deleted_entities.get('count'))
    return inner


def entity(method):
    """ Validation wrap output for entity objects """

    def inner(*args, **kwargs) -> Union[Entity, None]:
        obtained_entity = method(*args, **kwargs)
        if obtained_entity is None:
            return None
        else:
            return Entity(id=obtained_entity.get('id'), created_at=obtained_entity.get('createdAt'),
                          updated_at=obtained_entity.get('updatedAt'), name=obtained_entity.get('name'),
                          workspace_id=obtained_entity.get('workspaceId'), date_settings=obtained_entity.get('dateSettings'),
                          geo_settings=obtained_entity.get('geoSettings'), json_schema=obtained_entity.get('jsonSchema'))

    return inner
