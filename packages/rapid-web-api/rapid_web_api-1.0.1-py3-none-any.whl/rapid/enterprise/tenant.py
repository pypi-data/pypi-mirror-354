"""
Multi-tenant configuration and service tiers
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List


class ServiceTier(Enum):
    """Enterprise service tiers"""

    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    ENTERPRISE = "enterprise"


@dataclass
class Tenant:
    """Multi-tenant configuration"""

    tenant_id: str
    name: str
    tier: ServiceTier
    created_at: datetime
    settings: Dict[str, Any] = field(default_factory=dict)
    resource_limits: Dict[str, int] = field(default_factory=dict)
    custom_domains: List[str] = field(default_factory=list)
    is_active: bool = True

    def get_rate_limit(self) -> int:
        """Get rate limit based on service tier"""
        limits = {
            ServiceTier.BRONZE: 1000,
            ServiceTier.SILVER: 5000,
            ServiceTier.GOLD: 25000,
            ServiceTier.PLATINUM: 100000,
            ServiceTier.ENTERPRISE: -1,  # Unlimited
        }
        return limits.get(self.tier, 1000)

    def get_concurrent_connections(self) -> int:
        """Get max concurrent connections based on tier"""
        limits = {
            ServiceTier.BRONZE: 100,
            ServiceTier.SILVER: 500,
            ServiceTier.GOLD: 2500,
            ServiceTier.PLATINUM: 10000,
            ServiceTier.ENTERPRISE: -1,  # Unlimited
        }
        return limits.get(self.tier, 100)
