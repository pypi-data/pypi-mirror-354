"""
Enterprise server with high availability and multi-tenant support
"""

import logging
import threading
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional

from ..core.app import Rapid
from ..http.request import Request
from ..http.response import JSONResponse
from .monitoring import HealthStatus, MetricPoint
from .tenant import ServiceTier, Tenant


class EnterpriseServer(Rapid):
    """
    Enterprise server optimized for large-scale business applications.

    Features:
    - High availability with health monitoring
    - Multi-tenant architecture with resource isolation
    - Advanced monitoring and alerting
    - Clustering and load balancing
    - Business intelligence and analytics
    - Enterprise security and compliance
    """

    def __init__(
        self,
        title: str = "Rapid Enterprise Server",
        cluster_mode: bool = False,
        multi_tenant: bool = True,
        health_check_interval: int = 30,
        metrics_retention_hours: int = 168,  # 7 days
        **kwargs,
    ):
        super().__init__(title=title, **kwargs)

        self.cluster_mode = cluster_mode
        self.multi_tenant = multi_tenant
        self.health_check_interval = health_check_interval
        self.metrics_retention = timedelta(hours=metrics_retention_hours)

        # Multi-tenancy
        self.tenants: Dict[str, Tenant] = {}
        self.tenant_usage: Dict[str, Dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )

        # Monitoring and metrics
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self.alerts: Dict[str, Any] = {}  # Will be Alert objects from monitoring module
        self.health_status = HealthStatus.HEALTHY
        self.health_checks: Dict[str, Callable] = {}

        # Performance tracking
        self.request_counts: Dict[str, int] = defaultdict(int)
        self.response_times: deque = deque(maxlen=1000)
        self.error_counts: Dict[str, int] = defaultdict(int)

        # Clustering (if enabled)
        self.cluster_nodes: Dict[str, Dict[str, Any]] = {}
        self.node_id = str(uuid.uuid4())

        # Business intelligence
        self.business_metrics: Dict[str, List[MetricPoint]] = defaultdict(list)

        # Setup enterprise logging
        self._setup_enterprise_logging()

        # Start background tasks
        self._start_background_tasks()

    def _setup_enterprise_logging(self):
        """Setup enterprise-grade logging"""
        # Create specialized loggers
        self.access_logger = logging.getLogger("rapid.enterprise.access")
        self.performance_logger = logging.getLogger("rapid.enterprise.performance")
        self.business_logger = logging.getLogger("rapid.enterprise.business")
        self.security_logger = logging.getLogger("rapid.enterprise.security")

        # Configure handlers (in production, use log aggregation service)
        for logger in [
            self.access_logger,
            self.performance_logger,
            self.business_logger,
            self.security_logger,
        ]:
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(
                f"enterprise_{logger.name.split('.')[-1]}.log"
            )
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def _start_background_tasks(self):
        """Start enterprise background monitoring tasks"""
        if not hasattr(self, "_background_started"):
            self._background_started = True

            # Start health monitoring
            threading.Thread(target=self._health_monitor_loop, daemon=True).start()

            # Start metrics cleanup
            threading.Thread(target=self._metrics_cleanup_loop, daemon=True).start()

            # Start cluster heartbeat (if clustering enabled)
            if self.cluster_mode:
                threading.Thread(
                    target=self._cluster_heartbeat_loop, daemon=True
                ).start()

    def _health_monitor_loop(self):
        """Background health monitoring"""
        while True:
            try:
                self._perform_health_checks()
                time.sleep(self.health_check_interval)
            except Exception as e:
                self.performance_logger.error(f"Health monitor error: {e}")
                time.sleep(self.health_check_interval)

    def _metrics_cleanup_loop(self):
        """Clean up old metrics data"""
        while True:
            try:
                cutoff_time = datetime.utcnow() - self.metrics_retention

                # Clean up business metrics
                for metric_name, points in self.business_metrics.items():
                    self.business_metrics[metric_name] = [
                        p for p in points if p.timestamp > cutoff_time
                    ]

                time.sleep(3600)  # Run every hour
            except Exception as e:
                self.performance_logger.error(f"Metrics cleanup error: {e}")
                time.sleep(3600)

    def _cluster_heartbeat_loop(self):
        """Send cluster heartbeat (if clustering enabled)"""
        while True:
            try:
                if self.cluster_mode:
                    self._send_cluster_heartbeat()
                time.sleep(10)  # Heartbeat every 10 seconds
            except Exception as e:
                self.performance_logger.error(f"Cluster heartbeat error: {e}")
                time.sleep(10)

    def register_tenant(
        self,
        tenant_id: str,
        name: str,
        tier: ServiceTier,
        settings: Optional[Dict[str, Any]] = None,
        resource_limits: Optional[Dict[str, int]] = None,
    ) -> Tenant:
        """Register new tenant in multi-tenant environment"""

        tenant = Tenant(
            tenant_id=tenant_id,
            name=name,
            tier=tier,
            created_at=datetime.utcnow(),
            settings=settings or {},
            resource_limits=resource_limits or {},
        )

        self.tenants[tenant_id] = tenant

        # Log tenant registration
        self.business_logger.info(f"Tenant registered: {tenant_id} ({tier.value})")

        return tenant

    def enterprise_endpoint(
        self,
        path: str,
        tenant_aware: bool = True,
        rate_limit: bool = True,
        monitor_performance: bool = True,
        business_metric: Optional[str] = None,
        **kwargs,
    ):
        """Register enterprise endpoint with advanced monitoring"""

        def decorator(handler):
            async def enterprise_wrapper(request: Request, **path_params):
                start_time = time.perf_counter()
                tenant_id = None

                try:
                    # Extract tenant information
                    if tenant_aware and self.multi_tenant:
                        tenant_id = self._extract_tenant_id(request)
                        if not tenant_id or tenant_id not in self.tenants:
                            return JSONResponse(
                                content={"error": "Invalid tenant"}, status_code=400
                            )

                        tenant = self.tenants[tenant_id]
                        if not tenant.is_active:
                            return JSONResponse(
                                content={"error": "Tenant suspended"}, status_code=403
                            )

                    # Rate limiting
                    if rate_limit and tenant_id:
                        if not self._check_rate_limit(tenant_id, request):
                            return JSONResponse(
                                content={"error": "Rate limit exceeded"},
                                status_code=429,
                            )

                    # Add enterprise context to request
                    getattr(request, "tenant_id", None) = tenant_id
                    getattr(request, "enterprise_context", {}) = {
                        "tenant": self.tenants.get(tenant_id) if tenant_id else None,
                        "start_time": start_time,
                        "path": path,
                    }

                    # Call original handler
                    response = await handler(request, **path_params)

                    # Track performance
                    if monitor_performance:
                        duration = time.perf_counter() - start_time
                        self._record_performance_metric(path, duration, tenant_id)

                    # Track business metrics
                    if business_metric:
                        self._record_business_metric(
                            business_metric, 1, {"tenant_id": tenant_id or "system"}
                        )

                    # Log successful request
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    self.access_logger.info(
                        f"Success: {path} - Tenant: {tenant_id} - "
                        f"Duration: {duration_ms:.2f}ms"
                    )

                    return response

                except Exception as e:
                    # Track errors
                    self.error_counts[f"{path}:{type(e).__name__}"] += 1

                    # Log error
                    self.performance_logger.error(
                        f"Error in {path}: {e} - Tenant: {tenant_id}"
                    )

                    # Check if this triggers any alerts
                    self._check_alert_conditions()

                    raise

            # Register the wrapped handler
            route = self.get(path, **kwargs)(enterprise_wrapper)
            route.tenant_aware = tenant_aware
            route.rate_limit = rate_limit
            route.business_metric = business_metric

            return route

        return decorator

    def _extract_tenant_id(self, request: Request) -> Optional[str]:
        """Extract tenant ID from request"""
        # Check header first
        tenant_id = request.headers.get("X-Tenant-ID")
        if tenant_id:
            return tenant_id

        # Check subdomain
        host = request.headers.get("Host", "")
        if "." in host:
            subdomain = host.split(".")[0]
            if subdomain in self.tenants:
                return subdomain

        # Check query parameter
        # In production, you'd parse query string properly
        return None

    def _check_rate_limit(self, tenant_id: str, request: Request) -> bool:
        """Check if request is within rate limits"""
        if tenant_id not in self.tenants:
            return False

        tenant = self.tenants[tenant_id]
        limit = tenant.get_rate_limit()

        if limit == -1:  # Unlimited
            return True

        # Simple rate limiting - in production use Redis or similar
        current_minute = int(time.time() / 60)
        key = f"{tenant_id}:{current_minute}"

        self.tenant_usage[tenant_id][key] += 1

        # Clean old entries
        cutoff = current_minute - 1
        for old_key in list(self.tenant_usage[tenant_id].keys()):
            if int(old_key.split(":")[1]) < cutoff:
                del self.tenant_usage[tenant_id][old_key]

        # Check limit
        current_usage = sum(self.tenant_usage[tenant_id].values())
        return current_usage <= limit

    def _record_performance_metric(
        self, path: str, duration: float, tenant_id: Optional[str]
    ):
        """Record performance metrics"""
        self.response_times.append(duration)
        self.request_counts[path] += 1

        # Store detailed metrics
        metric_point = MetricPoint(
            timestamp=datetime.utcnow(),
            value=duration * 1000,  # Convert to milliseconds
            tags={"path": path, "tenant_id": tenant_id or "system"},
        )

        self.metrics["response_time"].append(metric_point)

    def _record_business_metric(
        self, metric_name: str, value: float, tags: Dict[str, str]
    ):
        """Record business intelligence metrics"""
        metric_point = MetricPoint(timestamp=datetime.utcnow(), value=value, tags=tags)

        self.business_metrics[metric_name].append(metric_point)

        # Log to business intelligence system
        self.business_logger.info(f"Metric: {metric_name} = {value} | {tags}")

    def add_health_check(self, name: str, check_function: Callable[[], bool]):
        """Add custom health check"""
        self.health_checks[name] = check_function

    def _perform_health_checks(self):
        """Perform all registered health checks"""
        failed_checks = []

        # Built-in health checks
        if not self._check_memory_usage():
            failed_checks.append("memory_usage")

        if not self._check_response_times():
            failed_checks.append("response_times")

        # Custom health checks
        for name, check_func in self.health_checks.items():
            try:
                if not check_func():
                    failed_checks.append(name)
            except Exception as e:
                failed_checks.append(f"{name}_error")
                self.performance_logger.error(f"Health check {name} failed: {e}")

        # Update health status
        if len(failed_checks) == 0:
            self.health_status = HealthStatus.HEALTHY
        elif len(failed_checks) <= 2:
            self.health_status = HealthStatus.DEGRADED
        else:
            self.health_status = HealthStatus.UNHEALTHY

    def _check_memory_usage(self) -> bool:
        """Check if memory usage is acceptable"""
        try:
            import psutil

            memory_percent = psutil.virtual_memory().percent
            return memory_percent < 85  # Alert if >85% memory usage
        except ImportError:
            return True  # Skip if psutil not available

    def _check_response_times(self) -> bool:
        """Check if response times are acceptable"""
        if not self.response_times:
            return True

        # Calculate 95th percentile
        sorted_times = sorted(self.response_times)
        p95_index = int(len(sorted_times) * 0.95)
        p95_time = (
            sorted_times[p95_index]
            if p95_index < len(sorted_times)
            else sorted_times[-1]
        )

        return p95_time < 1.0  # Alert if 95th percentile > 1 second

    def _check_alert_conditions(self):
        """Check if any alert conditions are met"""
        for alert_id, alert in self.alerts.items():
            if not alert.is_active:
                continue

            if self._evaluate_alert_condition(alert):
                if not alert.triggered_at:
                    alert.triggered_at = datetime.utcnow()
                    self._trigger_alert(alert)

    def _evaluate_alert_condition(self, alert) -> bool:
        """Evaluate if alert condition is met"""
        # Simplified alert evaluation - in production use proper rule engine
        if "error_rate" in alert.condition:
            total_requests = sum(self.request_counts.values())
            total_errors = sum(self.error_counts.values())
            if total_requests > 0:
                error_rate = total_errors / total_requests
                return error_rate > alert.threshold

        elif "response_time" in alert.condition:
            if self.response_times:
                avg_response_time = sum(self.response_times) / len(self.response_times)
                return avg_response_time > alert.threshold

        return False

    def _trigger_alert(self, alert):
        """Trigger alert notification"""
        self.security_logger.warning(
            f"ALERT TRIGGERED: {alert.name} - {alert.description}"
        )

        # In production, send to notification service (email, Slack, PagerDuty, etc.)

    def _send_cluster_heartbeat(self):
        """Send heartbeat to cluster nodes"""
        # In production, use proper service discovery
        heartbeat_data = {
            "node_id": self.node_id,
            "timestamp": datetime.utcnow().isoformat(),
            "health_status": self.health_status.value,
            "active_connections": len(getattr(self, "active_connections", [])),
            "cpu_usage": self._get_cpu_usage(),
            "memory_usage": self._get_memory_usage(),
        }

        self.performance_logger.info(f"Cluster heartbeat: {heartbeat_data}")

    def _get_cpu_usage(self) -> float:
        """Get current CPU usage"""
        try:
            import psutil

            return psutil.cpu_percent()
        except ImportError:
            return 0.0

    def _get_memory_usage(self) -> float:
        """Get current memory usage"""
        try:
            import psutil

            return psutil.virtual_memory().percent
        except ImportError:
            return 0.0

    def get_enterprise_stats(self) -> Dict[str, Any]:
        """Get comprehensive enterprise statistics"""

        # Calculate performance metrics
        avg_response_time = 0
        p95_response_time = 0
        if self.response_times:
            avg_response_time = sum(self.response_times) / len(self.response_times)
            sorted_times = sorted(self.response_times)
            p95_index = int(len(sorted_times) * 0.95)
            p95_response_time = (
                sorted_times[p95_index]
                if p95_index < len(sorted_times)
                else sorted_times[-1]
            )

        # Tenant statistics
        tenant_stats = {}
        for tier in ServiceTier:
            tenant_stats[tier.value] = len(
                [t for t in self.tenants.values() if t.tier == tier]
            )

        return {
            "service_info": {
                "cluster_mode": self.cluster_mode,
                "multi_tenant": self.multi_tenant,
                "health_status": self.health_status.value,
                "node_id": self.node_id if self.cluster_mode else None,
            },
            "performance": {
                "total_requests": sum(self.request_counts.values()),
                "total_errors": sum(self.error_counts.values()),
                "avg_response_time_ms": avg_response_time * 1000,
                "p95_response_time_ms": p95_response_time * 1000,
                "requests_per_path": dict(self.request_counts),
                "errors_by_type": dict(self.error_counts),
            },
            "tenants": {
                "total_tenants": len(self.tenants),
                "active_tenants": len(
                    [t for t in self.tenants.values() if t.is_active]
                ),
                "by_tier": tenant_stats,
            },
            "monitoring": {
                "health_checks": len(self.health_checks),
                "active_alerts": len(
                    [a for a in self.alerts.values() if a.is_active and a.triggered_at]
                ),
                "metrics_tracked": len(self.metrics),
                "business_metrics": len(self.business_metrics),
            },
            "system": {
                "cpu_usage_percent": self._get_cpu_usage(),
                "memory_usage_percent": self._get_memory_usage(),
                "uptime_seconds": (
                    datetime.utcnow() - datetime.utcnow()
                ).total_seconds(),  # Placeholder
            },
        }


