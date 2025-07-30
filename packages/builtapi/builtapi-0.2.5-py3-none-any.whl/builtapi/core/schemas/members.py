from typing import Union, Optional, List
from enum import Enum

from pydantic import BaseModel

from builtapi.core.schemas.users import UserProfile


class MemberRoles(str, Enum):
    owner = 'OWNER'
    admin = 'ADMIN'
    user = 'USER'


class Member(BaseModel):
    """
    Dataclass describes Member in BuiltAPI
    """
    id: str
    createdAt: str
    updatedAt: str
    workspaceId: str
    userId: str
    role: MemberRoles
    user: Optional[UserProfile] = None


class MembersList(BaseModel):
    """
    Dataclass describes Members as list
    """
    take: int
    count: int
    total: int
    items: List[Member]


# INPUTS
class ListMembersSchema(BaseModel):
    skip: int
    take: int


class OneByIdMemberSchema(BaseModel):
    id: str


class CurrentMemberSchema(BaseModel):
    pass


class CreateMemberSchema(BaseModel):
    email: str
    role: MemberRoles


class UpdateMemberSchema(BaseModel):
    id: str
    role: MemberRoles


class RemoveMemberSchema(BaseModel):
    id: str
