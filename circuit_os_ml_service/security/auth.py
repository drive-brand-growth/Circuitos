"""
JWT Authentication
Token generation, verification, and user management
"""

from typing import Optional, Dict, Any, Callable
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
import os

logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "circuit-os-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token
security = HTTPBearer()


# ============================================================================
# MODELS
# ============================================================================

class User(BaseModel):
    """User model"""
    user_id: str
    email: EmailStr
    username: str
    roles: list[str] = []
    is_active: bool = True
    metadata: Dict[str, Any] = {}


class TokenPayload(BaseModel):
    """JWT token payload"""
    sub: str  # user_id
    email: str
    username: str
    roles: list[str]
    exp: datetime
    iat: datetime


class LoginRequest(BaseModel):
    """Login request"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User


# ============================================================================
# JWT AUTHENTICATOR
# ============================================================================

class JWTAuthenticator:
    """
    JWT-based authentication system
    """

    def __init__(
        self,
        secret_key: str = SECRET_KEY,
        algorithm: str = ALGORITHM,
        token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expire_minutes = token_expire_minutes

        # In-memory user store (in production, use database)
        self.users: Dict[str, Dict[str, Any]] = {}

        # Initialize with default admin user
        self._create_default_users()

    def _create_default_users(self):
        """Create default users for demo"""
        self.register_user(
            email="admin@circuitos.com",
            username="admin",
            password="admin123",
            roles=["admin", "user"]
        )

        self.register_user(
            email="developer@circuitos.com",
            username="developer",
            password="dev123",
            roles=["developer", "user"]
        )

        self.register_user(
            email="viewer@circuitos.com",
            username="viewer",
            password="view123",
            roles=["viewer"]
        )

        logger.info("Created default users: admin, developer, viewer")

    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against hash"""
        return pwd_context.verify(plain_password, hashed_password)

    def register_user(
        self,
        email: str,
        username: str,
        password: str,
        roles: list[str] = None
    ) -> User:
        """Register a new user"""
        if email in self.users:
            raise ValueError(f"User with email {email} already exists")

        user_id = f"user_{len(self.users) + 1}"

        self.users[email] = {
            "user_id": user_id,
            "email": email,
            "username": username,
            "password_hash": self.hash_password(password),
            "roles": roles or ["user"],
            "is_active": True,
            "created_at": datetime.now().isoformat(),
            "metadata": {}
        }

        logger.info(f"Registered user: {username} ({email})")

        return User(
            user_id=user_id,
            email=email,
            username=username,
            roles=roles or ["user"]
        )

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user_data = self.users.get(email)

        if not user_data:
            logger.warning(f"Authentication failed: user not found ({email})")
            return None

        if not user_data.get("is_active"):
            logger.warning(f"Authentication failed: user inactive ({email})")
            return None

        if not self.verify_password(password, user_data["password_hash"]):
            logger.warning(f"Authentication failed: invalid password ({email})")
            return None

        logger.info(f"User authenticated: {email}")

        return User(
            user_id=user_data["user_id"],
            email=user_data["email"],
            username=user_data["username"],
            roles=user_data["roles"],
            is_active=user_data["is_active"],
            metadata=user_data.get("metadata", {})
        )

    def create_access_token(
        self,
        user: User,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.token_expire_minutes)

        to_encode = {
            "sub": user.user_id,
            "email": user.email,
            "username": user.username,
            "roles": user.roles,
            "exp": expire,
            "iat": datetime.utcnow()
        }

        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )

        logger.info(f"Created access token for user: {user.email}")

        return encoded_jwt

    def verify_token(self, token: str) -> Optional[TokenPayload]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            # Convert exp and iat to datetime
            payload["exp"] = datetime.fromtimestamp(payload["exp"])
            payload["iat"] = datetime.fromtimestamp(payload["iat"])

            token_data = TokenPayload(**payload)

            logger.debug(f"Token verified for user: {token_data.email}")

            return token_data

        except JWTError as e:
            logger.warning(f"Token verification failed: {e}")
            return None

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by user_id"""
        for user_data in self.users.values():
            if user_data["user_id"] == user_id:
                return User(
                    user_id=user_data["user_id"],
                    email=user_data["email"],
                    username=user_data["username"],
                    roles=user_data["roles"],
                    is_active=user_data["is_active"],
                    metadata=user_data.get("metadata", {})
                )
        return None

    async def login(self, email: str, password: str) -> TokenResponse:
        """Login and return token"""
        user = self.authenticate_user(email, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self.create_access_token(user)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=self.token_expire_minutes * 60,
            user=user
        )


# ============================================================================
# GLOBAL AUTHENTICATOR INSTANCE
# ============================================================================

_authenticator = None


def get_authenticator() -> JWTAuthenticator:
    """Get global authenticator instance"""
    global _authenticator
    if _authenticator is None:
        _authenticator = JWTAuthenticator()
    return _authenticator


# ============================================================================
# FASTAPI DEPENDENCIES
# ============================================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    FastAPI dependency to get current authenticated user

    Usage:
        @app.get("/protected")
        async def protected_route(user: User = Depends(get_current_user)):
            return {"user": user.email}
    """
    authenticator = get_authenticator()

    token = credentials.credentials
    token_payload = authenticator.verify_token(token)

    if token_payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = authenticator.get_user_by_id(token_payload.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_access_token(
    user: User,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Convenience function to create access token"""
    authenticator = get_authenticator()
    return authenticator.create_access_token(user, expires_delta)


def verify_access_token(token: str) -> Optional[TokenPayload]:
    """Convenience function to verify access token"""
    authenticator = get_authenticator()
    return authenticator.verify_token(token)


def require_auth(func: Callable) -> Callable:
    """
    Decorator to require authentication

    Usage:
        @require_auth
        async def my_function(user: User):
            # user is automatically injected
            pass
    """
    async def wrapper(*args, user: User = Depends(get_current_user), **kwargs):
        return await func(*args, user=user, **kwargs)
    return wrapper
