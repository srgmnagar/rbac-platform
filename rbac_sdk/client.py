import requests
from rbac_sdk.exceptions import RBACAuthError, RBACConnectionError, RBACNotFoundError

class RBACClient:
    def __init__(self, base_url="http://localhost:8000", api_key="dev-key-12345"):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"X-API-Key": api_key}
        self._cache = {}

    def get_permissions(self, user_id):
        if user_id in self._cache:
            return self._cache[user_id]
        try:
            response = requests.get(
                f"{self.base_url}/query/user-permissions",
                headers=self.headers,
                params={"user_id": user_id}
            )
            if response.status_code == 401:
                raise RBACAuthError("Invalid API key")
            if response.status_code == 404:
                raise RBACNotFoundError(f"User {user_id} not found")
            response.raise_for_status()
            data = response.json()
            permissions = data.get("data", [])
            self._cache[user_id] = permissions
            return permissions
        except requests.exceptions.ConnectionError:
            raise RBACConnectionError("Cannot reach RBAC backend at " + self.base_url)

    def has_permission(self, user_id, permission):
        return permission in self.get_permissions(user_id)
