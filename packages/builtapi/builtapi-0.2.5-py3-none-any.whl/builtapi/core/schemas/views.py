from typing import Any, Generic, TypeVar, Union, Optional, List, Dict

from pydantic import BaseModel, Field

from builtapi.core.schemas.common import CreatedAtOrderBy, NameOrderBy, UpdatedAtOrderBy
import builtapi.core.schemas.mongo as mongo_schemas
from builtapi.core.schemas.records import RecordDataSchema, RecordFilterSchema, RecordSkipSchema, RecordTakeSchema

RecordTakeSchema = mongo_schemas.MongoLimitSchema
RecordSkipSchema = mongo_schemas.MongoSkipSchema
RecordFilterSchema = mongo_schemas.MongoFilterSchema
RecordProjectionSchema = mongo_schemas.MongoProjectionSchema
RecordVariablesSchema = mongo_schemas.MongoLetSchema
RecordSortSchema = mongo_schemas.MongoSortSchema
ViewPipelineSchema = mongo_schemas.MongoPipelineSchema

# DATA


class Entity(BaseModel):
    name: str


class View(BaseModel):
    """
    Dataclass describes View in BuiltAPI
    """
    id: str
    createdAt: str
    updatedAt: str
    name: str
    pipeline: List[Dict]
    entityId: str


class ViewsList(BaseModel):
    """
    Dataclass describes Views as list
    """
    skip: int
    take: int
    count: int
    total: int
    items: List[View]


class ViewSchemaField(BaseModel):
    name: str
    path: List[str]
    count: int
    type: str
    probability: int
    has_duplicates: bool
    types: List[Dict]


class ViewSchema(BaseModel):
    count: Optional[Union[int, None]] = None
    fields: Optional[Union[List[ViewSchemaField], None]] = None


# METHODS

class SearchViewSchema(BaseModel):
    name: Optional[str] = None


OrderByViewSchema = List[Union[NameOrderBy, CreatedAtOrderBy, UpdatedAtOrderBy]]


class ListViewsSchema(BaseModel):
    skip: int = 0
    take: int = 100
    entityId: Optional[str] = None
    search: Optional[SearchViewSchema] = None
    orderBy: Optional[OrderByViewSchema] = {"name": "asc"}


class ListByWorkspaceViewsSchema(BaseModel):
    skip: int = 0
    take: int = 100
    search: Optional[SearchViewSchema] = None
    orderBy: Optional[OrderByViewSchema] = {"name": "asc"}


class OneByIdViewSchema(BaseModel):
    viewId: str


class SchemaViewSchema(BaseModel):
    viewId: str


class RecordsViewSchema(BaseModel):
    viewId: str
    skip: RecordSkipSchema
    take: RecordTakeSchema
    sort: Optional[RecordSortSchema] = None
    filter: Optional[RecordFilterSchema] = None
    projection: Optional[RecordProjectionSchema] = None
    variables: Optional[RecordVariablesSchema] = None


class RecordsViewTotalSchema(BaseModel):
    viewId: str
    filter: Optional[RecordFilterSchema] = None
    projection: Optional[RecordProjectionSchema] = None


class CreateViewSchema(BaseModel):
    entityId: str
    name: str
    pipeline: ViewPipelineSchema


class UpdateViewSchema(BaseModel):
    viewId: str
    name: str
    pipeline: ViewPipelineSchema


class RemoveViewSchema(BaseModel):
    viewId: str


# OUTPUTS
class ViewRecord(RecordDataSchema):
    class Config:
        allow_population_by_field_name = True


T = TypeVar('T')


class ViewListRecordModel(BaseModel, Generic[T]):
    skip: int
    take: int
    count: int
    items: List[T]
    hasMore: bool


class ViewRecordsList(ViewListRecordModel[ViewRecord]):
    pass


class ViewRecordsTotal(BaseModel):
    data: int
