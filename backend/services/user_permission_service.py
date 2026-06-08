from sqlalchemy.orm import Session
from sqlalchemy import insert
from ..models import Role, Permission, user_roles, role_permissions

class UserPermissionService:
    @staticmethod
    def assign_user_to_role(db: Session, user_id: str, role_id: int) -> dict:
        """Assign a user to a role"""
        stmt = insert(user_roles).values(user_id=user_id, role_id=role_id)
        db.execute(stmt)
        db.commit()
        return {"user_id": user_id, "role_id": role_id}
    
    @staticmethod
    def assign_permission_to_role(db: Session, role_id: int, permission_ids: list) -> None:
        """Assign permissions to a role"""
        for perm_id in permission_ids:
            stmt = insert(role_permissions).values(role_id=role_id, permission_id=perm_id)
            try:
                db.execute(stmt)
            except:
                pass  # Already exists, ignore
        db.commit()
    
    @staticmethod
    def get_user_permissions(db: Session, user_id: str) -> list:
        """Get all permissions for a user by traversing user->roles->permissions"""
        # Get all roles for this user
        roles = db.query(Role).join(user_roles).filter(user_roles.c.user_id == user_id).all()
        
        # Get all permissions from those roles
        permissions = set()
        for role in roles:
            for perm in role.permissions:
                permissions.add(perm.name)
        
        return sorted(list(permissions))
