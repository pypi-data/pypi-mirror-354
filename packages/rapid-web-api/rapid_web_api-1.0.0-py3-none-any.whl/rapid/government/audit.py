"""
Audit logging and event tracking system
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from .security import ClassificationLevel


class AuditEvent(Enum):
    """Types of events that must be audited"""

    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    LOGOUT = "logout"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    PERMISSION_DENIED = "permission_denied"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    SYSTEM_ERROR = "system_error"
    SECURITY_VIOLATION = "security_violation"
    CLASSIFICATION_VIOLATION = "classification_violation"


@dataclass
class AuditLogEntry:
    """Audit log entry with tamper-proof features"""

    id: str
    timestamp: datetime
    event_type: AuditEvent
    user_id: Optional[str]
    session_id: Optional[str]
    source_ip: str
    resource: Optional[str]
    action: str
    result: str  # SUCCESS, FAILURE, DENIED
    details: Dict[str, Any]
    classification: ClassificationLevel
    hash_chain: str  # Hash linking to previous entry for tamper detection

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type.value,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "source_ip": self.source_ip,
            "resource": self.resource,
            "action": self.action,
            "result": self.result,
            "details": self.details,
            "classification": self.classification.value,
            "hash_chain": self.hash_chain,
        }
