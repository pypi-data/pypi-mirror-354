"""
Enterprise monitoring, health checks, and alerting
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class HealthStatus(Enum):
    """Service health status"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"


class AlertSeverity(Enum):
    """Alert severity levels"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class MetricPoint:
    """Time-series metric data point"""

    timestamp: datetime
    value: float
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class Alert:
    """Enterprise alert configuration"""

    id: str
    name: str
    description: str
    severity: AlertSeverity
    condition: str
    threshold: float
    tenant_id: Optional[str]
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    triggered_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
