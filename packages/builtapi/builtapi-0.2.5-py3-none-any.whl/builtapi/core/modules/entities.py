from typing import Dict, Union, Optional, Any, List

from loguru import logger

from builtapi.core.modules.common import BaseModule, trpc_api_call
import builtapi.core.schemas.entities as entities_schemas


class EntitiesModule(BaseModule):
    @trpc_api_call(url="/trpc/entities.list", method="get",
                   return_type=entities_schemas.EntitiesList,
                   schema_class=entities_schemas.ListEntitySchema)
    def list(self,
             skip: int = 0,
             take: int = 100,
             search: Optional[Dict[str, Any]] = None,
             orderBy: Optional[List[Dict[str, str]]] = None) -> entities_schemas.EntitiesList:
        """
        List entities with optional search and ordering.
        """
        return {
            "skip": skip,
            "take": take,
            "search": search,
            "orderBy": orderBy
        }

    @trpc_api_call(url="/trpc/entities.oneById", method="get",
                   return_type=entities_schemas.Entity,
                   schema_class=entities_schemas.GetOneEntityByIdSchema)
    def oneById(self,
                entityId: str) -> entities_schemas.Entity:
        """
        Retrieve a single entity by its ID.
        """
        return {"entityId": entityId}

    @trpc_api_call(url="/trpc/entities.create", method="post",
                   return_type=entities_schemas.Entity,
                   schema_class=entities_schemas.CreateEntitySchema)
    def create(self,
               name: str,
               type: entities_schemas.EntityType = entities_schemas.EntityType.REGULAR,
               dateSettings: Optional[List[entities_schemas.DateSettings | dict]] = None,
               jsonSchema: Optional[Dict] = None) -> entities_schemas.Entity:
        """
        Create a new entity.
        """
        return {
            "type": type,
            "name": name,
            "dateSettings": dateSettings,
            "jsonSchema": jsonSchema
        }

    @trpc_api_call(url="/trpc/entities.update", method="post",
                   return_type=entities_schemas.Entity,
                   schema_class=entities_schemas.UpdateEntitySchema)
    def update(self,
               entityId: str,
               name: Optional[str] = None,
               dateSettings: Optional[List[entities_schemas.DateSettings | dict]] = None,
               jsonSchema: Optional[Dict] = None) -> entities_schemas.Entity:
        """
        Update an existing entity.
        """
        return {
            "entityId": entityId,
            "name": name,
            "dateSettings": dateSettings,
            "jsonSchema": jsonSchema
        }

    @trpc_api_call(url="/trpc/entities.remove", method="post",
                   return_type=entities_schemas.Entity,
                   schema_class=entities_schemas.RemoveEntitySchema)
    def remove(self,
               entityId: str) -> entities_schemas.Entity:
        """
        Remove an entity by its ID.
        """
        return {"entityId": entityId}
