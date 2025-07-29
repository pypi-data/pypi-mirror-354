"""
Strategy Statistics Container

Holds all statistical data for a single strategy including:
- Real-time metrics
- Historical performance data
- Trade records
- Position tracking
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class TradeRecord:
    """Record of a single trade execution"""
    timestamp: datetime
    symbol: str
    action: str  # 'BUY', 'SELL', 'CLOSE'
    quantity: float
    price: float
    total_amount: float
    signal_confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging/serialization"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'symbol': self.symbol,
            'action': self.action,
            'quantity': self.quantity,
            'price': self.price,
            'total_amount': self.total_amount,
            'signal_confidence': self.signal_confidence
        }

@dataclass
class PositionSnapshot:
    """Snapshot of a position at a point in time"""
    timestamp: datetime
    symbol: str
    quantity: float
    avg_cost: float
    current_price: float
    unrealized_pnl: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging/serialization"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'symbol': self.symbol,
            'quantity': self.quantity,
            'avg_cost': self.avg_cost,
            'current_price': self.current_price,
            'unrealized_pnl': self.unrealized_pnl
        }

class StrategyStats:
    """
    Statistics container for a single strategy
    
    Tracks all performance metrics, trade history, and real-time statistics
    for an individual strategy running in the system.
    """
    
    def __init__(self, strategy_id: str, initial_capital: float = 0.0):
        """
        Initialize strategy statistics
        
        Args:
            strategy_id: Unique identifier for the strategy
            initial_capital: Initial capital allocated to this strategy
        """
        self.strategy_id = strategy_id
        self.initial_capital = initial_capital
        self.start_time = datetime.now()
        
        # Core metrics
        self.total_pnl = 0.0
        self.realized_pnl = 0.0
        self.unrealized_pnl = 0.0
        self.max_drawdown = 0.0
        self.current_drawdown = 0.0
        self.peak_portfolio_value = initial_capital
        self.current_portfolio_value = initial_capital
        
        # Trade tracking
        self.trade_records: List[TradeRecord] = []
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.break_even_trades = 0
        
        # Position tracking
        self.current_positions: Dict[str, PositionSnapshot] = {}
        self.position_history: List[PositionSnapshot] = []
        
        # Signal tracking
        self.total_signals = 0
        self.executed_signals = 0
        self.rejected_signals = 0
        
        # Time-series data for live tracking
        self.pnl_history: List[Dict[str, Any]] = []
        self.drawdown_history: List[Dict[str, Any]] = []
        self.portfolio_value_history: List[Dict[str, Any]] = []
        
        # Custom metrics (extensible)
        self.custom_metrics: Dict[str, Any] = {}
        
        logger.debug(f"Initialized statistics for strategy {strategy_id} with ${initial_capital:,.2f} capital")
    
    def record_trade(self, timestamp: datetime, symbol: str, action: str,
                    quantity: float, price: float, total_amount: float,
                    signal_confidence: float = 0.0):
        """
        Record a trade execution
        
        Args:
            timestamp: When the trade occurred
            symbol: Symbol traded
            action: 'BUY', 'SELL', or 'CLOSE'
            quantity: Quantity traded
            price: Price per unit
            total_amount: Total dollar amount
            signal_confidence: Confidence of the signal that triggered this trade
        """
        trade = TradeRecord(
            timestamp=timestamp,
            symbol=symbol,
            action=action,
            quantity=quantity,
            price=price,
            total_amount=total_amount,
            signal_confidence=signal_confidence
        )
        
        self.trade_records.append(trade)
        self.total_trades += 1
        
        logger.debug(f"Strategy {self.strategy_id}: Recorded {action} trade for {symbol}: "
                    f"{quantity} @ ${price:.2f} (total: ${total_amount:.2f})")
    
    def update_position(self, symbol: str, quantity: float, avg_cost: float, 
                       current_price: float, timestamp: Optional[datetime] = None):
        """
        Update position information for a symbol
        
        Args:
            symbol: Symbol to update
            quantity: Current quantity held
            avg_cost: Average cost basis
            current_price: Current market price
            timestamp: When this update occurred
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        unrealized_pnl = (current_price - avg_cost) * quantity if quantity > 0 else 0.0
        
        position = PositionSnapshot(
            timestamp=timestamp,
            symbol=symbol,
            quantity=quantity,
            avg_cost=avg_cost,
            current_price=current_price,
            unrealized_pnl=unrealized_pnl
        )
        
        self.current_positions[symbol] = position
        self.position_history.append(position)
        
        # Update unrealized P&L
        self.unrealized_pnl = sum(pos.unrealized_pnl for pos in self.current_positions.values())
        
        logger.debug(f"Strategy {self.strategy_id}: Updated position {symbol}: "
                    f"{quantity} @ ${avg_cost:.2f} (current: ${current_price:.2f}, P&L: ${unrealized_pnl:.2f})")
    
    def update_pnl(self, realized_pnl_change: float = 0.0, timestamp: Optional[datetime] = None):
        """
        Update P&L metrics
        
        Args:
            realized_pnl_change: Change in realized P&L (from closed trades)
            timestamp: When this update occurred
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Update realized P&L
        self.realized_pnl += realized_pnl_change
        
        # Total P&L = realized + unrealized
        self.total_pnl = self.realized_pnl + self.unrealized_pnl
        
        # Update portfolio value
        self.current_portfolio_value = self.initial_capital + self.total_pnl
        
        # Track peak and drawdown
        if self.current_portfolio_value > self.peak_portfolio_value:
            self.peak_portfolio_value = self.current_portfolio_value
            self.current_drawdown = 0.0
        else:
            self.current_drawdown = (self.peak_portfolio_value - self.current_portfolio_value) / self.peak_portfolio_value
            self.max_drawdown = max(self.max_drawdown, self.current_drawdown)
        
        # Record time-series data
        self.pnl_history.append({
            'timestamp': timestamp.isoformat(),
            'total_pnl': self.total_pnl,
            'realized_pnl': self.realized_pnl,
            'unrealized_pnl': self.unrealized_pnl
        })
        
        self.drawdown_history.append({
            'timestamp': timestamp.isoformat(),
            'current_drawdown': self.current_drawdown,
            'max_drawdown': self.max_drawdown
        })
        
        self.portfolio_value_history.append({
            'timestamp': timestamp.isoformat(),
            'portfolio_value': self.current_portfolio_value,
            'peak_value': self.peak_portfolio_value
        })
        
        logger.debug(f"Strategy {self.strategy_id}: P&L updated - Total: ${self.total_pnl:.2f}, "
                    f"Drawdown: {self.current_drawdown:.2%}, Max DD: {self.max_drawdown:.2%}")
    
    def record_signal(self, executed: bool = True):
        """
        Record a signal generation
        
        Args:
            executed: Whether the signal was executed or rejected
        """
        self.total_signals += 1
        if executed:
            self.executed_signals += 1
        else:
            self.rejected_signals += 1
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive performance summary
        
        Returns:
            Dictionary with all key performance metrics
        """
        runtime = datetime.now() - self.start_time
        
        win_rate = self.winning_trades / max(self.total_trades, 1) * 100
        signal_execution_rate = self.executed_signals / max(self.total_signals, 1) * 100
        total_return = (self.current_portfolio_value - self.initial_capital) / self.initial_capital * 100
        
        return {
            'strategy_id': self.strategy_id,
            'runtime_seconds': runtime.total_seconds(),
            'initial_capital': self.initial_capital,
            'current_portfolio_value': self.current_portfolio_value,
            'total_pnl': self.total_pnl,
            'realized_pnl': self.realized_pnl,
            'unrealized_pnl': self.unrealized_pnl,
            'total_return_pct': total_return,
            'max_drawdown_pct': self.max_drawdown * 100,
            'current_drawdown_pct': self.current_drawdown * 100,
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'win_rate_pct': win_rate,
            'total_signals': self.total_signals,
            'executed_signals': self.executed_signals,
            'rejected_signals': self.rejected_signals,
            'signal_execution_rate_pct': signal_execution_rate,
            'active_positions': len(self.current_positions),
            'custom_metrics': self.custom_metrics
        }
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """
        Get current real-time metrics for live display
        
        Returns:
            Dictionary with current key metrics
        """
        return {
            'pnl': self.total_pnl,
            'realized_pnl': self.realized_pnl,
            'unrealized_pnl': self.unrealized_pnl,
            'max_drawdown_pct': self.max_drawdown * 100,
            'current_drawdown_pct': self.current_drawdown * 100,
            'portfolio_value': self.current_portfolio_value,
            'total_trades': self.total_trades,
            'total_signals': self.total_signals,
            'active_positions': len(self.current_positions)
        }
    
    def add_custom_metric(self, name: str, value: Any):
        """
        Add a custom metric for this strategy
        
        Args:
            name: Metric name
            value: Metric value
        """
        self.custom_metrics[name] = value
        logger.debug(f"Strategy {self.strategy_id}: Added custom metric {name} = {value}") 