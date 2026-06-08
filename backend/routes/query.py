from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserPermissionsResponse
from ..services.user_permission_service import UserPermissionService

router = APIRouter(prefix="/query", tags=["query"])

@router.get("/user-permissions", response_model=UserPermissionsResponse)
def get_user_permissions(user_id: str, db: Session = Depends(get_db)):
    """
    Get all permissions for a user.
    Used by SDK to check what a user can do.
    """
    permissions = UserPermissionService.get_user_permissions(db, user_id)

    return UserPermissionsResponse(
        status="success",
        user_id=user_id,
        data=permissions
    )
