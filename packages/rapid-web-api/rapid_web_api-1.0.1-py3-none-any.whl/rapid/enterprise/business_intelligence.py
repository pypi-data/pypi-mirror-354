"""
Business intelligence and analytics utilities
"""

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Optional

from .monitoring import MetricPoint


class BusinessIntelligence:
    """Business intelligence and analytics utilities"""

    def __init__(self, enterprise_server):
        self.server = enterprise_server

    def generate_usage_report(
        self, start_date: datetime, end_date: datetime, tenant_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate usage analytics report"""

        # Filter metrics by date range and tenant
        filtered_metrics = []
        for metric_name, points in self.server.business_metrics.items():
            for point in points:
                if start_date <= point.timestamp <= end_date:
                    if not tenant_id or point.tags.get("tenant_id") == tenant_id:
                        filtered_metrics.append((metric_name, point))

        # Aggregate data
        usage_by_day = defaultdict(int)
        usage_by_tenant = defaultdict(int)

        for metric_name, point in filtered_metrics:
            day_key = point.timestamp.date().isoformat()
            usage_by_day[day_key] += point.value

            tenant = point.tags.get("tenant_id", "unknown")
            usage_by_tenant[tenant] += point.value

        return {
            "report_period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
            },
            "total_usage": sum(usage_by_day.values()),
            "usage_by_day": dict(usage_by_day),
            "usage_by_tenant": dict(usage_by_tenant),
            "metrics_analyzed": len(filtered_metrics),
        }

    def get_tenant_analytics(self, tenant_id: str) -> Dict[str, Any]:
        """Get detailed analytics for specific tenant"""

        if tenant_id not in self.server.tenants:
            return {"error": "Tenant not found"}

        tenant = self.server.tenants[tenant_id]

        # Get tenant-specific metrics
        tenant_metrics = []
        for metric_name, points in self.server.business_metrics.items():
            tenant_points = [p for p in points if p.tags.get("tenant_id") == tenant_id]
            if tenant_points:
                tenant_metrics.append((metric_name, tenant_points))

        return {
            "tenant_info": {
                "id": tenant.tenant_id,
                "name": tenant.name,
                "tier": tenant.tier.value,
                "created_at": tenant.created_at.isoformat(),
                "is_active": tenant.is_active,
            },
            "usage_limits": {
                "rate_limit": tenant.get_rate_limit(),
                "concurrent_connections": tenant.get_concurrent_connections(),
            },
            "current_usage": self.server.tenant_usage.get(tenant_id, {}),
            "metrics_available": len(tenant_metrics),
        }

