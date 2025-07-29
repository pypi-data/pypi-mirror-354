"""
Drawdown Statistics Module

Tracks drawdown metrics including:
- Maximum drawdown
- Current drawdown 
- Drawdown duration
- Recovery periods
- Underwater curve analysis
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from ..stats_tracker import StatModule
from ..strategy_stats import StrategyStats, TradeRecord, PositionSnapshot

logger = logging.getLogger(__name__)

class DrawdownModule(StatModule):
    """
    Drawdown statistics module
    
    Provides comprehensive drawdown analysis including maximum drawdown,
    drawdown duration, recovery periods, and underwater curve tracking.
    """
    
    def __init__(self):
        super().__init__("drawdown")
        
        # Drawdown tracking
        self.peak_value = 0.0
        self.peak_timestamp: Optional[datetime] = None
        self.max_drawdown_value = 0.0
        self.max_drawdown_pct = 0.0
        self.max_drawdown_start: Optional[datetime] = None
        self.max_drawdown_end: Optional[datetime] = None
        self.current_drawdown_start: Optional[datetime] = None
        
        # Drawdown periods
        self.drawdown_periods: List[Dict[str, Any]] = []
        self.current_in_drawdown = False
        
        # Recovery tracking
        self.total_recovery_time = timedelta(0)
        self.longest_recovery_time = timedelta(0)
        self.num_recoveries = 0
        
        # Underwater curve (time series of drawdown values)
        self.underwater_curve: List[Dict[str, Any]] = []
        
        logger.debug("Initialized Drawdown statistics module")
    
    def process_trade(self, stats: StrategyStats, trade: TradeRecord) -> None:
        """
        Process a trade for drawdown calculation
        
        Args:
            stats: Strategy statistics container
            trade: Trade record to process
        """
        # Update drawdown based on new portfolio value
        self._update_drawdown(stats.current_portfolio_value, trade.timestamp)
    
    def process_position_update(self, stats: StrategyStats, position: PositionSnapshot) -> None:
        """
        Process a position update for drawdown calculation
        
        Args:
            stats: Strategy statistics container
            position: Position snapshot to process
        """
        # Update drawdown based on current portfolio value
        self._update_drawdown(stats.current_portfolio_value, position.timestamp)
    
    def _update_drawdown(self, current_value: float, timestamp: datetime) -> None:
        """
        Update drawdown calculations
        
        Args:
            current_value: Current portfolio value
            timestamp: Timestamp of the update
        """
        # Initialize peak if not set
        if self.peak_value == 0.0:
            self.peak_value = current_value
            self.peak_timestamp = timestamp
        
        # Check for new peak
        if current_value > self.peak_value:
            # New peak reached
            if self.current_in_drawdown:
                # End current drawdown period
                self._end_drawdown_period(timestamp)
            
            self.peak_value = current_value
            self.peak_timestamp = timestamp
            current_drawdown_pct = 0.0
            current_drawdown_value = 0.0
        else:
            # Calculate current drawdown
            current_drawdown_value = self.peak_value - current_value
            current_drawdown_pct = current_drawdown_value / self.peak_value
            
            # Check if this is a new maximum drawdown
            if current_drawdown_pct > self.max_drawdown_pct:
                self.max_drawdown_pct = current_drawdown_pct
                self.max_drawdown_value = current_drawdown_value
                self.max_drawdown_start = self.peak_timestamp
                self.max_drawdown_end = timestamp
            
            # Check if we're entering a new drawdown period
            if not self.current_in_drawdown and current_drawdown_pct > 0.01:  # 1% threshold
                self.current_in_drawdown = True
                self.current_drawdown_start = self.peak_timestamp
        
        # Record underwater curve point
        underwater_point = {
            'timestamp': timestamp.isoformat(),
            'portfolio_value': current_value,
            'peak_value': self.peak_value,
            'drawdown_value': current_drawdown_value,
            'drawdown_pct': current_drawdown_pct,
            'in_drawdown': self.current_in_drawdown
        }
        self.underwater_curve.append(underwater_point)
        
        logger.debug(f"Drawdown Module: Updated - Current DD: {current_drawdown_pct:.2%}, "
                    f"Max DD: {self.max_drawdown_pct:.2%}")
    
    def _end_drawdown_period(self, recovery_timestamp: datetime) -> None:
        """
        End the current drawdown period and record recovery
        
        Args:
            recovery_timestamp: When the recovery occurred
        """
        if self.current_drawdown_start and self.current_in_drawdown:
            # Calculate drawdown duration
            drawdown_duration = recovery_timestamp - self.current_drawdown_start
            
            # Record drawdown period
            drawdown_period = {
                'start_timestamp': self.current_drawdown_start.isoformat(),
                'end_timestamp': recovery_timestamp.isoformat(),
                'duration_seconds': drawdown_duration.total_seconds(),
                'duration_days': drawdown_duration.days,
                'max_drawdown_in_period': self.max_drawdown_pct,
                'recovery_timestamp': recovery_timestamp.isoformat()
            }
            
            self.drawdown_periods.append(drawdown_period)
            
            # Update recovery statistics
            self.total_recovery_time += drawdown_duration
            self.longest_recovery_time = max(self.longest_recovery_time, drawdown_duration)
            self.num_recoveries += 1
            
            # Reset drawdown state
            self.current_in_drawdown = False
            self.current_drawdown_start = None
            
            logger.info(f"Drawdown Module: Recovery completed in {drawdown_duration.days} days")
    
    def calculate_metrics(self, stats: StrategyStats) -> Dict[str, Any]:
        """
        Calculate comprehensive drawdown metrics
        
        Args:
            stats: Strategy statistics container
            
        Returns:
            Dictionary of drawdown metrics
        """
        # Current drawdown
        current_drawdown_value = 0.0
        current_drawdown_pct = 0.0
        current_drawdown_duration_days = 0
        
        if self.current_in_drawdown and self.current_drawdown_start:
            current_drawdown_value = self.peak_value - stats.current_portfolio_value
            current_drawdown_pct = current_drawdown_value / self.peak_value
            current_drawdown_duration = datetime.now() - self.current_drawdown_start
            current_drawdown_duration_days = current_drawdown_duration.days
        
        # Average recovery time
        avg_recovery_days = 0.0
        if self.num_recoveries > 0:
            avg_recovery_days = self.total_recovery_time.total_seconds() / (self.num_recoveries * 24 * 3600)
        
        # Maximum drawdown duration
        max_dd_duration_days = 0
        if self.max_drawdown_start and self.max_drawdown_end:
            max_dd_duration = self.max_drawdown_end - self.max_drawdown_start
            max_dd_duration_days = max_dd_duration.days
        
        # Calmar ratio (annual return / max drawdown)
        calmar_ratio = 0.0
        if self.max_drawdown_pct > 0 and stats.initial_capital > 0:
            # Estimate annualized return
            runtime = datetime.now() - stats.start_time
            if runtime.total_seconds() > 0:
                annual_return = (stats.total_pnl / stats.initial_capital) * (365.25 * 24 * 3600 / runtime.total_seconds())
                calmar_ratio = annual_return / self.max_drawdown_pct
        
        # Time in drawdown percentage
        total_runtime = datetime.now() - stats.start_time
        time_in_drawdown_pct = 0.0
        if total_runtime.total_seconds() > 0:
            total_drawdown_time = sum(
                (datetime.fromisoformat(period['end_timestamp']) - 
                 datetime.fromisoformat(period['start_timestamp'])).total_seconds()
                for period in self.drawdown_periods
            )
            # Add current drawdown time if in drawdown
            if self.current_in_drawdown and self.current_drawdown_start:
                total_drawdown_time += (datetime.now() - self.current_drawdown_start).total_seconds()
            
            time_in_drawdown_pct = (total_drawdown_time / total_runtime.total_seconds()) * 100
        
        return {
            'max_drawdown_pct': self.max_drawdown_pct * 100,
            'max_drawdown_value': self.max_drawdown_value,
            'max_drawdown_start': self.max_drawdown_start.isoformat() if self.max_drawdown_start else None,
            'max_drawdown_end': self.max_drawdown_end.isoformat() if self.max_drawdown_end else None,
            'max_drawdown_duration_days': max_dd_duration_days,
            'current_drawdown_pct': current_drawdown_pct * 100,
            'current_drawdown_value': current_drawdown_value,
            'current_drawdown_duration_days': current_drawdown_duration_days,
            'in_drawdown': self.current_in_drawdown,
            'peak_portfolio_value': self.peak_value,
            'peak_timestamp': self.peak_timestamp.isoformat() if self.peak_timestamp else None,
            'total_drawdown_periods': len(self.drawdown_periods),
            'total_recoveries': self.num_recoveries,
            'average_recovery_days': avg_recovery_days,
            'longest_recovery_days': self.longest_recovery_time.days,
            'time_in_drawdown_pct': time_in_drawdown_pct,
            'calmar_ratio': calmar_ratio,
            'underwater_curve_points': len(self.underwater_curve)
        }
    
    def get_underwater_curve(self) -> List[Dict[str, Any]]:
        """
        Get the underwater curve data
        
        Returns:
            List of underwater curve data points
        """
        return self.underwater_curve.copy()
    
    def get_drawdown_periods(self) -> List[Dict[str, Any]]:
        """
        Get all completed drawdown periods
        
        Returns:
            List of drawdown period data
        """
        return self.drawdown_periods.copy()
    
    def reset(self) -> None:
        """Reset drawdown module state"""
        self.peak_value = 0.0
        self.peak_timestamp = None
        self.max_drawdown_value = 0.0
        self.max_drawdown_pct = 0.0
        self.max_drawdown_start = None
        self.max_drawdown_end = None
        self.current_drawdown_start = None
        self.drawdown_periods.clear()
        self.current_in_drawdown = False
        self.total_recovery_time = timedelta(0)
        self.longest_recovery_time = timedelta(0)
        self.num_recoveries = 0
        self.underwater_curve.clear()
        
        logger.debug("Reset Drawdown module state") 