from typing import Annotated, Dict, Any, Literal, List
from datetime import datetime

from pydantic import Field, RootModel

# ID
MongoIdSchema = Annotated[str, Field(min_length=24, max_length=24)]

# Filter
MongoFilterSchema = Dict[str, Any]

# Let
MongoLetSchema = MongoFilterSchema


class MongoDataSchema(RootModel):
    root: Dict

    def model_dump(self, *args, **kwargs):
        original_dict = super().model_dump(*args, **kwargs)
        return self._serialize_dates(original_dict)

    def __getitem__(self, item):
        return self.root[item]

    def get(self, item, default=None):
        try:
            return self.root[item]
        except KeyError as err:
            if default is None:
                raise err
            return default

    @staticmethod
    def _serialize_dates(data):
        if isinstance(data, dict):
            return {k: MongoDataSchema._serialize_dates(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [MongoDataSchema._serialize_dates(item) for item in data]
        elif isinstance(data, datetime):
            return data.isoformat()
        return data


# Pagination
MongoLimitSchema = Annotated[int, Field(gt=0, lt=10000, default=1000)]
MongoSkipSchema = Annotated[int, Field(gte=0, default=0)]

# Pipeline
MongoPipelineSchema = Annotated[List[Dict[str, Any]], Field(min_length=1)]

# Sort
MongoSortSchema = Dict[str, Literal['asc', 'desc', 1, -1]]

# Projection
MongoProjectionSchema = Dict[str, Literal[True]]
