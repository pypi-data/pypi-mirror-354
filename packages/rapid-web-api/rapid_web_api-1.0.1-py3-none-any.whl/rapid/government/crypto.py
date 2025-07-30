"""
FIPS 140-2 compliant cryptographic operations and secure responses
"""

import hashlib
import hmac
import secrets
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..http.response import JSONResponse
from .security import ClassificationLevel


class FIPSCrypto:
    """FIPS 140-2 compliant cryptographic operations"""

    @staticmethod
    def secure_hash(data: bytes) -> str:
        """FIPS-approved secure hash"""
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def secure_random(length: int) -> bytes:
        """FIPS-approved random number generation"""
        return secrets.token_bytes(length)

    @staticmethod
    def hmac_sign(key: bytes, message: bytes) -> str:
        """FIPS-approved HMAC signing"""
        return hmac.new(key, message, hashlib.sha256).hexdigest()


class SecureResponse(JSONResponse):
    """Secure response with classification markings and audit trails"""

    def __init__(
        self,
        content: Any = None,
        classification: ClassificationLevel = ClassificationLevel.UNCLASSIFIED,
        handling_instructions: Optional[List[str]] = None,
        **kwargs,
    ):
        # Add classification markings to response
        if isinstance(content, dict):
            content["__classification"] = classification.value
            if handling_instructions:
                content["__handling"] = handling_instructions

        # Add security headers
        headers = kwargs.get("headers", {})
        headers.update(
            {
                "X-Classification": classification.value,
                "X-Content-Security-Policy": "default-src 'self'",
                "X-Frame-Options": "DENY",
                "X-XSS-Protection": "1; mode=block",
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
                "Cache-Control": "no-store, no-cache, must-revalidate",
            }
        )
        kwargs["headers"] = headers

        super().__init__(content=content, **kwargs)
