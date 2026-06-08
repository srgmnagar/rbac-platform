from pydantic import BaseModel
from typing import List, Optional

# Role schemas
class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

# Permission schemas
class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

# Assignment schemas
class RolePermissionAssign(BaseModel):
    role_id: int
    permission_ids: List[int]

class UserRoleAssign(BaseModel):
    user_id: str
    role_id: int

# Response schemas
class UserPermissionsResponse(BaseModel):
    status: str = "success"
    user_id: str
    data: List[str]  # List of permission names
