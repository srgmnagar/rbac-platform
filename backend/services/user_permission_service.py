from sqlalchemy.orm import Session
from sqlalchemy import insert
from ..models import Role, Permission, user_roles, role_permissions
from .. import cache


class UserPermissionService:
    @staticmethod
    def assign_user_to_role(db: Session, user_id: str, role_id: int) -> dict:
        """Assign a user to a role"""
        stmt = insert(user_roles).values(user_id=user_id, role_id=role_id)
        db.execute(stmt)
        db.commit()
        # Invalidate all cached permissions — the affected user now has a new
        # role, so their permission list has changed.
        cache.invalidate_all_cache()
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
        # Invalidate all cached permissions — any user with this role now has
        # different permissions, and we'd need an extra query to find them all.
        cache.invalidate_all_cache()

    @staticmethod
    def get_user_permissions(db: Session, user_id: str) -> list:
        """Get all permissions for a user by traversing user->roles->permissions"""
        # --- Cache read-through ---
        cached = cache.get_cached_permissions(user_id)
        if cached is not None:
            return cached

        # Cache miss: query PostgreSQL.
        # Get all roles for this user
        roles = db.query(Role).join(user_roles).filter(user_roles.c.user_id == user_id).all()

        # Get all permissions from those roles
        permissions = set()
        for role in roles:
            for perm in role.permissions:
                permissions.add(perm.name)

        result = sorted(list(permissions))

        # Populate cache for subsequent calls.
        cache.set_cached_permissions(user_id, result)

        return result

