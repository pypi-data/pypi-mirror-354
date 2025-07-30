from typing import Generic, TypeVar, Union, Optional, List, Any, Annotated, Dict

from pydantic import BaseModel, Field

from builtapi.core.schemas.entities import EntityIdSchema
from builtapi.core.schemas.mongo import (
    MongoFilterSchema,
    MongoLimitSchema,
    MongoPipelineSchema,
    MongoProjectionSchema,
    MongoSkipSchema,
    MongoLetSchema,
    MongoDataSchema,
    MongoSortSchema
)
from builtapi.core.schemas.common import ListModel

# FIELDS
RecordIdSchema = Annotated[str, Field(description="record id")]
RecordTakeSchema = MongoLimitSchema
RecordSkipSchema = MongoSkipSchema
RecordFilterSchema = MongoFilterSchema
RecordProjectionSchema = MongoProjectionSchema
RecordVariablesSchema = MongoLetSchema
RecordPipelineSchema = MongoPipelineSchema
RecordMultipleSchema = bool
RecordUpsertSchema = bool
RecordSoftSchema = bool
RecordDataSchema = MongoDataSchema
RecordSortSchgema = MongoSortSchema


class RecordPipelineInfoSchema(BaseModel):
    id: str


class RecordBaseSchema(BaseModel):
    entityId: EntityIdSchema


# INPUTS
class RecordListInputSchema(RecordBaseSchema):
    skip: RecordSkipSchema
    take: RecordTakeSchema
    filter: Optional[RecordFilterSchema] = None
    sort: Optional[MongoSortSchema] = None
    projection: Optional[RecordProjectionSchema] = None


class RecordGetOneInputSchema(RecordBaseSchema):
    filter: Optional[RecordFilterSchema] = None
    projection: Optional[RecordProjectionSchema] = None


class RecordCreateSchema(BaseModel):
    data: RecordDataSchema


class RecordCreateOneInputSchema(RecordCreateSchema):
    entityId: EntityIdSchema


class RecordReplaceSchema(BaseModel):
    filter: RecordFilterSchema
    data: RecordDataSchema
    upsert: Optional[RecordUpsertSchema] = False


class RecordReplaceOneInputSchema(RecordReplaceSchema):
    entityId: EntityIdSchema


class RecordUpdateSchema(BaseModel):
    filter: RecordFilterSchema
    data: RecordDataSchema
    upsert: Optional[RecordUpsertSchema] = False


class RecordUpdateOneInputSchema(RecordUpdateSchema):
    entityId: EntityIdSchema


class RecordRemoveSchema(BaseModel):
    filter: RecordFilterSchema


class RecordRemoveOneInputSchema(RecordRemoveSchema):
    entityId: EntityIdSchema


class RecordUpdateManyInputSchema(RecordUpdateSchema):
    entityId: EntityIdSchema


class RecordRemoveManyInputSchema(RecordRemoveSchema):
    entityId: EntityIdSchema


T = TypeVar('T')


class RecordBulkInputSchema(BaseModel, Generic[T]):
    entityId: EntityIdSchema
    items: List[T]


class RecordCreateBulkInputSchema(RecordBulkInputSchema[RecordCreateSchema]):
    pass


class RecordReplaceBulkInputSchema(RecordBulkInputSchema[RecordReplaceSchema]):
    pass


class RecordUpdateBulkInputSchema(RecordBulkInputSchema[RecordUpdateSchema]):
    pass


class RecordRemoveBulkInputSchema(RecordBulkInputSchema[RecordRemoveSchema]):
    pass


RecordSchemaInputSchema = RecordBaseSchema

# OUTPUTS


class Record(BaseModel):
    id: str = Field(..., alias='_id')
    data: RecordDataSchema
    meta: Dict[str, Any] = None
    pipelines: Optional[Dict[str, Any]] = None

    class Config:
        allow_population_by_field_name = True


class RecordsList(ListModel[Record]):
    pass


class UpdateManyResult(BaseModel):
    acknowledged: bool
    modifiedCount: int
    upsertedId: Optional[List[str]] = None
    upsertedCount: int
    matchedCount: int


class RemoveManyResult(BaseModel):
    acknowledged: bool
    deletedCount: int


class BulkResultErrors(BaseModel):
    code: int
    index: int
    errmsg: str
    op: Dict


class BulkResult(BaseModel):
    errors: List[BulkResultErrors]
    insertedIds: Dict[str, str]
    insertedCount: int
    upsertedIds: Dict[str, str]
    upsertedCount: int
    matchedCount: int
    modifiedCount: int
    deletedCount: int
