from typing import Union, Optional

from pydantic import BaseModel


class UserProfile(BaseModel):
    """
    Dataclass describes User profile
    """
    id: str
    createdAt: str
    updatedAt: str
    externalId: str
    email: str
    name: str


class GetUserProfileSchema(BaseModel):
    pass


class UpdateUserSchema(BaseModel):
    name: str
