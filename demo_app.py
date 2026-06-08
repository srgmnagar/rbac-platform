from fastapi import FastAPI
from rbac_sdk import RBACClient

app = FastAPI()
client = RBACClient()

@app.get("/dashboard/{user_id}")
def dashboard(user_id: str):
    permissions = client.get_permissions(user_id)
    return {
        "user_id": user_id,
        "permissions": permissions,
        "features": {
            "can_view_reports": client.has_permission(user_id, "view_reports"),
            "can_approve": client.has_permission(user_id, "approve_requests"),
            "can_delete": client.has_permission(user_id, "delete_user"),
            "can_edit_roles": client.has_permission(user_id, "edit_role")
        }
    }

@app.get("/check/{user_id}/{permission}")
def check(user_id: str, permission: str):
    result = client.has_permission(user_id, permission)
    return {"user_id": user_id, "permission": permission, "granted": result}
