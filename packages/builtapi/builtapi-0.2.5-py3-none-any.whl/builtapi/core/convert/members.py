from typing import Union

from builtapi.core.schemas.members import MembersList, Member
from builtapi.core.schemas.users import UserProfile


def members_list(method):
    """ Validation wrap output from List Members endpoint """

    def inner(*args, **kwargs) -> MembersList:
        obtained_entities = method(*args, **kwargs)
        if obtained_entities.get('items') is None:
            items = []
        else:
            # Generate entities
            items = []
            for i in obtained_entities['items']:
                if i.get('user') is None:
                    user = None
                else:
                    user = UserProfile(id=i['user'].get('id'), created_at=i['user'].get('createdAt'),
                                       updated_at=i['user'].get('updatedAt'), external_id=i['user'].get('externalId'),
                                       email=i['user'].get('email'), name=i['user'].get('name'))
                current_item = Member(id=i.get('id'), created_at=i.get('createdAt'), updated_at=i.get('updatedAt'),
                                      workspace_id=i.get('workspaceId'), user_id=i.get('userId'),
                                      role=i.get('role'), user=user)
                items.append(current_item)
        return MembersList(take=obtained_entities.get('take'), count=obtained_entities.get('take'),
                           total=obtained_entities.get('total'), items=items)

    return inner


def member(method):
    """ Validation wrap output for member objects """

    def inner(*args, **kwargs) -> Union[Member, None]:
        obtained_entity = method(*args, **kwargs)
        if obtained_entity is None:
            return None
        else:
            if obtained_entity.get('user') is None:
                user = None
            else:
                user = UserProfile(id=obtained_entity['user'].get('id'), created_at=obtained_entity['user'].get('createdAt'),
                                   updated_at=obtained_entity['user'].get('updatedAt'),
                                   external_id=obtained_entity['user'].get('externalId'),
                                   email=obtained_entity['user'].get('email'),
                                   name=obtained_entity['user'].get('name'))
            return Member(id=obtained_entity.get('id'), created_at=obtained_entity.get('createdAt'),
                          updated_at=obtained_entity.get('updatedAt'), workspace_id=obtained_entity.get('workspaceId'),
                          user_id=obtained_entity.get('userId'), role=obtained_entity.get('role'),
                          user=user)

    return inner
