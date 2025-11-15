"""
CircuitContext - State management for circuit execution
Thread-safe context object that flows through action sequence
"""

from typing import Any, Dict, Optional
from datetime import datetime
import uuid
import threading


class CircuitContext:
    """
    Context object that maintains state during circuit execution

    Features:
    - Get/set variables
    - Execution metadata tracking
    - Action execution history
    - Error recording
    - Thread-safe operations
    """

    def __init__(self, initial_data: Dict[str, Any] = None):
        self.execution_id = str(uuid.uuid4())
        self.started_at = datetime.now()
        self._data = initial_data or {}
        self._metadata = {
            "execution_id": self.execution_id,
            "started_at": self.started_at.isoformat(),
            "actions_executed": [],
            "errors": []
        }
        self._lock = threading.RLock()  # Reentrant lock for thread safety

    def get(self, key: str, default: Any = None) -> Any:
        """Get variable from context (thread-safe)"""
        with self._lock:
            return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set variable in context (thread-safe)"""
        with self._lock:
            self._data[key] = value

    def has(self, key: str) -> bool:
        """Check if variable exists"""
        with self._lock:
            return key in self._data

    def merge(self, data: Dict[str, Any]) -> None:
        """Merge multiple variables"""
        with self._lock:
            self._data.update(data)

    def get_all(self) -> Dict[str, Any]:
        """Get all context data (returns copy for safety)"""
        with self._lock:
            return self._data.copy()

    def add_metadata(self, key: str, value: Any) -> None:
        """Add execution metadata"""
        with self._lock:
            self._metadata[key] = value

    def record_action(self, action_name: str, duration: float, success: bool) -> None:
        """Record action execution"""
        with self._lock:
            self._metadata["actions_executed"].append({
                "action": action_name,
                "duration_ms": duration * 1000,
                "success": success,
                "timestamp": datetime.now().isoformat()
            })

    def record_error(self, action_name: str, error: str) -> None:
        """Record error"""
        with self._lock:
            self._metadata["errors"].append({
                "action": action_name,
                "error": str(error),
                "timestamp": datetime.now().isoformat()
            })

    def get_metadata(self) -> Dict[str, Any]:
        """Get execution metadata"""
        with self._lock:
            return self._metadata.copy()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize context to dictionary"""
        with self._lock:
            return {
                "data": self._data.copy(),
                "metadata": self._metadata.copy()
            }

    def __repr__(self):
        return f"CircuitContext(execution_id={self.execution_id}, actions={len(self._metadata['actions_executed'])})"
