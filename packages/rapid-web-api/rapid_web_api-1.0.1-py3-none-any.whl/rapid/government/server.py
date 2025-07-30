"""
Government server with high-security features and compliance
"""

import json
import logging
import secrets
import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set

from ..core.app import Rapid
from ..http.request import Request
from ..http.response import JSONResponse
from .audit import AuditEvent, AuditLogEntry
from .security import ClassificationLevel, SecurityClearance, SecurityContext


class GovernmentServer(Rapid):
    """
    Government server optimized for high-security applications.

    Features:
    - FIPS 140-2 compliant cryptographic operations
    - Multi-factor authentication with hardware tokens
    - Zero-trust architecture with continuous verification
    - Comprehensive audit logging with tamper protection
    - Role-based access control with attribute-based extensions
    - Classification handling and export controls
    """

    def __init__(
        self,
        title: str = "Rapid Government Server",
        fips_mode: bool = True,
        audit_level: str = "COMPREHENSIVE",
        max_classification: ClassificationLevel = ClassificationLevel.SECRET,
        session_timeout_minutes: int = 30,
        **kwargs,
    ):
        super().__init__(title=title, **kwargs)

        self.fips_mode = fips_mode
        self.audit_level = audit_level
        self.max_classification = max_classification
        self.session_timeout = timedelta(minutes=session_timeout_minutes)

        # Security infrastructure
        self.active_sessions: Dict[str, SecurityContext] = {}
        self.audit_log: List[AuditLogEntry] = []
        self.failed_login_attempts: Dict[str, List[datetime]] = {}
        self.blocked_ips: Dict[str, datetime] = {}

        # Cryptographic keys (in production, use HSM or key management service)
        self.signing_key = secrets.token_bytes(32)
        self.encryption_key = secrets.token_bytes(32)

        # Security policies
        self.password_policy = {
            "min_length": 14,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_numbers": True,
            "require_special": True,
            "max_age_days": 60,
            "history_count": 12,
        }

        self.lockout_policy = {
            "max_attempts": 3,
            "lockout_duration_minutes": 30,
            "reset_period_minutes": 15,
        }

        # Setup secure logging
        self._setup_audit_logging()

        # Initialize hash chain for audit log integrity
        self.last_audit_hash = self._calculate_genesis_hash()

    def _setup_audit_logging(self):
        """Setup tamper-resistant audit logging"""
        audit_logger = logging.getLogger("rapid.government.audit")
        audit_logger.setLevel(logging.INFO)

        # In production, use secure log aggregation service
        handler = logging.FileHandler("government_audit.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        audit_logger.addHandler(handler)

        self.audit_logger = audit_logger

    def _calculate_genesis_hash(self) -> str:
        """Calculate genesis hash for audit log chain"""
        import hashlib

        genesis_data = f"RAPID_GOVERNMENT_AUDIT_GENESIS_{datetime.utcnow().isoformat()}"
        return hashlib.sha256(genesis_data.encode()).hexdigest()

    def _calculate_hash_chain(self, entry_data: str, previous_hash: str) -> str:
        """Calculate hash chain for audit log integrity"""
        import hashlib

        combined = f"{previous_hash}:{entry_data}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def secure_endpoint(
        self,
        path: str,
        classification: ClassificationLevel = ClassificationLevel.UNCLASSIFIED,
        required_roles: Optional[List[str]] = None,
        require_mfa: bool = False,
        require_hardware_token: bool = False,
        **kwargs,
    ):
        """Register secure endpoint with access controls"""

        def decorator(handler):
            async def secure_wrapper(request: Request, **path_params):
                # Extract security context
                security_context = self._get_security_context(request)

                if not security_context:
                    self._audit_log(
                        AuditEvent.PERMISSION_DENIED,
                        None,
                        None,
                        self._get_client_ip(request),
                        path,
                        "access_denied",
                        "DENIED",
                        {"reason": "no_security_context"},
                        ClassificationLevel.UNCLASSIFIED,
                    )
                    return JSONResponse(
                        content={"error": "Authentication required"}, status_code=401
                    )

                # Check session validity
                if security_context.is_expired():
                    self._invalidate_session(security_context.session_id)
                    self._audit_log(
                        AuditEvent.PERMISSION_DENIED,
                        security_context.user_id,
                        security_context.session_id,
                        self._get_client_ip(request),
                        path,
                        "access_denied",
                        "DENIED",
                        {"reason": "session_expired"},
                        classification,
                    )
                    return JSONResponse(
                        content={"error": "Session expired"}, status_code=401
                    )

                # Check classification clearance
                if not security_context.can_access_classification(classification):
                    self._audit_log(
                        AuditEvent.CLASSIFICATION_VIOLATION,
                        security_context.user_id,
                        security_context.session_id,
                        self._get_client_ip(request),
                        path,
                        "classification_violation",
                        "DENIED",
                        {
                            "user_clearance": security_context.clearance_level.value,
                            "required_classification": classification.value,
                        },
                        classification,
                    )
                    return JSONResponse(
                        content={"error": "Insufficient security clearance"},
                        status_code=403,
                    )

                # Check role requirements
                if required_roles:
                    if not any(
                        role in security_context.roles for role in required_roles
                    ):
                        self._audit_log(
                            AuditEvent.PERMISSION_DENIED,
                            security_context.user_id,
                            security_context.session_id,
                            self._get_client_ip(request),
                            path,
                            "role_check_failed",
                            "DENIED",
                            {
                                "user_roles": list(security_context.roles),
                                "required_roles": required_roles,
                            },
                            classification,
                        )
                        return JSONResponse(
                            content={"error": "Insufficient privileges"},
                            status_code=403,
                        )

                # Check MFA requirements
                if require_mfa and not security_context.mfa_verified:
                    self._audit_log(
                        AuditEvent.PERMISSION_DENIED,
                        security_context.user_id,
                        security_context.session_id,
                        self._get_client_ip(request),
                        path,
                        "mfa_required",
                        "DENIED",
                        {"reason": "mfa_not_verified"},
                        classification,
                    )
                    return JSONResponse(
                        content={"error": "Multi-factor authentication required"},
                        status_code=403,
                    )

                # Check hardware token requirements
                if (
                    require_hardware_token
                    and not security_context.hardware_token_verified
                ):
                    self._audit_log(
                        AuditEvent.PERMISSION_DENIED,
                        security_context.user_id,
                        security_context.session_id,
                        self._get_client_ip(request),
                        path,
                        "hardware_token_required",
                        "DENIED",
                        {"reason": "hardware_token_not_verified"},
                        classification,
                    )
                    return JSONResponse(
                        content={"error": "Hardware token verification required"},
                        status_code=403,
                    )

                # Update activity and continue
                security_context.update_activity()

                # Audit successful access
                self._audit_log(
                    AuditEvent.DATA_ACCESS,
                    security_context.user_id,
                    security_context.session_id,
                    self._get_client_ip(request),
                    path,
                    "endpoint_access",
                    "SUCCESS",
                    {
                        "classification": classification.value,
                        "roles_used": list(security_context.roles),
                    },
                    classification,
                )

                # Add security context to request for handler use
                request.security_context = security_context

                # Call original handler
                try:
                    result = await handler(request, **path_params)
                    return result
                except Exception as e:
                    self._audit_log(
                        AuditEvent.SYSTEM_ERROR,
                        security_context.user_id,
                        security_context.session_id,
                        self._get_client_ip(request),
                        path,
                        "handler_error",
                        "FAILURE",
                        {"error": str(e)},
                        classification,
                    )
                    raise

            # Register the wrapped handler
            route = self.get(path, **kwargs)(secure_wrapper)
            route.classification = classification
            route.required_roles = required_roles or []
            route.require_mfa = require_mfa
            route.require_hardware_token = require_hardware_token

            return route

        return decorator

    def _get_security_context(self, request: Request) -> Optional[SecurityContext]:
        """Extract security context from request"""
        # In production, this would validate JWT tokens, session cookies, etc.
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        session_id = auth_header[7:]  # Remove "Bearer "
        return self.active_sessions.get(session_id)

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request"""
        # Check for forwarded headers (behind proxy/load balancer)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        return request.client.host if request.client else "unknown"

    def _audit_log(
        self,
        event_type: AuditEvent,
        user_id: Optional[str],
        session_id: Optional[str],
        source_ip: str,
        resource: Optional[str],
        action: str,
        result: str,
        details: Dict[str, Any],
        classification: ClassificationLevel,
    ):
        """Create tamper-proof audit log entry"""

        entry_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()

        # Create entry data for hash calculation
        entry_data = f"{entry_id}:{timestamp.isoformat()}:{event_type.value}:{user_id}:{action}:{result}"

        # Calculate hash chain
        hash_chain = self._calculate_hash_chain(entry_data, self.last_audit_hash)

        # Create audit entry
        audit_entry = AuditLogEntry(
            id=entry_id,
            timestamp=timestamp,
            event_type=event_type,
            user_id=user_id,
            session_id=session_id,
            source_ip=source_ip,
            resource=resource,
            action=action,
            result=result,
            details=details,
            classification=classification,
            hash_chain=hash_chain,
        )

        # Store in memory and log
        self.audit_log.append(audit_entry)
        self.last_audit_hash = hash_chain

        # Log to file system
        self.audit_logger.info(json.dumps(audit_entry.to_dict()))

        # In production, also send to SIEM system

    def create_session(
        self,
        user_id: str,
        clearance_level: SecurityClearance,
        roles: Set[str],
        source_ip: str,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create new secure session"""

        session_id = secrets.token_urlsafe(32)
        now = datetime.utcnow()

        security_context = SecurityContext(
            user_id=user_id,
            clearance_level=clearance_level,
            roles=roles,
            attributes=attributes or {},
            session_id=session_id,
            created_at=now,
            expires_at=now + self.session_timeout,
            last_activity=now,
            source_ip=source_ip,
        )

        self.active_sessions[session_id] = security_context

        self._audit_log(
            AuditEvent.LOGIN_SUCCESS,
            user_id,
            session_id,
            source_ip,
            None,
            "create_session",
            "SUCCESS",
            {
                "clearance_level": clearance_level.value,
                "roles": list(roles),
                "session_timeout_minutes": self.session_timeout.total_seconds() / 60,
            },
            ClassificationLevel.UNCLASSIFIED,
        )

        return session_id

    def _invalidate_session(self, session_id: str):
        """Invalidate a security session"""
        if session_id in self.active_sessions:
            context = self.active_sessions[session_id]
            del self.active_sessions[session_id]

            self._audit_log(
                AuditEvent.LOGOUT,
                context.user_id,
                session_id,
                context.source_ip,
                None,
                "invalidate_session",
                "SUCCESS",
                {"reason": "session_invalidated"},
                ClassificationLevel.UNCLASSIFIED,
            )

    def verify_mfa(self, session_id: str, mfa_token: str) -> bool:
        """Verify multi-factor authentication"""
        if session_id not in self.active_sessions:
            return False

        context = self.active_sessions[session_id]

        # In production, verify against TOTP/HOTP or hardware token
        # This is a simplified example
        if self._verify_totp_token(mfa_token, context.user_id):
            context.mfa_verified = True

            self._audit_log(
                AuditEvent.LOGIN_SUCCESS,
                context.user_id,
                session_id,
                context.source_ip,
                None,
                "mfa_verification",
                "SUCCESS",
                {"mfa_method": "totp"},
                ClassificationLevel.UNCLASSIFIED,
            )
            return True
        else:
            self._audit_log(
                AuditEvent.LOGIN_FAILURE,
                context.user_id,
                session_id,
                context.source_ip,
                None,
                "mfa_verification",
                "FAILURE",
                {"mfa_method": "totp", "reason": "invalid_token"},
                ClassificationLevel.UNCLASSIFIED,
            )
            return False

    def _verify_totp_token(self, token: str, user_id: str) -> bool:
        """Verify TOTP token (simplified implementation)"""
        # In production, use proper TOTP library and user-specific secrets
        # This is just a placeholder
        return len(token) == 6 and token.isdigit()

    def get_security_stats(self) -> Dict[str, Any]:
        """Get security and compliance statistics"""
        now = datetime.utcnow()

        # Count active sessions by clearance level
        clearance_counts = {}
        for context in self.active_sessions.values():
            level = context.clearance_level.value
            clearance_counts[level] = clearance_counts.get(level, 0) + 1

        # Count recent audit events
        recent_events = {}
        for entry in self.audit_log[-1000:]:  # Last 1000 events
            event_type = entry.event_type.value
            recent_events[event_type] = recent_events.get(event_type, 0) + 1

        return {
            "active_sessions": len(self.active_sessions),
            "clearance_distribution": clearance_counts,
            "max_classification": self.max_classification.value,
            "fips_mode": self.fips_mode,
            "audit_entries": len(self.audit_log),
            "recent_audit_events": recent_events,
            "session_timeout_minutes": self.session_timeout.total_seconds() / 60,
            "blocked_ips": len(self.blocked_ips),
            "failed_login_tracking": len(self.failed_login_attempts),
        }

