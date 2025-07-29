"""
Built-in Statistics Modules

This package contains pre-built statistics modules for common metrics:
- PnLModule: Profit & Loss tracking
- DrawdownModule: Drawdown calculation and tracking  
- TradeModule: Trade performance analysis
"""

from .pnl_module import PnLModule
from .drawdown_module import DrawdownModule
from .trade_module import TradeModule

__all__ = [
    'PnLModule',
    'DrawdownModule', 
    'TradeModule'
] 