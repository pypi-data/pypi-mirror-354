"""
Enterprise response types with advanced metadata
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from ..http.response import JSONResponse


class EnterpriseResponse(JSONResponse):
    """Enterprise response with advanced metadata"""

    def __init__(
        self,
        content: Any = None,
        tenant_id: Optional[str] = None,
        business_context: Optional[Dict[str, Any]] = None,
        cache_policy: Optional[str] = None,
        **kwargs,
    ):
        # Add enterprise metadata
        if isinstance(content, dict):
            content["__meta"] = {
                "tenant_id": tenant_id,
                "timestamp": datetime.utcnow().isoformat(),
                "business_context": business_context,
                "response_id": str(uuid.uuid4()),
            }

        # Add enterprise headers
        headers = kwargs.get("headers", {})
        headers.update(
            {
                "X-Enterprise-Response": "true",
                "X-Response-ID": str(uuid.uuid4()),
                "X-Cache-Policy": cache_policy or "default",
            }
        )

        if tenant_id:
            headers["X-Tenant-ID"] = tenant_id

        kwargs["headers"] = headers

        super().__init__(content=content, **kwargs)
