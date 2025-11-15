"""
RBAC - Role-Based Access Control
Permission management and authorization
"""

from typing import List, Set, Dict, Any, Callable
from enum import Enum
from pydantic import BaseModel
from fastapi import HTTPException, status, Depends
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class Permission(str, Enum):
    """System permissions"""
    # Circuit permissions
    CIRCUIT_READ = "circuit:read"
    CIRCUIT_EXECUTE = "circuit:execute"
    CIRCUIT_CREATE = "circuit:create"
    CIRCUIT_UPDATE = "circuit:update"
    CIRCUIT_DELETE = "circuit:delete"

    # Intelligence permissions
    RAG_QUERY = "rag:query"
    ML_PREDICT = "ml:predict"
    ML_TRAIN = "ml:train"
    KG_QUERY = "kg:query"
    KG_WRITE = "kg:write"

    # Admin permissions
    USER_CREATE = "user:create"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    ROLE_MANAGE = "role:manage"

    # System permissions
    METRICS_READ = "metrics:read"
    LOGS_READ = "logs:read"
    CONFIG_READ = "config:read"
    CONFIG_WRITE = "config:write"


class Role(str, Enum):
    """System roles"""
    ADMIN = "admin"
    DEVELOPER = "developer"
    OPERATOR = "operator"
    ANALYST = "analyst"
    VIEWER = "viewer"
    USER = "user"


# ============================================================================
# ROLE DEFINITIONS
# ============================================================================

ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.ADMIN: {
        # All permissions
        Permission.CIRCUIT_READ,
        Permission.CIRCUIT_EXECUTE,
        Permission.CIRCUIT_CREATE,
        Permission.CIRCUIT_UPDATE,
        Permission.CIRCUIT_DELETE,
        Permission.RAG_QUERY,
        Permission.ML_PREDICT,
        Permission.ML_TRAIN,
        Permission.KG_QUERY,
        Permission.KG_WRITE,
        Permission.USER_CREATE,
        Permission.USER_UPDATE,
        Permission.USER_DELETE,
        Permission.ROLE_MANAGE,
        Permission.METRICS_READ,
        Permission.LOGS_READ,
        Permission.CONFIG_READ,
        Permission.CONFIG_WRITE,
    },

    Role.DEVELOPER: {
        # Full circuit and intelligence access, no user management
        Permission.CIRCUIT_READ,
        Permission.CIRCUIT_EXECUTE,
        Permission.CIRCUIT_CREATE,
        Permission.CIRCUIT_UPDATE,
        Permission.CIRCUIT_DELETE,
        Permission.RAG_QUERY,
        Permission.ML_PREDICT,
        Permission.ML_TRAIN,
        Permission.KG_QUERY,
        Permission.KG_WRITE,
        Permission.METRICS_READ,
        Permission.LOGS_READ,
        Permission.CONFIG_READ,
    },

    Role.OPERATOR: {
        # Execute and monitor, no create/delete
        Permission.CIRCUIT_READ,
        Permission.CIRCUIT_EXECUTE,
        Permission.RAG_QUERY,
        Permission.ML_PREDICT,
        Permission.KG_QUERY,
        Permission.METRICS_READ,
        Permission.LOGS_READ,
        Permission.CONFIG_READ,
    },

    Role.ANALYST: {
        # Intelligence access, no circuit modification
        Permission.CIRCUIT_READ,
        Permission.RAG_QUERY,
        Permission.ML_PREDICT,
        Permission.KG_QUERY,
        Permission.METRICS_READ,
    },

    Role.VIEWER: {
        # Read-only access
        Permission.CIRCUIT_READ,
        Permission.METRICS_READ,
    },

    Role.USER: {
        # Basic access
        Permission.CIRCUIT_READ,
        Permission.CIRCUIT_EXECUTE,
        Permission.RAG_QUERY,
        Permission.ML_PREDICT,
        Permission.KG_QUERY,
    }
}


# ============================================================================
# RBAC MANAGER
# ============================================================================

class RBACManager:
    """
    Role-Based Access Control Manager
    """

    def __init__(self):
        self.role_permissions = ROLE_PERMISSIONS

        # Custom role definitions (for dynamic roles)
        self.custom_roles: Dict[str, Set[Permission]] = {}

        # User-specific permissions (overrides)
        self.user_permissions: Dict[str, Set[Permission]] = {}

    def get_role_permissions(self, role: Role) -> Set[Permission]:
        """Get permissions for a role"""
        return self.role_permissions.get(role, set())

    def get_user_permissions(
        self,
        user_roles: List[str],
        user_id: str = None
    ) -> Set[Permission]:
        """
        Get all permissions for a user based on their roles

        Combines permissions from all roles and user-specific overrides
        """
        permissions = set()

        # Add permissions from all roles
        for role_str in user_roles:
            try:
                role = Role(role_str)
                permissions.update(self.get_role_permissions(role))
            except ValueError:
                # Check custom roles
                if role_str in self.custom_roles:
                    permissions.update(self.custom_roles[role_str])
                else:
                    logger.warning(f"Unknown role: {role_str}")

        # Add user-specific permissions
        if user_id and user_id in self.user_permissions:
            permissions.update(self.user_permissions[user_id])

        return permissions

    def has_permission(
        self,
        user_roles: List[str],
        required_permission: Permission,
        user_id: str = None
    ) -> bool:
        """Check if user has required permission"""
        user_permissions = self.get_user_permissions(user_roles, user_id)
        return required_permission in user_permissions

    def has_any_permission(
        self,
        user_roles: List[str],
        required_permissions: List[Permission],
        user_id: str = None
    ) -> bool:
        """Check if user has any of the required permissions"""
        user_permissions = self.get_user_permissions(user_roles, user_id)
        return any(perm in user_permissions for perm in required_permissions)

    def has_all_permissions(
        self,
        user_roles: List[str],
        required_permissions: List[Permission],
        user_id: str = None
    ) -> bool:
        """Check if user has all required permissions"""
        user_permissions = self.get_user_permissions(user_roles, user_id)
        return all(perm in user_permissions for perm in required_permissions)

    def grant_user_permission(
        self,
        user_id: str,
        permission: Permission
    ):
        """Grant a specific permission to a user"""
        if user_id not in self.user_permissions:
            self.user_permissions[user_id] = set()

        self.user_permissions[user_id].add(permission)
        logger.info(f"Granted {permission.value} to user {user_id}")

    def revoke_user_permission(
        self,
        user_id: str,
        permission: Permission
    ):
        """Revoke a specific permission from a user"""
        if user_id in self.user_permissions:
            self.user_permissions[user_id].discard(permission)
            logger.info(f"Revoked {permission.value} from user {user_id}")

    def create_custom_role(
        self,
        role_name: str,
        permissions: Set[Permission]
    ):
        """Create a custom role with specific permissions"""
        self.custom_roles[role_name] = permissions
        logger.info(f"Created custom role: {role_name} with {len(permissions)} permissions")

    def get_role_hierarchy(self) -> Dict[str, int]:
        """Get role hierarchy (for precedence)"""
        return {
            Role.ADMIN: 100,
            Role.DEVELOPER: 80,
            Role.OPERATOR: 60,
            Role.ANALYST: 50,
            Role.USER: 30,
            Role.VIEWER: 10,
        }

    def get_highest_role(self, user_roles: List[str]) -> Optional[Role]:
        """Get the highest precedence role for a user"""
        hierarchy = self.get_role_hierarchy()
        highest_role = None
        highest_level = -1

        for role_str in user_roles:
            try:
                role = Role(role_str)
                level = hierarchy.get(role, 0)
                if level > highest_level:
                    highest_level = level
                    highest_role = role
            except ValueError:
                continue

        return highest_role


# ============================================================================
# GLOBAL RBAC MANAGER
# ============================================================================

_rbac_manager = None


def get_rbac_manager() -> RBACManager:
    """Get global RBAC manager instance"""
    global _rbac_manager
    if _rbac_manager is None:
        _rbac_manager = RBACManager()
    return _rbac_manager


# ============================================================================
# FASTAPI DEPENDENCIES
# ============================================================================

def require_permission(required_permission: Permission):
    """
    FastAPI dependency to require specific permission

    Usage:
        @app.post("/circuits", dependencies=[Depends(require_permission(Permission.CIRCUIT_CREATE))])
        async def create_circuit(user: User = Depends(get_current_user)):
            ...
    """
    def permission_checker(user: "User" = Depends("get_current_user")):
        from .auth import get_current_user

        rbac = get_rbac_manager()

        if not rbac.has_permission(user.roles, required_permission, user.user_id):
            logger.warning(
                f"Permission denied: {user.email} attempted {required_permission.value}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {required_permission.value} required"
            )

        return user

    return permission_checker


def require_any_permission(required_permissions: List[Permission]):
    """
    FastAPI dependency to require any of the specified permissions

    Usage:
        @app.get("/data")
        async def get_data(
            user: User = Depends(require_any_permission([Permission.CIRCUIT_READ, Permission.METRICS_READ]))
        ):
            ...
    """
    def permission_checker(user: "User" = Depends("get_current_user")):
        from .auth import get_current_user

        rbac = get_rbac_manager()

        if not rbac.has_any_permission(user.roles, required_permissions, user.user_id):
            logger.warning(
                f"Permission denied: {user.email} needs one of {[p.value for p in required_permissions]}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: requires one of {[p.value for p in required_permissions]}"
            )

        return user

    return permission_checker


def require_role(required_role: Role):
    """
    FastAPI dependency to require specific role

    Usage:
        @app.post("/admin/users", dependencies=[Depends(require_role(Role.ADMIN))])
        async def create_user():
            ...
    """
    def role_checker(user: "User" = Depends("get_current_user")):
        from .auth import get_current_user

        if required_role.value not in user.roles:
            logger.warning(
                f"Role denied: {user.email} attempted access requiring {required_role.value}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {required_role.value} required"
            )

        return user

    return role_checker


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def has_permission(user_roles: List[str], permission: Permission) -> bool:
    """Check if user roles have permission"""
    rbac = get_rbac_manager()
    return rbac.has_permission(user_roles, permission)


def get_user_permissions(user_roles: List[str]) -> Set[Permission]:
    """Get all permissions for user roles"""
    rbac = get_rbac_manager()
    return rbac.get_user_permissions(user_roles)


def check_permission_decorator(required_permission: Permission):
    """
    Decorator to check permission (for non-FastAPI functions)

    Usage:
        @check_permission_decorator(Permission.CIRCUIT_EXECUTE)
        def execute_circuit(user_roles: List[str], ...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, user_roles: List[str] = None, **kwargs):
            if user_roles is None:
                raise ValueError("user_roles required for permission check")

            rbac = get_rbac_manager()
            if not rbac.has_permission(user_roles, required_permission):
                raise PermissionError(f"Permission {required_permission.value} required")

            return func(*args, user_roles=user_roles, **kwargs)

        return wrapper
    return decorator
