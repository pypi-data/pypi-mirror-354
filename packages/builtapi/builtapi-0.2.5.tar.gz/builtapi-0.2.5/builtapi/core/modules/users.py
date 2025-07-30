from typing import Dict, Union

import requests
from loguru import logger

from builtapi.core.modules.common import BaseModule, trpc_api_call
from builtapi.core.schemas.users import UserProfile, UpdateUserSchema, GetUserProfileSchema


class UsersModule(BaseModule):

    @trpc_api_call(url="/trpc/users.profile", method="get",
                   return_type=UserProfile, schema_class=GetUserProfileSchema)
    def get_profile(self):
        return {}

    @trpc_api_call(url="/trpc/users.update", method="post",
                   return_type=UserProfile, schema_class=UpdateUserSchema)
    def update_profile(self,
                       name: str):
        return {
            "name": name
        }
