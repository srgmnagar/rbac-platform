from backend.database import Base, engine, SessionLocal
from backend.models import Role, Permission, user_roles, role_permissions

def init_db():
    """Create all tables and seed initial data"""
    
    # Create all tables
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Create Roles
        print("Creating roles...")
        admin_role = Role(name="Admin", description="Full system access")
        manager_role = Role(name="Manager", description="Can view reports and approve requests")
        employee_role = Role(name="Employee", description="Can view own reports")
        
        db.add(admin_role)
        db.add(manager_role)
        db.add(employee_role)
        db.commit()
        print("Roles created")
        
        # Create Permissions
        print("Creating permissions...")
        view_reports_perm = Permission(name="view_reports", description="Can view reports")
        approve_requests_perm = Permission(name="approve_requests", description="Can approve requests")
        delete_user_perm = Permission(name="delete_user", description="Can delete users")
        edit_role_perm = Permission(name="edit_role", description="Can edit roles")
        
        db.add(view_reports_perm)
        db.add(approve_requests_perm)
        db.add(delete_user_perm)
        db.add(edit_role_perm)
        db.commit()
        print("Permissions created")
        
        # Assign permissions to roles
        print("Assigning permissions to roles...")
        
        # Admin gets all permissions
        admin_role.permissions.append(view_reports_perm)
        admin_role.permissions.append(approve_requests_perm)
        admin_role.permissions.append(delete_user_perm)
        admin_role.permissions.append(edit_role_perm)
        
        # Manager gets view and approve
        manager_role.permissions.append(view_reports_perm)
        manager_role.permissions.append(approve_requests_perm)
        
        # Employee gets view only
        employee_role.permissions.append(view_reports_perm)
        
        db.commit()
        print("Permissions assigned to roles")
        
        # Assign users to roles
        print("Assigning users to roles...")
        
        stmt = user_roles.insert().values(user_id="alice@org.com", role_id=admin_role.id)
        db.execute(stmt)
        
        stmt = user_roles.insert().values(user_id="bob@org.com", role_id=manager_role.id)
        db.execute(stmt)
        
        stmt = user_roles.insert().values(user_id="charlie@org.com", role_id=employee_role.id)
        db.execute(stmt)
        
        db.commit()
        print("Users assigned to roles")
        
        print("\n" + "="*50)
        print("Database initialization complete!")
        print("="*50)
        print("\nSeed data:")
        print("  Users:")
        print("    - alice@org.com (Admin)")
        print("    - bob@org.com (Manager)")
        print("    - charlie@org.com (Employee)")
        print("\n  Roles:")
        print("    - Admin: all permissions")
        print("    - Manager: view_reports, approve_requests")
        print("    - Employee: view_reports")
        print("\n  Permissions:")
        print("    - view_reports")
        print("    - approve_requests")
        print("    - delete_user")
        print("    - edit_role")
        print("="*50)
        
    except Exception as e:
        db.rollback()
        print(f"Error: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
