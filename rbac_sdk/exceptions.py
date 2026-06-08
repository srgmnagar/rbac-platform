class RBACError(Exception):
    """Base exception for all RBAC SDK errors"""
    pass


class RBACAuthError(RBACError):
    """Raised when the API key is invalid or missing (HTTP 401)"""
    def __init__(self, message: str = "Invalid or missing API key"):
        self.message = message
        super().__init__(self.message)


class RBACConnectionError(RBACError):
    """Raised when the RBAC backend is unreachable"""
    def __init__(self, message: str = "Cannot connect to RBAC backend"):
        self.message = message
        super().__init__(self.message)


class RBACNotFoundError(RBACError):
    """Raised when the requested user has no record in the RBAC system"""
    def __init__(self, user_id: str = ""):
        self.user_id = user_id
        self.message = f"User not found: {user_id}" if user_id else "User not found"
        super().__init__(self.message)
