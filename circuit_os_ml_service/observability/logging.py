"""
Structured Logging
JSON-formatted logging for Circuit OS
"""

import logging
import json
import sys
from typing import Dict, Any, Optional
from datetime import datetime
from pythonjsonlogger import jsonlogger
import os


# ============================================================================
# STRUCTURED LOGGER
# ============================================================================

class StructuredLogger:
    """
    Structured logging with JSON format
    """

    def __init__(
        self,
        name: str = "circuit-os",
        level: str = None,
        output_file: Optional[str] = None
    ):
        self.name = name
        self.level = level or os.getenv("LOG_LEVEL", "INFO")
        self.output_file = output_file

        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, self.level.upper()))

        # Remove existing handlers
        self.logger.handlers = []

        # Create formatter
        self.formatter = CustomJsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s'
        )

        # Add console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

        # Add file handler if specified
        if output_file:
            file_handler = logging.FileHandler(output_file)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)

        self.logger.info("Structured logging initialized", extra={
            "log_level": self.level,
            "output_file": output_file or "console"
        })

    def _add_context(self, extra: Dict = None) -> Dict:
        """Add standard context to log entry"""
        context = {
            "service": "circuit-os",
            "environment": os.getenv("ENVIRONMENT", "development"),
        }

        if extra:
            context.update(extra)

        return context

    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, extra=self._add_context(kwargs))

    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, extra=self._add_context(kwargs))

    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, extra=self._add_context(kwargs))

    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, extra=self._add_context(kwargs))

    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, extra=self._add_context(kwargs))

    def exception(self, message: str, exc_info=True, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, exc_info=exc_info, extra=self._add_context(kwargs))

    # ========================================================================
    # SPECIFIC LOGGING METHODS
    # ========================================================================

    def log_circuit_execution(
        self,
        circuit_name: str,
        execution_id: str,
        status: str,
        duration: float = None,
        actions_count: int = None,
        error: str = None
    ):
        """Log circuit execution"""
        self.info(
            f"Circuit execution: {circuit_name}",
            circuit_name=circuit_name,
            execution_id=execution_id,
            status=status,
            duration_seconds=duration,
            actions_count=actions_count,
            error=error,
            event_type="circuit_execution"
        )

    def log_api_request(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        duration: float = None,
        user_id: str = None,
        request_id: str = None
    ):
        """Log API request"""
        self.info(
            f"{method} {endpoint} {status_code}",
            http_method=method,
            http_endpoint=endpoint,
            http_status=status_code,
            duration_seconds=duration,
            user_id=user_id,
            request_id=request_id,
            event_type="api_request"
        )

    def log_security_event(
        self,
        event_type: str,
        user_id: str = None,
        email: str = None,
        status: str = None,
        details: Dict = None
    ):
        """Log security event"""
        log_method = self.warning if status == "failed" else self.info

        log_method(
            f"Security event: {event_type}",
            security_event_type=event_type,
            user_id=user_id,
            email=email,
            status=status,
            details=details or {},
            event_type="security"
        )

    def log_ml_prediction(
        self,
        model_name: str,
        prediction_id: str,
        confidence: float = None,
        duration: float = None,
        features_count: int = None
    ):
        """Log ML prediction"""
        self.info(
            f"ML prediction: {model_name}",
            model_name=model_name,
            prediction_id=prediction_id,
            confidence=confidence,
            duration_seconds=duration,
            features_count=features_count,
            event_type="ml_prediction"
        )

    def log_rag_query(
        self,
        query: str,
        documents_count: int,
        duration: float = None,
        query_id: str = None
    ):
        """Log RAG query"""
        self.info(
            f"RAG query: {query[:50]}...",
            query_preview=query[:100],
            documents_retrieved=documents_count,
            duration_seconds=duration,
            query_id=query_id,
            event_type="rag_query"
        )

    def log_error(
        self,
        error_type: str,
        error_message: str,
        context: Dict = None,
        exception: Exception = None
    ):
        """Log error with context"""
        extra = {
            "error_type": error_type,
            "error_message": error_message,
            "context": context or {},
            "event_type": "error"
        }

        if exception:
            self.exception(
                f"Error: {error_type}",
                exc_info=exception,
                **extra
            )
        else:
            self.error(
                f"Error: {error_type}",
                **extra
            )


# ============================================================================
# CUSTOM JSON FORMATTER
# ============================================================================

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter with Circuit OS fields
    """

    def add_fields(self, log_record, record, message_dict):
        """Add custom fields to log record"""
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        # Add timestamp
        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().isoformat() + 'Z'

        # Add level
        if not log_record.get('level'):
            log_record['level'] = record.levelname

        # Add logger name
        if not log_record.get('logger'):
            log_record['logger'] = record.name

        # Add correlation ID if in context
        # (would come from request context in production)


# ============================================================================
# GLOBAL LOGGER
# ============================================================================

_structured_logger = None


def get_logger(name: str = "circuit-os") -> StructuredLogger:
    """Get global structured logger instance"""
    global _structured_logger
    if _structured_logger is None:
        _structured_logger = StructuredLogger(name=name)
    return _structured_logger


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def log_circuit_execution(
    circuit_name: str,
    execution_id: str,
    status: str,
    **kwargs
):
    """Convenience function to log circuit execution"""
    logger = get_logger()
    logger.log_circuit_execution(circuit_name, execution_id, status, **kwargs)


def log_security_event(event_type: str, **kwargs):
    """Convenience function to log security event"""
    logger = get_logger()
    logger.log_security_event(event_type, **kwargs)


def log_error(error_type: str, error_message: str, **kwargs):
    """Convenience function to log error"""
    logger = get_logger()
    logger.log_error(error_type, error_message, **kwargs)
