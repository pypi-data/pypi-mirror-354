"""
ASGI server implementation for Rapid framework
"""

import asyncio
import signal
import sys
from typing import Optional

try:
    import uvicorn

    HAS_UVICORN = True
except ImportError:
    HAS_UVICORN = False

try:
    import gunicorn

    HAS_GUNICORN = True
except ImportError:
    HAS_GUNICORN = False


class RapidServer:
    """
    High-performance ASGI server for Rapid applications.

    Supports multiple server backends with automatic selection.
    """

    def __init__(self, app, server_type: str = "auto"):
        self.app = app
        self.server_type = server_type
        self._setup_event_loop()

    def _setup_event_loop(self):
        """Setup optimized event loop"""
        if sys.platform != "win32":
            try:
                import uvloop

                uvloop.install()
            except Exception:  # nosec B110
                # Fall back to default event loop if uvloop unavailable
                pass

    def run(
        self,
        host: str = "127.0.0.1",
        port: int = 8000,
        workers: int = 1,
        reload: bool = False,
        log_level: str = "info",
    ):
        """Run the server with optimal configuration"""

        if not HAS_UVICORN:
            raise RuntimeError(
                "uvicorn is required to run Rapid applications. "
                "Install it with: pip install uvicorn"
            )

        # Configure uvicorn for optimal performance
        config = {
            "app": self.app,
            "host": host,
            "port": port,
            "reload": reload,
            "log_level": log_level,
            "access_log": False,  # Disable for performance
            "server_header": False,  # Disable for performance
            "date_header": False,  # Disable for performance
        }

        if workers > 1 and not reload:
            # Use gunicorn for multi-worker setups
            if HAS_GUNICORN:
                self._run_gunicorn(config, workers)
            else:
                print("Warning: gunicorn not available, running single worker")
                self._run_uvicorn(config)
        else:
            self._run_uvicorn(config)

    def _run_uvicorn(self, config):
        """Run with uvicorn"""
        import uvicorn

        uvicorn.run(**config)

    def _run_gunicorn(self, config, workers):
        """Run with gunicorn + uvicorn workers"""
        from gunicorn.app.base import BaseApplication

        class StandaloneApplication(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                config = {
                    key: value
                    for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None
                }
                for key, value in config.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        options = {
            "bind": f"{config['host']}:{config['port']}",
            "workers": workers,
            "worker_class": "uvicorn.workers.UvicornWorker",
            "worker_connections": 1000,
            "max_requests": 1000,
            "max_requests_jitter": 50,
            "preload_app": True,
            "keepalive": 2,
        }

        StandaloneApplication(config["app"], options).run()


def run_app(app, **kwargs):
    """Convenience function to run Rapid applications"""
    server = RapidServer(app)
    server.run(**kwargs)
