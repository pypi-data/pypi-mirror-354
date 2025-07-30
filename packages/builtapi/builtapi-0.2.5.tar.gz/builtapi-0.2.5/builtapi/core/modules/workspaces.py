from typing import Dict, Optional, Any

import requests
from loguru import logger

from builtapi.core.modules.common import BaseModule, trpc_api_call
import builtapi.core.schemas.workspaces as workspaces_schemas


class WorkspacesModule(BaseModule):
    @trpc_api_call(url="/trpc/workspaces.list", method="get",
                   return_type=workspaces_schemas.WorkspacesList,
                   schema_class=workspaces_schemas.ListWorkspaceSchema)
    def list(self,
             skip: int = 0,
             take: int = 100,
             search: Optional[Dict[str, Any]] = None
             ) -> workspaces_schemas.WorkspacesList:
        """List available workspaces"""
        return {
            "skip": skip,
            "take": take,
            "search": search
        }

    @trpc_api_call(url="/trpc/workspaces.oneById", method="get",
                   return_type=workspaces_schemas.Workspace,
                   schema_class=workspaces_schemas.OneByIdWorkspaceSchema)
    def get_current(self) -> workspaces_schemas.Workspace:
        """Get current workspace"""
        return {}

    @trpc_api_call(url="/trpc/workspaces.create", method="post",
                   return_type=workspaces_schemas.Workspace,
                   schema_class=workspaces_schemas.CreateWorkspaceSchema)
    def create(self, name: str) -> workspaces_schemas.Workspace:
        """Create new workspace"""
        return {
            "name": name
        }

    @trpc_api_call(url="/trpc/workspaces.update", method="post",
                   return_type=workspaces_schemas.Workspace,
                   schema_class=workspaces_schemas.UpdateWorkspaceSchema)
    def update(self, name: str) -> workspaces_schemas.Workspace:
        """Update current workspace"""
        return {
            "name": name
        }

    @trpc_api_call(url="/trpc/workspaces.remove", method="post",
                   return_type=workspaces_schemas.Workspace,
                   schema_class=workspaces_schemas.RemoveWorkspaceSchema)
    def remove(self) -> workspaces_schemas.Workspace:
        """Remove current workspace"""
        return {}

    @trpc_api_call(url="/trpc/workspaces.leave", method="post",
                   return_type=workspaces_schemas.Workspace,
                   schema_class=workspaces_schemas.LeaveWorkspaceSchema)
    def leave(self) -> workspaces_schemas.Workspace:
        """Leave current workspace"""
        return {}
