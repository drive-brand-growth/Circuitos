"""
Input Validation and Sanitization
Prevent injection attacks and validate data schemas
"""

from typing import Dict, Any, List, Optional, Set
from pydantic import BaseModel, validator, Field
from fastapi import HTTPException, status
import re
import html
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class ValidationError(Exception):
    """Custom validation error"""
    pass


class InjectionAttemptError(ValidationError):
    """Potential injection attack detected"""
    pass


# ============================================================================
# SANITIZATION UTILITIES
# ============================================================================

class InputSanitizer:
    """
    Input sanitization utilities
    """

    # Dangerous patterns
    SQL_INJECTION_PATTERNS = [
        r"(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\s",
        r";\s*(SELECT|INSERT|UPDATE|DELETE|DROP)",
        r"--",
        r"/\*.*\*/",
        r"(UNION|OR|AND)\s+\d+\s*=\s*\d+",
    ]

    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe",
        r"<object",
        r"<embed",
    ]

    COMMAND_INJECTION_PATTERNS = [
        r";\s*(rm|cat|ls|wget|curl|nc|bash|sh)\s",
        r"\|\s*(rm|cat|ls|wget|curl|nc|bash|sh)\s",
        r"`.*`",
        r"\$\(.*\)",
    ]

    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """
        Sanitize string input

        - Limit length
        - HTML escape
        - Remove null bytes
        """
        if not isinstance(value, str):
            return value

        # Remove null bytes
        value = value.replace("\x00", "")

        # Limit length
        if len(value) > max_length:
            logger.warning(f"String truncated from {len(value)} to {max_length}")
            value = value[:max_length]

        # HTML escape
        value = html.escape(value)

        return value

    @classmethod
    def detect_sql_injection(cls, value: str) -> bool:
        """Detect potential SQL injection"""
        if not isinstance(value, str):
            return False

        value_upper = value.upper()

        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, value_upper, re.IGNORECASE):
                logger.warning(f"SQL injection pattern detected: {pattern}")
                return True

        return False

    @classmethod
    def detect_xss(cls, value: str) -> bool:
        """Detect potential XSS attack"""
        if not isinstance(value, str):
            return False

        for pattern in cls.XSS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                logger.warning(f"XSS pattern detected: {pattern}")
                return True

        return False

    @classmethod
    def detect_command_injection(cls, value: str) -> bool:
        """Detect potential command injection"""
        if not isinstance(value, str):
            return False

        for pattern in cls.COMMAND_INJECTION_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                logger.warning(f"Command injection pattern detected: {pattern}")
                return True

        return False

    @classmethod
    def validate_safe_input(cls, value: str, field_name: str = "input") -> str:
        """
        Validate input is safe from injection attacks

        Raises InjectionAttemptError if dangerous patterns detected
        """
        if not isinstance(value, str):
            return value

        if cls.detect_sql_injection(value):
            raise InjectionAttemptError(f"SQL injection detected in {field_name}")

        if cls.detect_xss(value):
            raise InjectionAttemptError(f"XSS attack detected in {field_name}")

        if cls.detect_command_injection(value):
            raise InjectionAttemptError(f"Command injection detected in {field_name}")

        return value

    @staticmethod
    def sanitize_dict(data: Dict[str, Any], max_depth: int = 10) -> Dict[str, Any]:
        """
        Recursively sanitize dictionary

        - Sanitize string values
        - Limit nesting depth
        """
        if max_depth <= 0:
            logger.warning("Max depth reached during sanitization")
            return {}

        sanitized = {}

        for key, value in data.items():
            # Sanitize key
            if not isinstance(key, str):
                key = str(key)

            key = InputSanitizer.sanitize_string(key, max_length=100)

            # Sanitize value
            if isinstance(value, str):
                sanitized[key] = InputSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = InputSanitizer.sanitize_dict(value, max_depth - 1)
            elif isinstance(value, list):
                sanitized[key] = [
                    InputSanitizer.sanitize_string(v) if isinstance(v, str) else v
                    for v in value[:100]  # Limit list size
                ]
            else:
                sanitized[key] = value

        return sanitized


# ============================================================================
# VALIDATION SCHEMAS
# ============================================================================

class CircuitDataSchema(BaseModel):
    """Schema for circuit execution data"""

    class Config:
        extra = "allow"  # Allow extra fields
        max_anystr_length = 10000

    @validator("*", pre=True)
    def sanitize_strings(cls, v):
        """Sanitize all string fields"""
        if isinstance(v, str):
            return InputSanitizer.sanitize_string(v)
        return v


class CircuitExecutionRequest(BaseModel):
    """Validated circuit execution request"""

    circuit_name: str = Field(..., min_length=1, max_length=100)
    data: Dict[str, Any] = Field(default_factory=dict)
    check_triggers: bool = True
    timeout: Optional[int] = Field(None, ge=1, le=600)  # 1-600 seconds

    @validator("circuit_name")
    def validate_circuit_name(cls, v):
        """Validate circuit name"""
        # Only allow alphanumeric, underscore, hyphen
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Circuit name can only contain letters, numbers, underscore, and hyphen")

        # Check for injection attempts
        InputSanitizer.validate_safe_input(v, "circuit_name")

        return v

    @validator("data")
    def validate_data(cls, v):
        """Validate and sanitize data"""
        # Sanitize dictionary
        sanitized = InputSanitizer.sanitize_dict(v)

        # Check for injection in values
        for key, value in sanitized.items():
            if isinstance(value, str):
                try:
                    InputSanitizer.validate_safe_input(value, f"data.{key}")
                except InjectionAttemptError as e:
                    logger.error(f"Injection attempt blocked: {e}")
                    raise ValueError(f"Invalid data format: {e}")

        return sanitized


class RAGQueryRequest(BaseModel):
    """Validated RAG query request"""

    query: str = Field(..., min_length=1, max_length=1000)
    context: Dict[str, Any] = Field(default_factory=dict)
    k: int = Field(10, ge=1, le=100)

    @validator("query")
    def validate_query(cls, v):
        """Validate query"""
        # Sanitize
        v = InputSanitizer.sanitize_string(v, max_length=1000)

        # Check for injection
        InputSanitizer.validate_safe_input(v, "query")

        return v

    @validator("context")
    def validate_context(cls, v):
        """Validate context"""
        return InputSanitizer.sanitize_dict(v)


class MLPredictionRequest(BaseModel):
    """Validated ML prediction request"""

    model_name: str = Field(..., min_length=1, max_length=100)
    features: Dict[str, Any] = Field(..., min_items=1)

    @validator("model_name")
    def validate_model_name(cls, v):
        """Validate model name"""
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Model name can only contain letters, numbers, underscore, and hyphen")

        InputSanitizer.validate_safe_input(v, "model_name")

        return v

    @validator("features")
    def validate_features(cls, v):
        """Validate features"""
        return InputSanitizer.sanitize_dict(v)


# ============================================================================
# VALIDATOR CLASS
# ============================================================================

class CircuitRequestValidator:
    """
    Request validator for Circuit OS
    """

    def __init__(self):
        self.sanitizer = InputSanitizer()

        # Allowed circuit names (whitelist approach)
        self.allowed_circuit_names: Optional[Set[str]] = None

        # Blocked patterns
        self.blocked_patterns: List[str] = []

    def set_allowed_circuits(self, circuit_names: List[str]):
        """Set whitelist of allowed circuit names"""
        self.allowed_circuit_names = set(circuit_names)
        logger.info(f"Circuit whitelist set: {len(circuit_names)} circuits allowed")

    def add_blocked_pattern(self, pattern: str):
        """Add blocked regex pattern"""
        self.blocked_patterns.append(pattern)
        logger.info(f"Added blocked pattern: {pattern}")

    def validate_circuit_request(
        self,
        circuit_name: str,
        data: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Validate circuit execution request

        Returns (validated_circuit_name, validated_data)
        Raises ValidationError on invalid input
        """
        # Validate circuit name
        if self.allowed_circuit_names:
            if circuit_name not in self.allowed_circuit_names:
                raise ValidationError(f"Circuit '{circuit_name}' not in whitelist")

        # Check blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, circuit_name, re.IGNORECASE):
                raise ValidationError(f"Circuit name matches blocked pattern")

        # Sanitize
        try:
            request = CircuitExecutionRequest(
                circuit_name=circuit_name,
                data=data
            )
            return request.circuit_name, request.data

        except Exception as e:
            logger.error(f"Validation failed: {e}")
            raise ValidationError(f"Invalid request: {e}")

    def validate_rag_query(
        self,
        query: str,
        context: Dict[str, Any] = None,
        k: int = 10
    ) -> Tuple[str, Dict[str, Any], int]:
        """Validate RAG query request"""
        try:
            request = RAGQueryRequest(
                query=query,
                context=context or {},
                k=k
            )
            return request.query, request.context, request.k

        except Exception as e:
            logger.error(f"RAG query validation failed: {e}")
            raise ValidationError(f"Invalid RAG query: {e}")

    def validate_ml_prediction(
        self,
        model_name: str,
        features: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """Validate ML prediction request"""
        try:
            request = MLPredictionRequest(
                model_name=model_name,
                features=features
            )
            return request.model_name, request.features

        except Exception as e:
            logger.error(f"ML prediction validation failed: {e}")
            raise ValidationError(f"Invalid ML prediction request: {e}")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def sanitize_input(value: Any) -> Any:
    """Sanitize input value"""
    if isinstance(value, str):
        return InputSanitizer.sanitize_string(value)
    elif isinstance(value, dict):
        return InputSanitizer.sanitize_dict(value)
    else:
        return value


def validate_circuit_data(circuit_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate circuit execution data

    Raises HTTPException on validation failure
    """
    validator = CircuitRequestValidator()

    try:
        _, validated_data = validator.validate_circuit_request(circuit_name, data)
        return validated_data

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InjectionAttemptError as e:
        logger.error(f"Injection attempt blocked: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input detected"
        )


def validate_and_sanitize_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    General request validation and sanitization

    Returns sanitized data
    """
    try:
        # Sanitize all strings
        sanitized = InputSanitizer.sanitize_dict(request_data)

        # Check for injection attempts
        for key, value in sanitized.items():
            if isinstance(value, str):
                InputSanitizer.validate_safe_input(value, key)

        return sanitized

    except InjectionAttemptError as e:
        logger.error(f"Injection attempt: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input detected"
        )
