from enum import Enum
from datetime import datetime
from typing import Union, Optional, List, Any, Annotated, Dict

from pydantic import BaseModel, StringConstraints, model_validator, Field

from builtapi.core.schemas.common import (
    NameOrderBy,
    CreatedAtOrderBy,
    UpdatedAtOrderBy,
    SkipSchema,
    TakeSchema,
    ListModel
)

EntityIdSchema = Annotated[str, Field(description=('Entity UUID'))]
EntityNameSchema = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=64)]


class EntityType(str, Enum):
    REGULAR = 'REGULAR'
    LOGS = 'LOGS'


class DateSettingsTypes(str, Enum):
    ISO = "iso",
    MILLISECONDS = "milliseconds",
    SECONDS = "seconds",
    CUSTOM = "custom"


class DateSettings(BaseModel):
    type: DateSettingsTypes
    targetKey: str
    sourcePath: str
    format: Optional[str] = None

    @model_validator(mode="after")
    def check_custom_format(self):
        if self.type == DateSettingsTypes.CUSTOM and not self.format:
            raise ValueError('Format is required when type is CUSTOM')
        return self


class Entity(BaseModel):
    """
    Dataclass describes Entity in BuiltAPI
    """
    id: str
    createdAt: datetime
    updatedAt: datetime
    workspaceId: str
    name: EntityNameSchema
    type: EntityType
    dateSettings: Optional[List[DateSettings]] = list()
    geoSettings: Optional[List] = list()
    jsonSchema: Optional[Dict] = None


EntitiesList = ListModel[Entity]

# Input Schemas


class EntitySearchSchema(BaseModel):
    ids: Optional[List[str]] = None
    name: Optional[str] = None
    types: Optional[List[EntityType]] = None


EntityOrderBySchema = List[Union[NameOrderBy, CreatedAtOrderBy, UpdatedAtOrderBy]]


class ListEntitySchema(BaseModel):
    search: Optional[EntitySearchSchema] = None
    orderBy: Optional[EntityOrderBySchema] = {"name": "asc"}
    skip: SkipSchema
    take: TakeSchema


class GetOneEntityByIdSchema(BaseModel):
    entityId: EntityIdSchema


class CreateEntitySchema(BaseModel):
    type: EntityType
    name: EntityNameSchema
    dateSettings: Optional[List[DateSettings]] = None
    jsonSchema: Optional[Dict] = None


class UpdateEntitySchema(BaseModel):
    entityId: EntityIdSchema
    name: Optional[EntityNameSchema] = None
    dateSettings: Optional[List[DateSettings]] = None
    jsonSchema: Optional[Dict] = None


class RemoveEntitySchema(BaseModel):
    entityId: EntityIdSchema


class RemovedEntities(BaseModel):
    """
    Dataclass describes removed Entities as list
    """
    count: Optional[Union[int, None]] = None
