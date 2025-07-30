from packaging.version import Version
from typing import List, Union, Optional, Dict, Any

import requests
from loguru import logger

from builtapi.core.modules.common import BaseModule, trpc_api_call
import builtapi.core.schemas.views as views_schemas
from builtapi.utils import get_version

class ViewsModule(BaseModule):

    @trpc_api_call(url="/trpc/views.list", method="get",
                   return_type=views_schemas.ViewsList, schema_class=views_schemas.ListViewsSchema)
    def list(self,
             skip: int = 0,
             take: int = 100,
             entity_id: Optional[str] = None,
             search: Optional[Dict[str, Any]] = None,
             orderBy: Optional[List[Dict[str, str]]] = None) -> views_schemas.ViewsList:
        return {
            "entityId": entity_id,
            "skip": skip,
            "take": take,
            "search": search,
            "orderBy": orderBy
        }

    @trpc_api_call(url="/trpc/views.list", method="get",
                   return_type=views_schemas.ViewsList, schema_class=views_schemas.ListByWorkspaceViewsSchema)
    def list_by_workspace(self,
                          skip: int = 0,
                          take: int = 100,
                          search: Optional[Dict[str, Any]] = None,
                          orderBy: Optional[List[Dict[str, str]]] = None) -> views_schemas.ViewsList:
        return {
            "skip": skip,
            "take": take,
            "search": search,
            "orderBy": orderBy
        }

    @trpc_api_call(url="/trpc/views.oneById", method="get",
                   return_type=views_schemas.View, schema_class=views_schemas.OneByIdViewSchema)
    def get_one_by_id(self,
                      view_id: str):
        return {
            "viewId": view_id
        }

    @trpc_api_call(url="/trpc/views.schema", method="get",
                   return_type=views_schemas.ViewSchema, schema_class=views_schemas.SchemaViewSchema)
    def get_schema(self,
                   view_id: str):
        return {
            "viewId": view_id
        }

    @trpc_api_call(url="/trpc/views.create", method="post",
                   return_type=views_schemas.View, schema_class=views_schemas.CreateViewSchema)
    def create(self,
               entity_id: str,
               name: str,
               pipeline: List[Dict]):
        return {
            "entityId": entity_id,
            "name": name,
            "pipeline": pipeline
        }

    @trpc_api_call(url="/trpc/views.update", method="post",
                   return_type=views_schemas.View, schema_class=views_schemas.UpdateViewSchema)
    def update(self,
               view_id: str,
               name: str,
               pipeline: List[Dict]):
        return {
            "viewId": view_id,
            "name": name,
            "pipeline": pipeline
        }

    @trpc_api_call(url="/trpc/views.remove", method="post",
                   return_type=views_schemas.View, schema_class=views_schemas.RemoveViewSchema)
    def remove(self, view_id: str):
        return {
            "viewId": view_id
        }
    
    @trpc_api_call(url="/trpc/views.records", method="post",
                     return_type=views_schemas.ViewRecordsList, schema_class=views_schemas.RecordsViewSchema)
    def get_records(self,
                view_id: str,
                skip: int,
                take: int,
                sort: Optional[Dict[str, str]] = None,
                filter: Optional[Dict[str, Any]] = None,
                projection: Optional[Dict[str, bool]] = None,
                variables: Optional[Dict[str, Any]] = None):
        return {
            "viewId": view_id,
            "skip": skip,
            "take": take,
            "sort": sort,
            "filter": filter,
            "projection": projection,
            "variables": variables
        }
    
    def get_records_total(self, view_id: str):
        input_data = {
            "viewId": view_id
        }
        
        response = self.session.post("/trpc/views.recordsTotal", json=input_data)
        result = response.json()

        version_str = response.headers['x-builtapi-version']
        version = get_version(version_str)
        if version < Version("0.1.0"):
            return result['result']['data']
        
        return result['result']['data']['total']
