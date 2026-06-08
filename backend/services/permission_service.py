from sqlalchemy.orm import Session
from ..models import Permission
from ..schemas import PermissionCreate

class PermissionService:
    @staticmethod
    def create_permission(db: Session, perm_data: PermissionCreate) -> Permission:
        """Create a new permission"""
        db_perm = Permission(name=perm_data.name, description=perm_data.description)
        db.add(db_perm)
        db.commit()
        db.refresh(db_perm)
        return db_perm
    
    @staticmethod
    def list_permissions(db: Session) -> list:
        """List all permissions"""
        return db.query(Permission).all()
    
    @staticmethod
    def get_permission(db: Session, permission_id: int) -> Permission:
        """Get a specific permission by ID"""
        return db.query(Permission).filter(Permission.id == permission_id).first()
