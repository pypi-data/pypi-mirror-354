"""
Security context and classification system
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Set


class ClassificationLevel(Enum):
    """Security classification levels"""

    UNCLASSIFIED = "UNCLASSIFIED"
    CUI = "CONTROLLED_UNCLASSIFIED_INFORMATION"  # Controlled Unclassified Information
    CONFIDENTIAL = "CONFIDENTIAL"
    SECRET = "SECRET"
    TOP_SECRET = "TOP_SECRET"


class SecurityClearance(Enum):
    """Personnel security clearance levels"""

    PUBLIC = "PUBLIC"
    BASIC = "BASIC"
    CONFIDENTIAL = "CONFIDENTIAL"
    SECRET = "SECRET"
    TOP_SECRET = "TOP_SECRET"
    TS_SCI = "TOP_SECRET_SCI"  # Top Secret/Sensitive Compartmented Information


@dataclass
class SecurityContext:
    """Security context for a user session"""

    user_id: str
    clearance_level: SecurityClearance
    roles: Set[str]
    attributes: Dict[str, Any]
    session_id: str
    created_at: datetime
    expires_at: datetime
    last_activity: datetime
    source_ip: str
    mfa_verified: bool = False
    hardware_token_verified: bool = False

    def is_expired(self) -> bool:
        """Check if security context has expired"""
        return datetime.utcnow() > self.expires_at

    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.utcnow()

    def can_access_classification(self, classification: ClassificationLevel) -> bool:
        """Check if user can access data at given classification level"""
        clearance_order = {
            SecurityClearance.PUBLIC: 0,
            SecurityClearance.BASIC: 1,
            SecurityClearance.CONFIDENTIAL: 2,
            SecurityClearance.SECRET: 3,
            SecurityClearance.TOP_SECRET: 4,
            SecurityClearance.TS_SCI: 5,
        }

        classification_order = {
            ClassificationLevel.UNCLASSIFIED: 0,
            ClassificationLevel.CUI: 1,
            ClassificationLevel.CONFIDENTIAL: 2,
            ClassificationLevel.SECRET: 3,
            ClassificationLevel.TOP_SECRET: 4,
        }

        return clearance_order.get(self.clearance_level, 0) >= classification_order.get(
            classification, 0
        )
