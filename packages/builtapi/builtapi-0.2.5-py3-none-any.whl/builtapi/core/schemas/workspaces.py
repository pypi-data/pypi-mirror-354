from dataclasses import dataclass
from typing import Union, Optional, List, Annotated

from pydantic import BaseModel, Field, StringConstraints

WorkspaceIdSchema = Annotated[str, Field(description=('Entity UUID'))]
WorkspaceNameSchema = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=64)]


class Workspace(BaseModel):
    """
    Dataclass describes Workspace in BuiltAPI
    """
    id: Optional[Union[WorkspaceIdSchema, None]] = None
    created_at: Optional[Union[str, None]] = None
    updated_at: Optional[Union[str, None]] = None
    name: WorkspaceNameSchema


class WorkspacesList(BaseModel):
    """
    Dataclass describes Workspaces as list
    """
    take: Optional[Union[int, None]] = None
    count: Optional[Union[int, None]] = None
    total: Optional[Union[int, None]] = None
    items: Optional[Union[List[Workspace], None]] = None

# METHODS


class SearchWorkspaceSchema(BaseModel):
    name: Optional[str] = None


class ListWorkspaceSchema(BaseModel):
    skip: Optional[int] = None
    take: Optional[int] = None
    search: Optional[SearchWorkspaceSchema] = None


class OneByIdWorkspaceSchema(BaseModel):
    pass


class RemoveWorkspaceSchema(BaseModel):
    pass


class CreateWorkspaceSchema(BaseModel):
    name: str


class UpdateWorkspaceSchema(BaseModel):
    name: str


class LeaveWorkspaceSchema(BaseModel):
    pass
