from typing import Union

from builtapi.core.schemas.workspaces import WorkspacesList, Workspace


def workspaces_list(method):
    """ Validation wrap output from List workspaces endpoint """

    def inner(*args, **kwargs) -> WorkspacesList:
        obt_workspaces = method(*args, **kwargs)
        if obt_workspaces.get('items') is None:
            items = []
        else:
            # Generate entities
            items = [Workspace(id=i.get('id'), created_at=i.get('createdAt'),
                               updated_at=i.get('updatedAt'), name=i.get('name')) for i in obt_workspaces['items']]
        return WorkspacesList(take=obt_workspaces.get('take'), count=obt_workspaces.get('take'),
                              total=obt_workspaces.get('total'), items=items)

    return inner


def workspace(method):
    """ Validation wrap output for workspace objects """

    def inner(*args, **kwargs) -> Union[Workspace, None]:
        obtained_workspace = method(*args, **kwargs)
        if obtained_workspace is None:
            return None
        return Workspace(id=obtained_workspace.get('id'), created_at=obtained_workspace.get('createdAt'),
                         updated_at=obtained_workspace.get('updatedAt'), name=obtained_workspace.get('name'))

    return inner
