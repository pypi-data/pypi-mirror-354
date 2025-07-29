"""
Statistics Tracker and Modular Statistics Framework

Provides a pluggable system for calculating strategy statistics:
- Base StatModule class for extensible statistics
- StatsTracker coordinates statistics calculation
- Built-in modules for common metrics
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Type
from datetime import datetime

from .strategy_stats import StrategyStats, TradeRecord, PositionSnapshot

logger = logging.getLogger(__name__)

class StatModule(ABC):
    """
    Base class for pluggable statistics modules
    
    Each module calculates specific metrics and can be easily added/removed
    from the statistics tracking system.
    """
    
    def __init__(self, name: str):
        """
        Initialize statistics module
        
        Args:
            name: Unique name for this module
        """
        self.name = name
        self.enabled = True
    
    @abstractmethod
    def process_trade(self, stats: StrategyStats, trade: TradeRecord) -> None:
        """
        Process a new trade record
        
        Args:
            stats: Strategy statistics container to update
            trade: Trade record to process
        """
        pass
    
    @abstractmethod
    def process_position_update(self, stats: StrategyStats, position: PositionSnapshot) -> None:
        """
        Process a position update
        
        Args:
            stats: Strategy statistics container to update
            position: Position snapshot to process
        """
        pass
    
    @abstractmethod
    def calculate_metrics(self, stats: StrategyStats) -> Dict[str, Any]:
        """
        Calculate and return metrics for this module
        
        Args:
            stats: Strategy statistics container
            
        Returns:
            Dictionary of calculated metrics
        """
        pass
    
    def reset(self) -> None:
        """Reset module state (optional override)"""
        pass
    
    def enable(self) -> None:
        """Enable this statistics module"""
        self.enabled = True
        logger.debug(f"Statistics module '{self.name}' enabled")
    
    def disable(self) -> None:
        """Disable this statistics module"""
        self.enabled = False
        logger.debug(f"Statistics module '{self.name}' disabled")

class StatsTracker:
    """
    Main statistics tracking engine
    
    Coordinates multiple statistics modules to provide comprehensive
    performance tracking for trading strategies.
    """
    
    def __init__(self, strategy_id: str, initial_capital: float = 0.0):
        """
        Initialize statistics tracker
        
        Args:
            strategy_id: Unique identifier for the strategy
            initial_capital: Initial capital allocated to this strategy
        """
        self.strategy_id = strategy_id
        self.stats = StrategyStats(strategy_id, initial_capital)
        
        # Registered statistics modules
        self.modules: Dict[str, StatModule] = {}
        self.module_order: List[str] = []
        
        logger.info(f"Initialized statistics tracker for strategy {strategy_id}")
    
    def register_module(self, module: StatModule) -> None:
        """
        Register a statistics module
        
        Args:
            module: Statistics module to register
        """
        if module.name in self.modules:
            logger.warning(f"Replacing existing statistics module: {module.name}")
        
        self.modules[module.name] = module
        if module.name not in self.module_order:
            self.module_order.append(module.name)
        
        logger.info(f"Registered statistics module: {module.name}")
    
    def unregister_module(self, module_name: str) -> None:
        """
        Unregister a statistics module
        
        Args:
            module_name: Name of module to unregister
        """
        if module_name in self.modules:
            del self.modules[module_name]
            if module_name in self.module_order:
                self.module_order.remove(module_name)
            logger.info(f"Unregistered statistics module: {module_name}")
        else:
            logger.warning(f"Attempted to unregister non-existent module: {module_name}")
    
    def get_module(self, module_name: str) -> Optional[StatModule]:
        """
        Get a registered module by name
        
        Args:
            module_name: Name of the module
            
        Returns:
            StatModule instance or None if not found
        """
        return self.modules.get(module_name)
    
    def enable_module(self, module_name: str) -> None:
        """
        Enable a statistics module
        
        Args:
            module_name: Name of module to enable
        """
        module = self.modules.get(module_name)
        if module:
            module.enable()
        else:
            logger.warning(f"Cannot enable non-existent module: {module_name}")
    
    def disable_module(self, module_name: str) -> None:
        """
        Disable a statistics module
        
        Args:
            module_name: Name of module to disable
        """
        module = self.modules.get(module_name)
        if module:
            module.disable()
        else:
            logger.warning(f"Cannot disable non-existent module: {module_name}")
    
    def record_trade(self, timestamp: datetime, symbol: str, action: str,
                    quantity: float, price: float, total_amount: float,
                    signal_confidence: float = 0.0) -> None:
        """
        Record a trade and update all statistics
        
        Args:
            timestamp: When the trade occurred
            symbol: Symbol traded
            action: 'BUY', 'SELL', or 'CLOSE'
            quantity: Quantity traded
            price: Price per unit
            total_amount: Total dollar amount
            signal_confidence: Confidence of the signal that triggered this trade
        """
        # Record in base statistics
        self.stats.record_trade(timestamp, symbol, action, quantity, total_amount, signal_confidence)
        
        # Get the latest trade record
        trade = self.stats.trade_records[-1]
        
        # Process through all enabled modules
        for module_name in self.module_order:
            module = self.modules[module_name]
            if module.enabled:
                try:
                    module.process_trade(self.stats, trade)
                except Exception as e:
                    logger.error(f"Error in statistics module {module_name}.process_trade: {e}")
        
        logger.debug(f"Processed trade through {len([m for m in self.modules.values() if m.enabled])} modules")
    
    def update_position(self, symbol: str, quantity: float, avg_cost: float,
                       current_price: float, timestamp: Optional[datetime] = None) -> None:
        """
        Update position and recalculate statistics
        
        Args:
            symbol: Symbol to update
            quantity: Current quantity held
            avg_cost: Average cost basis
            current_price: Current market price
            timestamp: When this update occurred
        """
        # Update base statistics
        self.stats.update_position(symbol, quantity, avg_cost, current_price, timestamp)
        
        # Get the latest position
        position = self.stats.current_positions[symbol]
        
        # Process through all enabled modules
        for module_name in self.module_order:
            module = self.modules[module_name]
            if module.enabled:
                try:
                    module.process_position_update(self.stats, position)
                except Exception as e:
                    logger.error(f"Error in statistics module {module_name}.process_position_update: {e}")
    
    def record_signal(self, executed: bool = True) -> None:
        """
        Record a signal generation
        
        Args:
            executed: Whether the signal was executed or rejected
        """
        self.stats.record_signal(executed)
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive metrics from all modules
        
        Returns:
            Dictionary with metrics from all enabled modules
        """
        all_metrics = {
            'strategy_id': self.strategy_id,
            'base_stats': self.stats.get_performance_summary()
        }
        
        # Collect metrics from all enabled modules
        for module_name in self.module_order:
            module = self.modules[module_name]
            if module.enabled:
                try:
                    module_metrics = module.calculate_metrics(self.stats)
                    all_metrics[f"{module_name}_metrics"] = module_metrics
                except Exception as e:
                    logger.error(f"Error calculating metrics in module {module_name}: {e}")
                    all_metrics[f"{module_name}_metrics"] = {"error": str(e)}
        
        return all_metrics
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """
        Get current real-time metrics for live display
        
        Returns:
            Dictionary with current key metrics from base stats
        """
        return self.stats.get_current_metrics()
    
    def get_detailed_summary(self) -> Dict[str, Any]:
        """
        Get detailed summary including trade and position history
        
        Returns:
            Comprehensive summary for logging/reporting
        """
        summary = self.get_all_metrics()
        
        # Add detailed trade history
        summary['trade_history'] = [trade.to_dict() for trade in self.stats.trade_records]
        
        # Add position history
        summary['position_history'] = [pos.to_dict() for pos in self.stats.position_history]
        
        # Add time-series data
        summary['time_series'] = {
            'pnl_history': self.stats.pnl_history,
            'drawdown_history': self.stats.drawdown_history,
            'portfolio_value_history': self.stats.portfolio_value_history
        }
        
        return summary
    
    def reset_statistics(self, keep_modules: bool = True) -> None:
        """
        Reset all statistics
        
        Args:
            keep_modules: Whether to keep registered modules (just reset their state)
        """
        initial_capital = self.stats.initial_capital
        self.stats = StrategyStats(self.strategy_id, initial_capital)
        
        if keep_modules:
            # Reset all modules
            for module in self.modules.values():
                module.reset()
        else:
            # Clear all modules
            self.modules.clear()
            self.module_order.clear()
        
        logger.info(f"Reset statistics for strategy {self.strategy_id}")
    
    def add_custom_metric(self, name: str, value: Any) -> None:
        """
        Add a custom metric to base statistics
        
        Args:
            name: Metric name
            value: Metric value
        """
        self.stats.add_custom_metric(name, value) 