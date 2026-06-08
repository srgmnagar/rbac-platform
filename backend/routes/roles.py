from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import RoleCreate, RoleResponse
from ..services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("", response_model=list[RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    """Get all roles"""
    roles = RoleService.list_roles(db)
    return roles

@router.post("", response_model=RoleResponse, status_code=201)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    """Create a new role"""
    try:
        return RoleService.create_role(db, role)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))