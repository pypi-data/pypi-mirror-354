"""
Government module for Rapid - High-security applications

Optimized for:
- FIPS 140-2 compliant cryptographic operations
- Multi-factor authentication and zero-trust architecture
- Comprehensive audit logging and compliance reporting
- Role-based access control with attribute-based extensions
- FedRAMP and FISMA compliance
- Classification handling and export controls
"""

from .audit import AuditEvent, AuditLogEntry
from .compliance import ComplianceReporter
from .crypto import FIPSCrypto, SecureResponse
from .security import ClassificationLevel, SecurityClearance, SecurityContext

# Import all government components
from .server import GovernmentServer

# Export main public API
__all__ = [
    "GovernmentServer",
    "SecurityContext",
    "ClassificationLevel",
    "SecurityClearance",
    "AuditEvent",
    "AuditLogEntry",
    "ComplianceReporter",
    "FIPSCrypto",
    "SecureResponse",
]
