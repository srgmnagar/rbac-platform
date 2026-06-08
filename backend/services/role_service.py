from sqlalchemy.orm import Session
from ..models import Role
from ..schemas import RoleCreate

class RoleService:
    @staticmethod
    def create_role(db: Session, role_data: RoleCreate) -> Role:
        """Create a new role"""
        db_role = Role(name=role_data.name, description=role_data.description)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role
    
    @staticmethod
    def list_roles(db: Session) -> list:
        """List all roles"""
        return db.query(Role).all()
    
    @staticmethod
    def get_role(db: Session, role_id: int) -> Role:
        """Get a specific role by ID"""
        return db.query(Role).filter(Role.id == role_id).first()
