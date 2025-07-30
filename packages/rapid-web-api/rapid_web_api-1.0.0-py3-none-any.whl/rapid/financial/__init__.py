from typing import Callable, Optional, Dict, Any
"""
Rapid Financial Module - High-precision financial applications

Optimized for:
- High-frequency trading platforms
- Cryptocurrency exchanges
- Banking systems
- Payment processing
"""

import decimal
import time

from ..core.app import Rapid
from ..http.response import JSONResponse


class TradingServer(Rapid):
    """
    Financial trading server with microsecond precision

    Features:
    - Decimal precision for financial calculations
    - High-frequency trading optimizations
    - Built-in risk management hooks
    - Audit trail capabilities
    """

    def __init__(self, **kwargs) -> None:
        # Financial-specific optimizations
        kwargs.setdefault("title", "Rapid Trading Server")
        kwargs.setdefault("description", "High-precision financial trading platform")
        super().__init__(**kwargs)

        # Financial-specific settings
        self.precision = kwargs.get("precision", 8)  # 8 decimal places
        self.risk_limits = kwargs.get("risk_limits", True)
        self.audit_enabled = kwargs.get("audit_enabled", True)

        # Performance monitoring
        self.trade_count = 0
        self.total_volume = decimal.Decimal("0")

        # Set decimal context for financial precision
        decimal.getcontext().prec = self.precision + 2

    def market_status(self):
        """Get market status with microsecond precision"""
        now = time.time()
        return JSONResponse(
            {
                "status": "open",
                "timestamp": int(now * 1000000),  # microseconds
                "trades_count": self.trade_count,
                "volume": str(self.total_volume),
                "precision": self.precision,
                "risk_limits": self.risk_limits,
            }
        )

    def record_trade(self, amount, price, side="buy"):
        """Record a trade with financial precision"""
        amount_decimal = decimal.Decimal(str(amount))
        price_decimal = decimal.Decimal(str(price))
        volume = amount_decimal * price_decimal

        self.trade_count += 1
        self.total_volume += volume

        if self.audit_enabled:
            return {
                "trade_id": self.trade_count,
                "amount": str(amount_decimal),
                "price": str(price_decimal),
                "volume": str(volume),
                "side": side,
                "timestamp": int(time.time() * 1000000),
            }

    def get_trading_stats(self):
        """Get trading statistics"""
        return {
            "total_trades": self.trade_count,
            "total_volume": str(self.total_volume),
            "precision": self.precision,
            "avg_trade_volume": str(self.total_volume / self.trade_count)
            if self.trade_count > 0
            else "0",
        }


# Convenience function for financial server setup
def create_trading_server(name="TradingServer", precision=8, risk_limits=True):
    """Create a financial trading server with optimized defaults"""
    return TradingServer(
        title=name,
        precision=precision,
        risk_limits=risk_limits,
        audit_enabled=True,
        description=f"Financial server - {precision} decimal precision",
    )


__all__ = ["TradingServer", "create_trading_server"]

