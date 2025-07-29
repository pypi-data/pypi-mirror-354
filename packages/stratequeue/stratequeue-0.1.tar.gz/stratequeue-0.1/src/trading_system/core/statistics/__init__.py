"""
Strategy Statistics Tracking Package

A modular system for tracking strategy performance metrics including:
- Profit & Loss (PnL)
- Maximum Drawdown
- Trade statistics
- Position tracking
- Performance analytics

Public API:
    StrategyStats: Individual strategy statistics container
    StatsTracker: Statistics calculation engine
    StatsManager: Multi-strategy statistics coordinator
    StatModule: Base class for pluggable statistics modules
"""

from .strategy_stats import StrategyStats
from .stats_tracker import StatsTracker, StatModule
from .stats_manager import StatsManager
from .modules import PnLModule, DrawdownModule, TradeModule

__all__ = [
    'StrategyStats',
    'StatsTracker', 
    'StatModule',
    'StatsManager',
    'PnLModule',
    'DrawdownModule',
    'TradeModule'
] 