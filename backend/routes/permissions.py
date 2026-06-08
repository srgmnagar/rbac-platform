from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import PermissionCreate, PermissionResponse
from ..services.permission_service import PermissionService

router = APIRouter(prefix="/permissions", tags=["permissions"])

@router.get("", response_model=list[PermissionResponse])
def list_permissions(db: Session = Depends(get_db)):
    """Get all permissions"""
    permissions = PermissionService.list_permissions(db)
    return permissions

@router.post("", response_model=PermissionResponse, status_code=201)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    """Create a new permission"""
    try:
        return PermissionService.create_permission(db, permission)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))