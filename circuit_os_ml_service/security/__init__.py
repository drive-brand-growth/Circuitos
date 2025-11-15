"""
Security Module - JWT, RBAC, Rate Limiting, Validation
Production-grade security for Circuit OS
"""

from .auth import (
    JWTAuthenticator,
    create_access_token,
    verify_access_token,
    get_current_user,
    require_auth
)

from .rbac import (
    Role,
    Permission,
    RBACManager,
    require_permission,
    has_permission
)

from .rate_limit import (
    RateLimiter,
    TokenBucket,
    rate_limit,
    get_rate_limiter
)

from .validation import (
    CircuitRequestValidator,
    validate_circuit_data,
    sanitize_input,
    ValidationError
)

__all__ = [
    # Authentication
    "JWTAuthenticator",
    "create_access_token",
    "verify_access_token",
    "get_current_user",
    "require_auth",

    # Authorization
    "Role",
    "Permission",
    "RBACManager",
    "require_permission",
    "has_permission",

    # Rate Limiting
    "RateLimiter",
    "TokenBucket",
    "rate_limit",
    "get_rate_limiter",

    # Validation
    "CircuitRequestValidator",
    "validate_circuit_data",
    "sanitize_input",
    "ValidationError",
]
