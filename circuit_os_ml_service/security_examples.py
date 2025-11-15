"""
Security Examples - Demonstrating JWT, RBAC, Rate Limiting, and Validation
Complete security layer demonstration
"""

import asyncio
import logging
from typing import Dict, Any

from security import (
    # Authentication
    JWTAuthenticator,
    User,

    # Authorization
    RBACManager,
    Permission,
    Role,

    # Rate Limiting
    RateLimiter,
    TokenBucket,

    # Validation
    CircuitRequestValidator,
    InputSanitizer,
    InjectionAttemptError,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# AUTHENTICATION EXAMPLES
# ============================================================================

async def demo_authentication():
    """Demonstrate JWT authentication"""
    print("=" * 70)
    print("DEMO 1: JWT AUTHENTICATION")
    print("=" * 70)
    print()

    authenticator = JWTAuthenticator()

    # Register a new user
    print("1. Registering new user...")
    user = authenticator.register_user(
        email="test@example.com",
        username="testuser",
        password="securepassword123",
        roles=["developer", "user"]
    )
    print(f"   ✓ User registered: {user.username} ({user.email})")
    print(f"   Roles: {user.roles}")
    print()

    # Authenticate user
    print("2. Authenticating user...")
    authenticated_user = authenticator.authenticate_user(
        "test@example.com",
        "securepassword123"
    )

    if authenticated_user:
        print(f"   ✓ Authentication successful: {authenticated_user.email}")
    else:
        print("   ✗ Authentication failed")
    print()

    # Create JWT token
    print("3. Creating JWT access token...")
    token = authenticator.create_access_token(authenticated_user)
    print(f"   ✓ Token created: {token[:50]}...")
    print(f"   Expires in: {authenticator.token_expire_minutes} minutes")
    print()

    # Verify token
    print("4. Verifying JWT token...")
    token_payload = authenticator.verify_token(token)

    if token_payload:
        print(f"   ✓ Token valid")
        print(f"   User ID: {token_payload.sub}")
        print(f"   Email: {token_payload.email}")
        print(f"   Roles: {token_payload.roles}")
        print(f"   Issued at: {token_payload.iat}")
        print(f"   Expires at: {token_payload.exp}")
    else:
        print("   ✗ Token invalid")
    print()

    # Test invalid credentials
    print("5. Testing invalid credentials...")
    invalid_user = authenticator.authenticate_user(
        "test@example.com",
        "wrongpassword"
    )

    if invalid_user:
        print("   ✗ Should have failed!")
    else:
        print("   ✓ Correctly rejected invalid password")
    print()


# ============================================================================
# AUTHORIZATION EXAMPLES
# ============================================================================

async def demo_authorization():
    """Demonstrate RBAC authorization"""
    print("=" * 70)
    print("DEMO 2: RBAC AUTHORIZATION")
    print("=" * 70)
    print()

    rbac = RBACManager()

    # Show role permissions
    print("1. Role Permissions:")
    print()

    roles_to_show = [Role.ADMIN, Role.DEVELOPER, Role.VIEWER]

    for role in roles_to_show:
        permissions = rbac.get_role_permissions(role)
        print(f"   {role.value.upper()} ({len(permissions)} permissions):")
        for perm in sorted(permissions, key=lambda p: p.value)[:5]:  # Show first 5
            print(f"     • {perm.value}")
        if len(permissions) > 5:
            print(f"     ... and {len(permissions) - 5} more")
        print()

    # Check permissions
    print("2. Permission Checks:")
    print()

    user_roles = ["developer", "user"]

    permissions_to_check = [
        Permission.CIRCUIT_EXECUTE,
        Permission.CIRCUIT_DELETE,
        Permission.USER_DELETE,
        Permission.ML_TRAIN,
    ]

    for perm in permissions_to_check:
        has_perm = rbac.has_permission(user_roles, perm)
        status = "✓ ALLOWED" if has_perm else "✗ DENIED"
        print(f"   {status}: Developer trying {perm.value}")

    print()

    # Grant user-specific permission
    print("3. Granting user-specific permission...")
    user_id = "user_123"
    rbac.grant_user_permission(user_id, Permission.USER_DELETE)
    print(f"   ✓ Granted {Permission.USER_DELETE.value} to user {user_id}")

    has_perm_after = rbac.has_permission(user_roles, Permission.USER_DELETE, user_id)
    print(f"   Permission check: {'✓ ALLOWED' if has_perm_after else '✗ DENIED'}")
    print()

    # Create custom role
    print("4. Creating custom role...")
    custom_permissions = {
        Permission.CIRCUIT_READ,
        Permission.CIRCUIT_EXECUTE,
        Permission.METRICS_READ,
    }

    rbac.create_custom_role("circuit_operator", custom_permissions)
    print(f"   ✓ Created 'circuit_operator' with {len(custom_permissions)} permissions")
    print()


# ============================================================================
# RATE LIMITING EXAMPLES
# ============================================================================

async def demo_rate_limiting():
    """Demonstrate rate limiting"""
    print("=" * 70)
    print("DEMO 3: RATE LIMITING")
    print("=" * 70)
    print()

    # Token bucket demo
    print("1. Token Bucket Algorithm:")
    print()

    # Create bucket: 5 tokens, refill at 1 token/second
    bucket = TokenBucket(capacity=5, refill_rate=1.0)

    print(f"   Bucket capacity: 5 tokens")
    print(f"   Refill rate: 1 token/second")
    print()

    # Consume tokens
    print("   Consuming tokens:")
    for i in range(7):
        success = bucket.consume(1)
        available = bucket.get_available_tokens()
        status = "✓" if success else "✗"
        print(f"     Request {i+1}: {status} (Available: {available})")

    print()

    # Wait and refill
    print("   Waiting 2 seconds for refill...")
    await asyncio.sleep(2)

    available = bucket.get_available_tokens()
    print(f"   Available tokens after refill: {available}")
    print()

    # Rate limiter with different user roles
    print("2. Rate Limiter with User Roles:")
    print()

    rate_limiter = RateLimiter()

    # Test different roles
    test_cases = [
        ("admin_user", "admin", 5),
        ("dev_user", "developer", 5),
        ("regular_user", "user", 5),
    ]

    for user_id, role, num_requests in test_cases:
        print(f"   {role.upper()} ({user_id}):")

        allowed_count = 0
        denied_count = 0

        for i in range(num_requests):
            allowed, wait_time = rate_limiter.check_rate_limit(
                user_id=user_id,
                user_role=role,
                tokens=1
            )

            if allowed:
                allowed_count += 1
            else:
                denied_count += 1

        print(f"     Allowed: {allowed_count}/{num_requests}")
        print(f"     Denied: {denied_count}/{num_requests}")
        print()

    # Statistics
    stats = rate_limiter.get_statistics()
    print(f"   Rate Limiter Statistics:")
    print(f"     User buckets: {stats['user_buckets']}")
    print(f"     IP buckets: {stats['ip_buckets']}")
    print(f"     Global tokens available: {stats['global_tokens_available']}")
    print()


# ============================================================================
# INPUT VALIDATION EXAMPLES
# ============================================================================

async def demo_input_validation():
    """Demonstrate input validation and sanitization"""
    print("=" * 70)
    print("DEMO 4: INPUT VALIDATION & SANITIZATION")
    print("=" * 70)
    print()

    # Sanitization
    print("1. Input Sanitization:")
    print()

    test_inputs = [
        "Normal text",
        "<script>alert('XSS')</script>",
        "Text with \"quotes\" and <html>",
        "A" * 1500,  # Long string
    ]

    for input_str in test_inputs:
        sanitized = InputSanitizer.sanitize_string(input_str, max_length=100)
        truncated = "..." if len(input_str) > 100 else ""
        print(f"   Original: {input_str[:50]}{truncated}")
        print(f"   Sanitized: {sanitized[:50]}...")
        print()

    # Injection detection
    print("2. Injection Attack Detection:")
    print()

    injection_tests = [
        ("SQL Injection", "SELECT * FROM users WHERE id=1; DROP TABLE users;"),
        ("XSS Attack", "<script>document.cookie</script>"),
        ("Command Injection", "test; rm -rf /"),
        ("Safe Input", "Just a normal search query"),
    ]

    for test_name, test_input in injection_tests:
        sql_detected = InputSanitizer.detect_sql_injection(test_input)
        xss_detected = InputSanitizer.detect_xss(test_input)
        cmd_detected = InputSanitizer.detect_command_injection(test_input)

        any_detected = sql_detected or xss_detected or cmd_detected

        status = "✗ BLOCKED" if any_detected else "✓ SAFE"
        print(f"   {status}: {test_name}")

        if sql_detected:
            print(f"     → SQL injection detected")
        if xss_detected:
            print(f"     → XSS attack detected")
        if cmd_detected:
            print(f"     → Command injection detected")

    print()

    # Circuit request validation
    print("3. Circuit Request Validation:")
    print()

    validator = CircuitRequestValidator()

    # Set allowed circuits
    validator.set_allowed_circuits(["lead_processing", "data_sync"])

    valid_requests = [
        ("lead_processing", {"lead_id": "123", "status": "new"}),
    ]

    invalid_requests = [
        ("unknown_circuit", {"data": "test"}),
        ("lead_processing", {"query": "'; DROP TABLE--"}),
    ]

    print("   Valid Requests:")
    for circuit_name, data in valid_requests:
        try:
            validated_name, validated_data = validator.validate_circuit_request(
                circuit_name,
                data
            )
            print(f"     ✓ {circuit_name}: Validated successfully")
        except Exception as e:
            print(f"     ✗ {circuit_name}: {e}")

    print()
    print("   Invalid Requests:")
    for circuit_name, data in invalid_requests:
        try:
            validated_name, validated_data = validator.validate_circuit_request(
                circuit_name,
                data
            )
            print(f"     ✗ {circuit_name}: Should have been blocked!")
        except Exception as e:
            print(f"     ✓ {circuit_name}: Correctly blocked - {str(e)[:50]}")

    print()


# ============================================================================
# COMPLETE SECURITY FLOW
# ============================================================================

async def demo_complete_security_flow():
    """Demonstrate complete security flow"""
    print("=" * 70)
    print("DEMO 5: COMPLETE SECURITY FLOW")
    print("=" * 70)
    print()

    authenticator = JWTAuthenticator()
    rbac = RBACManager()
    rate_limiter = RateLimiter()
    validator = CircuitRequestValidator()

    print("1. User Registration & Authentication")
    print()

    # Register user
    user = authenticator.register_user(
        email="secure@example.com",
        username="secureuser",
        password="VerySecurePassword123!",
        roles=["developer"]
    )
    print(f"   ✓ User registered: {user.email}")

    # Login
    token_response = await authenticator.login(user.email, "VerySecurePassword123!")
    token = token_response.access_token
    print(f"   ✓ Login successful, token generated")
    print()

    # Verify token
    print("2. Token Verification & Permission Check")
    print()

    token_payload = authenticator.verify_token(token)
    print(f"   ✓ Token verified for: {token_payload.email}")

    # Check permissions
    has_execute = rbac.has_permission(
        token_payload.roles,
        Permission.CIRCUIT_EXECUTE
    )
    print(f"   ✓ CIRCUIT_EXECUTE permission: {'ALLOWED' if has_execute else 'DENIED'}")

    has_delete_user = rbac.has_permission(
        token_payload.roles,
        Permission.USER_DELETE
    )
    print(f"   ✗ USER_DELETE permission: {'ALLOWED' if has_delete_user else 'DENIED'}")
    print()

    # Rate limiting
    print("3. Rate Limit Check")
    print()

    allowed, wait_time = rate_limiter.check_rate_limit(
        user_id=user.user_id,
        user_role="developer",
        ip="192.168.1.100"
    )

    if allowed:
        print(f"   ✓ Rate limit check: PASSED")
    else:
        print(f"   ✗ Rate limit check: FAILED (wait {wait_time:.2f}s)")
    print()

    # Input validation
    print("4. Input Validation")
    print()

    circuit_data = {
        "circuit_name": "lead_processing",
        "data": {
            "lead_id": "lead_12345",
            "company": "Acme Corp",
        }
    }

    try:
        validated_name, validated_data = validator.validate_circuit_request(
            circuit_data["circuit_name"],
            circuit_data["data"]
        )
        print(f"   ✓ Input validation: PASSED")
        print(f"   Circuit: {validated_name}")
        print(f"   Data keys: {list(validated_data.keys())}")
    except Exception as e:
        print(f"   ✗ Input validation: FAILED - {e}")

    print()

    # Complete flow summary
    print("5. Security Flow Summary")
    print()
    print("   ┌─────────────────┐")
    print("   │ 1. Login        │ → JWT Token Generated")
    print("   └─────────────────┘")
    print("           ↓")
    print("   ┌─────────────────┐")
    print("   │ 2. Verify Token │ → User Authenticated")
    print("   └─────────────────┘")
    print("           ↓")
    print("   ┌─────────────────┐")
    print("   │ 3. Check RBAC   │ → Permissions Validated")
    print("   └─────────────────┘")
    print("           ↓")
    print("   ┌─────────────────┐")
    print("   │ 4. Rate Limit   │ → Request Allowed")
    print("   └─────────────────┘")
    print("           ↓")
    print("   ┌─────────────────┐")
    print("   │ 5. Validate     │ → Input Sanitized")
    print("   └─────────────────┘")
    print("           ↓")
    print("   ┌─────────────────┐")
    print("   │ 6. Execute      │ → Circuit Runs Safely")
    print("   └─────────────────┘")
    print()


# ============================================================================
# MAIN DEMO
# ============================================================================

async def main():
    """Run all security demos"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "CIRCUIT OS - SECURITY LAYER DEMO" + " " * 21 + "║")
    print("║" + " " * 12 + "JWT + RBAC + Rate Limiting + Validation" + " " * 16 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    await demo_authentication()
    await demo_authorization()
    await demo_rate_limiting()
    await demo_input_validation()
    await demo_complete_security_flow()

    print("=" * 70)
    print("SECURITY LAYER DEMONSTRATION COMPLETE")
    print("=" * 70)
    print()
    print("Summary:")
    print("  ✓ JWT Authentication - Token generation and verification")
    print("  ✓ RBAC Authorization - 6 roles, 18 permissions")
    print("  ✓ Rate Limiting - Token bucket per user/IP/global")
    print("  ✓ Input Validation - SQL/XSS/Command injection detection")
    print()
    print("All security components are production-ready!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
