from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import RolePermissionAssign
from ..services.user_permission_service import UserPermissionService
from ..services.role_service import RoleService
from ..services.permission_service import PermissionService

router = APIRouter(prefix="/role-permissions", tags=["role-permissions"])

@router.post("", status_code=201)
def assign_permissions_to_role(
    assignment: RolePermissionAssign,
    db: Session = Depends(get_db)
):
    """Assign permissions to a role"""
    # Verify role exists
    role = RoleService.get_role(db, assignment.role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Verify all permissions exist
    for perm_id in assignment.permission_ids:
        perm = PermissionService.get_permission(db, perm_id)
        if not perm:
            raise HTTPException(status_code=404, detail=f"Permission {perm_id} not found")

    # Assign permissions
    UserPermissionService.assign_permission_to_role(db, assignment.role_id, assignment.permission_ids)

    return {"status": "success", "message": f"Assigned {len(assignment.permission_ids)} permissions to role"}