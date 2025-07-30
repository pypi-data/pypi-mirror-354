from typing import Annotated, Generic, TypeVar, Union, ForwardRef, Dict, List, Any
from enum import Enum
import re

from pydantic import Field, RootModel, conint, BaseModel

# Field Name
field_name_regex = re.compile(r'^[^.\\$]+$')
FieldNameSchema = Annotated[str, Field(pattern=field_name_regex)]

# Skip and Take
SkipSchema = Annotated[conint(ge=0), Field(default=0)]
TakeSchema = Annotated[conint(ge=1, le=1000), Field(default=100)]


# Sort

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class NameOrderBy(BaseModel):
    name: SortOrder


class CreatedAtOrderBy(BaseModel):
    created_at: SortOrder


class UpdatedAtOrderBy(BaseModel):
    updated_at: SortOrder


# Literals
LiteralSchema = Union[str, int, float, bool, None]

# List Schema
T = TypeVar('T')


class ListModel(BaseModel, Generic[T]):
    skip: int
    take: int
    count: int
    total: int
    items: List[T]
