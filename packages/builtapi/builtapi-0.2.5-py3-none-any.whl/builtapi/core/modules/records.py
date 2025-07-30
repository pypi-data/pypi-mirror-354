from packaging.version import Version
from typing import Dict, Any, Optional, List

from builtapi.core.modules.common import BaseModule, trpc_api_call, rest_api_call
import builtapi.core.schemas.records as records_schemas
from builtapi.utils import get_version


class RecordsModule(BaseModule):

    def list(self,
             entityId: str,
             filter: Optional[Dict[str, Any]] = None,
             take: int = 100,
             skip: int = 0,
             sort: Optional[Dict[str, str]] = None,
             projection: Optional[Dict[str, bool]] = None):
        """
        List records with optional search and ordering.
        BuiltAPI version before 0.1.0 return total in list response. After 0.1.0, total is returned in separate response.
        """
        input = {
            "entityId": entityId,
            "filter": filter,
            "take": take,
            "skip": skip,
            "sort": sort,
            "projection": projection
        }

        request_body = records_schemas.RecordListInputSchema(**input).model_dump(
                    mode="json", exclude_unset=True, exclude_none=True)

        #request records list
        list_response = self.session.post("/trpc/records.list", json=request_body)
        list_result = list_response.json()
        list_result_data = list_result['result']['data']
        
        version_str = list_response.headers['x-builtapi-version']
        version = get_version(version_str)
        if version < Version("0.1.0"):
            return records_schemas.RecordsList(
                skip=list_result_data['skip'],
                take=list_result_data['take'],
                count=list_result_data["count"],
                total=list_result_data["total"],
                items=list_result_data["items"]
            )

        #request total
        total_response = self.session.post("/trpc/records.total", json=request_body)
        total_result = total_response.json()

        records_list = records_schemas.RecordsList(
            skip=list_result_data['skip'],
            take=list_result_data['take'],
            count=list_result_data["count"],
            total=total_result['result']['data']['total'],
            items=list_result_data["items"]
        )

        return records_list

    @trpc_api_call(url="/trpc/records.getOne", method="get",
                   return_type=records_schemas.Record,
                   schema_class=records_schemas.RecordGetOneInputSchema)
    def get_one(self,
                entityId: str,
                filter: Optional[Dict[str, Any]] = None,
                projection: Optional[Dict[str, bool]] = None):
        """
        Return one Record
        """
        return {
            "entityId": entityId,
            "filter": filter,
            "projection": projection
        }

    @trpc_api_call(url="/trpc/records.createOne", method="post",
                   return_type=records_schemas.Record,
                   schema_class=records_schemas.RecordCreateOneInputSchema)
    def create_one(self,
                   entityId: str,
                   data: Dict):
        """
        Create a new record.
        """
        return {
            "entityId": entityId,
            "data": data
        }

    @trpc_api_call(url="/trpc/records.replaceOne", method="post",
                   return_type=records_schemas.Record,
                   schema_class=records_schemas.RecordReplaceOneInputSchema)
    def replace_one(self,
                    entityId: str,
                    filter: Dict[str, Any],
                    data: Dict,
                    upsert: Optional[bool] = False):
        return {
            "entityId": entityId,
            "filter": filter,
            "data": data,
            "upsert": upsert
        }

    @trpc_api_call(url="/trpc/records.updateOne", method="post",
                   return_type=records_schemas.Record,
                   schema_class=records_schemas.RecordUpdateOneInputSchema)
    def update_one(self,
                   entityId: str,
                   filter: Dict[str, Any],
                   data: Dict,
                   upsert: Optional[bool] = False):
        return {
            "entityId": entityId,
            "filter": filter,
            "data": data,
            "upsert": upsert
        }

    @trpc_api_call(url="/trpc/records.removeOne", method="post",
                   return_type=records_schemas.Record,
                   schema_class=records_schemas.RecordRemoveOneInputSchema)
    def remove_one(self,
                   entityId: str,
                   filter: Dict[str, Any]):
        return {
            "entityId": entityId,
            "filter": filter
        }

    @trpc_api_call(url="/trpc/records.updateMany", method="post",
                   return_type=records_schemas.UpdateManyResult,
                   schema_class=records_schemas.RecordUpdateManyInputSchema)
    def update_many(self,
                    entityId: str,
                    filter: Dict[str, Any],
                    data: Dict,
                    upsert: Optional[bool] = False):
        return {
            "entityId": entityId,
            "filter": filter,
            "data": data,
            "upsert": upsert
        }

    @trpc_api_call(url="/trpc/records.removeMany", method="post",
                   return_type=records_schemas.RemoveManyResult,
                   schema_class=records_schemas.RecordRemoveManyInputSchema)
    def remove_many(self,
                    entityId: str,
                    filter: Dict[str, Any]):
        return {
            "entityId": entityId,
            "filter": filter
        }

    @rest_api_call(url="/api/entities/{entityId}/records/bulk", method="post",
                   return_type=records_schemas.BulkResult,
                   schema_class=records_schemas.RecordCreateBulkInputSchema)
    def create_bulk(self,
                    entityId: str,
                    items: List[Dict]):
        return {
            "entityId": entityId,
            "items": items
        }

    @rest_api_call(url="/api/entities/{entityId}/records/bulk", method="put",
                   return_type=records_schemas.BulkResult,
                   schema_class=records_schemas.RecordReplaceBulkInputSchema)
    def replace_bulk(self,
                     entityId: str,
                     items: List[Dict]):
        return {
            "entityId": entityId,
            "items": items
        }

    @rest_api_call(url="/api/entities/{entityId}/records/bulk", method="patch",
                   return_type=records_schemas.BulkResult,
                   schema_class=records_schemas.RecordUpdateBulkInputSchema)
    def update_bulk(self,
                    entityId: str,
                    items: List[Dict]):
        return {
            "entityId": entityId,
            "items": items
        }

    @rest_api_call(url="/api/entities/{entityId}/records/bulk", method="delete",
                   return_type=records_schemas.BulkResult,
                   schema_class=records_schemas.RecordRemoveBulkInputSchema)
    def remove_bulk(self,
                    entityId: str,
                    items: List[Dict]):
        return {
            "entityId": entityId,
            "items": items
        }
