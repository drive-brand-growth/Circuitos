"""
Rate Limiting
Token bucket algorithm for API rate limiting
"""

from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
from fastapi import HTTPException, status, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import asyncio
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# TOKEN BUCKET
# ============================================================================

class TokenBucket:
    """
    Token bucket algorithm for rate limiting

    Allows bursts up to capacity, refills at a constant rate
    """

    def __init__(
        self,
        capacity: int,
        refill_rate: float,  # tokens per second
        initial_tokens: Optional[int] = None
    ):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = initial_tokens if initial_tokens is not None else capacity
        self.last_refill = time.time()

    def _refill(self):
        """Refill tokens based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_refill

        # Calculate tokens to add
        tokens_to_add = elapsed * self.refill_rate

        # Update token count
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens

        Returns True if successful, False if insufficient tokens
        """
        self._refill()

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        else:
            return False

    def get_available_tokens(self) -> int:
        """Get current available tokens"""
        self._refill()
        return int(self.tokens)

    def get_wait_time(self, tokens: int = 1) -> float:
        """Get wait time in seconds until tokens are available"""
        self._refill()

        if self.tokens >= tokens:
            return 0.0

        tokens_needed = tokens - self.tokens
        wait_time = tokens_needed / self.refill_rate

        return wait_time


# ============================================================================
# RATE LIMITER
# ============================================================================

class RateLimiter:
    """
    Rate limiter with multiple bucket strategies
    """

    def __init__(self):
        # Per-user buckets
        self.user_buckets: Dict[str, TokenBucket] = {}

        # Per-IP buckets
        self.ip_buckets: Dict[str, TokenBucket] = {}

        # Per-endpoint buckets
        self.endpoint_buckets: Dict[str, TokenBucket] = {}

        # Global bucket
        self.global_bucket: Optional[TokenBucket] = None

        # Rate limit configurations
        self.user_limits = {
            "admin": (1000, 10.0),      # 1000 tokens, refill at 10/sec
            "developer": (500, 5.0),     # 500 tokens, refill at 5/sec
            "user": (100, 1.0),          # 100 tokens, refill at 1/sec
            "viewer": (50, 0.5),         # 50 tokens, refill at 0.5/sec
        }

        self.ip_limit = (200, 2.0)       # Per-IP limit
        self.global_limit = (10000, 100.0)  # Global system limit

        # Cleanup task
        self._cleanup_task = None

    def _get_user_bucket(self, user_id: str, role: str) -> TokenBucket:
        """Get or create bucket for user"""
        if user_id not in self.user_buckets:
            capacity, refill_rate = self.user_limits.get(
                role,
                self.user_limits["user"]  # Default
            )
            self.user_buckets[user_id] = TokenBucket(capacity, refill_rate)

        return self.user_buckets[user_id]

    def _get_ip_bucket(self, ip: str) -> TokenBucket:
        """Get or create bucket for IP"""
        if ip not in self.ip_buckets:
            capacity, refill_rate = self.ip_limit
            self.ip_buckets[ip] = TokenBucket(capacity, refill_rate)

        return self.ip_buckets[ip]

    def _get_global_bucket(self) -> TokenBucket:
        """Get global bucket"""
        if self.global_bucket is None:
            capacity, refill_rate = self.global_limit
            self.global_bucket = TokenBucket(capacity, refill_rate)

        return self.global_bucket

    def check_rate_limit(
        self,
        user_id: Optional[str] = None,
        user_role: Optional[str] = "user",
        ip: Optional[str] = None,
        tokens: int = 1
    ) -> Tuple[bool, Optional[float]]:
        """
        Check if request should be allowed

        Returns (allowed, wait_time)
        """
        # Check global limit
        global_bucket = self._get_global_bucket()
        if not global_bucket.consume(tokens):
            wait_time = global_bucket.get_wait_time(tokens)
            logger.warning(f"Global rate limit exceeded, wait {wait_time:.2f}s")
            return False, wait_time

        # Check user limit
        if user_id:
            user_bucket = self._get_user_bucket(user_id, user_role)
            if not user_bucket.consume(tokens):
                wait_time = user_bucket.get_wait_time(tokens)
                logger.warning(f"User rate limit exceeded for {user_id}, wait {wait_time:.2f}s")
                return False, wait_time

        # Check IP limit
        if ip:
            ip_bucket = self._get_ip_bucket(ip)
            if not ip_bucket.consume(tokens):
                wait_time = ip_bucket.get_wait_time(tokens)
                logger.warning(f"IP rate limit exceeded for {ip}, wait {wait_time:.2f}s")
                return False, wait_time

        return True, None

    async def cleanup_old_buckets(self, max_age_minutes: int = 60):
        """Clean up buckets that haven't been used recently"""
        # This would track last_used timestamp in production
        # For now, just limit bucket count

        max_buckets = 10000

        if len(self.user_buckets) > max_buckets:
            # Remove random buckets (in production, remove oldest)
            to_remove = len(self.user_buckets) - max_buckets
            for key in list(self.user_buckets.keys())[:to_remove]:
                del self.user_buckets[key]
            logger.info(f"Cleaned up {to_remove} user buckets")

        if len(self.ip_buckets) > max_buckets:
            to_remove = len(self.ip_buckets) - max_buckets
            for key in list(self.ip_buckets.keys())[:to_remove]:
                del self.ip_buckets[key]
            logger.info(f"Cleaned up {to_remove} IP buckets")

    def start_cleanup_task(self):
        """Start background cleanup task"""
        async def cleanup_loop():
            while True:
                await asyncio.sleep(300)  # Every 5 minutes
                await self.cleanup_old_buckets()

        self._cleanup_task = asyncio.create_task(cleanup_loop())

    def get_statistics(self) -> Dict:
        """Get rate limiter statistics"""
        return {
            "user_buckets": len(self.user_buckets),
            "ip_buckets": len(self.ip_buckets),
            "global_tokens_available": self._get_global_bucket().get_available_tokens(),
        }


# ============================================================================
# GLOBAL RATE LIMITER
# ============================================================================

_rate_limiter = None


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter


# ============================================================================
# FASTAPI MIDDLEWARE
# ============================================================================

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for rate limiting

    Usage:
        app.add_middleware(RateLimitMiddleware)
    """

    def __init__(self, app, rate_limiter: Optional[RateLimiter] = None):
        super().__init__(app)
        self.rate_limiter = rate_limiter or get_rate_limiter()

    async def dispatch(self, request: Request, call_next):
        # Extract user info from request (if authenticated)
        user_id = None
        user_role = "user"

        # Try to get user from auth header
        auth_header = request.headers.get("authorization")
        if auth_header:
            try:
                from .auth import verify_access_token

                token = auth_header.replace("Bearer ", "")
                token_payload = verify_access_token(token)

                if token_payload:
                    user_id = token_payload.sub
                    # Get highest role
                    from .rbac import get_rbac_manager
                    rbac = get_rbac_manager()
                    highest_role = rbac.get_highest_role(token_payload.roles)
                    user_role = highest_role.value if highest_role else "user"

            except Exception:
                pass  # Continue without user context

        # Get client IP
        client_ip = request.client.host if request.client else None

        # Check rate limit
        allowed, wait_time = self.rate_limiter.check_rate_limit(
            user_id=user_id,
            user_role=user_role,
            ip=client_ip,
            tokens=1
        )

        if not allowed:
            return Response(
                content=f"Rate limit exceeded. Try again in {wait_time:.2f} seconds.",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                headers={
                    "Retry-After": str(int(wait_time) + 1),
                    "X-RateLimit-Remaining": "0"
                }
            )

        # Add rate limit headers
        response = await call_next(request)

        # Add remaining tokens info
        if user_id:
            bucket = self.rate_limiter._get_user_bucket(user_id, user_role)
            response.headers["X-RateLimit-Remaining"] = str(bucket.get_available_tokens())

        return response


# ============================================================================
# FASTAPI DEPENDENCY
# ============================================================================

async def rate_limit(
    request: Request,
    tokens: int = 1,
    user_id: Optional[str] = None,
    user_role: str = "user"
):
    """
    FastAPI dependency for rate limiting

    Usage:
        @app.get("/resource")
        async def get_resource(
            _: None = Depends(rate_limit)
        ):
            ...

        Or with custom tokens:
        @app.post("/expensive")
        async def expensive_operation(
            _: None = Depends(lambda: rate_limit(tokens=10))
        ):
            ...
    """
    rate_limiter = get_rate_limiter()

    # Get client IP
    client_ip = request.client.host if request.client else None

    # If no user_id provided, try to extract from request
    if not user_id:
        auth_header = request.headers.get("authorization")
        if auth_header:
            try:
                from .auth import verify_access_token

                token = auth_header.replace("Bearer ", "")
                token_payload = verify_access_token(token)

                if token_payload:
                    user_id = token_payload.sub

                    # Get highest role
                    from .rbac import get_rbac_manager
                    rbac = get_rbac_manager()
                    highest_role = rbac.get_highest_role(token_payload.roles)
                    user_role = highest_role.value if highest_role else "user"

            except Exception:
                pass

    # Check rate limit
    allowed, wait_time = rate_limiter.check_rate_limit(
        user_id=user_id,
        user_role=user_role,
        ip=client_ip,
        tokens=tokens
    )

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {wait_time:.2f} seconds.",
            headers={
                "Retry-After": str(int(wait_time) + 1)
            }
        )
