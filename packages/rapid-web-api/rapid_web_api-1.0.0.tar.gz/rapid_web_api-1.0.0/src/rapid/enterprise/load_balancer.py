"""
Load balancer for cluster mode
"""

import random
from datetime import datetime
from typing import Dict, Optional

from .monitoring import HealthStatus


class LoadBalancer:
    """Simple load balancer for cluster mode"""

    def __init__(self, enterprise_server):
        self.server = enterprise_server
        self.node_weights: Dict[str, float] = {}

    def register_node(self, node_id: str, weight: float = 1.0):
        """Register node in load balancer"""
        self.node_weights[node_id] = weight
        self.server.cluster_nodes[node_id] = {
            "weight": weight,
            "last_seen": datetime.utcnow(),
            "health_status": HealthStatus.HEALTHY.value,
        }

    def get_best_node(self) -> Optional[str]:
        """Get best node for request routing"""
        if not self.node_weights:
            return None

        # Simple weighted random selection
        total_weight = sum(self.node_weights.values())
        if total_weight == 0:
            return None

        r = random.uniform(0, total_weight)
        cumulative_weight = 0

        for node_id, weight in self.node_weights.items():
            cumulative_weight += weight
            if r <= cumulative_weight:
                return node_id

        return list(self.node_weights.keys())[0]  # Fallback
