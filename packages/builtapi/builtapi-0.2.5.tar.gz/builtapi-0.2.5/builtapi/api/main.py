from contextlib import contextmanager
from typing import Union
from urllib.parse import urljoin

from loguru import logger

from builtapi.session import init_session
from builtapi.core.modules.entities import EntitiesModule
from builtapi.core.modules.records import RecordsModule
from builtapi.core.modules.members import MembersModule
from builtapi.core.modules.users import UsersModule
from builtapi.core.modules.views import ViewsModule
from builtapi.core.modules.workspaces import WorkspacesModule
from builtapi.settings import BUILTAPI_GATEWAY_URL, BUILTAPI_DEFAULT_WORKSPACE_ID
from builtapi.token import get_token


class BuiltAPI:
    """
    Class for interacting with BuiltAPI service
    Versions tracked by the
    """

    def __init__(self, workspace_id: str = None, token: Union[str, None] = None, url: Union[str, None] = None):
        self.token = token or get_token()
        self.url = url or BUILTAPI_GATEWAY_URL
        self.workspace_id = workspace_id or BUILTAPI_DEFAULT_WORKSPACE_ID

        for name, value in [('token', self.token),
                            ('url', self.url),
                            ('workspace_id', self.workspace_id)]:
            if value is None:
                raise ValueError(f'Configuration field {name} can not be None')

        session = init_session(self.workspace_id, self.token, self.url)

        # Modules
        self.entities = EntitiesModule(session)
        self.records = RecordsModule(session)
        self.members = MembersModule(session)
        self.users = UsersModule(session)
        self.views = ViewsModule(session)
        self.workspaces = WorkspacesModule(session)
