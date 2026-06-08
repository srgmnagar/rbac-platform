from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserRoleAssign, RoleResponse
from ..services.user_permission_service import UserPermissionService
from ..services.role_service import RoleService

router = APIRouter(prefix="/user-roles", tags=["user-roles"])

@router.post("", status_code=201)
def assign_user_to_role(
    assignment: UserRoleAssign,
    db: Session = Depends(get_db)
):
    """Assign a user to a role"""
    # Verify role exists
    role = RoleService.get_role(db, assignment.role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Assign user to role
    result = UserPermissionService.assign_user_to_role(db, assignment.user_id, assignment.role_id)

    return {"status": "success", "message": f"User {assignment.user_id} assigned to role {role.name}", "data": result}

@router.get("", response_model=list[dict])
def list_user_roles(db: Session = Depends(get_db)):
    """List all user-role assignments"""
    from ..models import user_roles, Role

    stmt = db.query(user_roles, Role).join(Role).all()
    result = []
    for assignment, role in stmt:
        result.append({
            "user_id": assignment.user_id,
            "role_id": role.id,
            "role_name": role.name
        })

    return result

@router.get("/by-user/{user_id}", response_model=list[RoleResponse])
def get_user_roles(user_id: str, db: Session = Depends(get_db)):
    """Get all roles for a specific user"""
    from ..models import Role, user_roles

    roles = db.query(Role).join(user_roles).filter(user_roles.c.user_id == user_id).all()
    return roles