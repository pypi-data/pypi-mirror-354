import requests
from loguru import logger

from builtapi.core.modules.common import BaseModule, trpc_api_call
import builtapi.core.schemas.members as members_schemas


class MembersModule(BaseModule):

    @trpc_api_call(url="/trpc/members.list", method="get",
                   return_type=members_schemas.MembersList, schema_class=members_schemas.ListMembersSchema)
    def list(self,
             skip: int = 0,
             take: int = 100):
        return {
            "skip": skip,
            "take": take
        }

    @trpc_api_call(url="/trpc/members.oneById", method="get",
                   return_type=members_schemas.Member, schema_class=members_schemas.OneByIdMemberSchema)
    def one_by_id(self,
                  id: str):
        return {
            "id": id
        }

    @trpc_api_call(url="/trpc/members.current", method="get",
                   return_type=members_schemas.Member, schema_class=members_schemas.CurrentMemberSchema)
    def current(self):
        return {}

    @trpc_api_call(url="/trpc/members.create", method="post",
                   return_type=members_schemas.Member,
                   schema_class=members_schemas.CreateMemberSchema)
    def create(self,
               email: str,
               role: members_schemas.MemberRoles):
        return {
            "email": email,
            "role": role
        }

    @trpc_api_call(url="/trpc/members.update", method="post",
                   return_type=members_schemas.Member,
                   schema_class=members_schemas.UpdateMemberSchema)
    def update(self,
               id: str,
               role: members_schemas.MemberRoles):
        return {
            "id": id,
            "role": role
        }

    @trpc_api_call(url="/trpc/members.remove", method="post",
                   return_type=members_schemas.Member, schema_class=members_schemas.RemoveMemberSchema)
    def remove(self, id: str):
        return {
            "id": id
        }
