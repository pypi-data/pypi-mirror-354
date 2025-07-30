"""
Enterprise module for Rapid - Large-scale business applications

Optimized for:
- High availability and fault tolerance
- Advanced monitoring and observability
- Multi-tenant architecture with isolation
- Enterprise security and compliance
- Scalable clustering and load balancing
- Business intelligence and analytics
"""

from .business_intelligence import BusinessIntelligence
from .load_balancer import LoadBalancer
from .monitoring import Alert, AlertSeverity, HealthStatus, MetricPoint
from .response import EnterpriseResponse

# Import all enterprise components
from .server import EnterpriseServer
from .tenant import ServiceTier, Tenant

# Export main public API
__all__ = [
    "EnterpriseServer",
    "Tenant",
    "ServiceTier",
    "HealthStatus",
    "AlertSeverity",
    "MetricPoint",
    "Alert",
    "BusinessIntelligence",
    "LoadBalancer",
    "EnterpriseResponse",
]
