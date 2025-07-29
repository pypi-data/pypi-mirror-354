"""
Profit & Loss Statistics Module

Tracks detailed P&L metrics including:
- Realized and unrealized P&L
- Trade-by-trade P&L
- Position-level P&L
- Return calculations
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

from ..stats_tracker import StatModule
from ..strategy_stats import StrategyStats, TradeRecord, PositionSnapshot

logger = logging.getLogger(__name__)

class PnLModule(StatModule):
    """
    Profit & Loss statistics module
    
    Provides detailed P&L tracking and analysis including trade-level
    and position-level profit/loss calculations.
    """
    
    def __init__(self):
        super().__init__("pnl")
        
        # Trade P&L tracking
        self.trade_pnl_history: List[Dict[str, Any]] = []
        self.position_pnl_history: List[Dict[str, Any]] = []
        
        # P&L by symbol
        self.symbol_pnl: Dict[str, float] = {}
        self.symbol_realized_pnl: Dict[str, float] = {}
        self.symbol_unrealized_pnl: Dict[str, float] = {}
        
        # Performance ratios
        self.best_trade_pnl = 0.0
        self.worst_trade_pnl = 0.0
        self.avg_trade_pnl = 0.0
        
        logger.debug("Initialized P&L statistics module")
    
    def process_trade(self, stats: StrategyStats, trade: TradeRecord) -> None:
        """
        Process a trade for P&L calculation
        
        Args:
            stats: Strategy statistics container
            trade: Trade record to process
        """
        # Calculate trade P&L (simplified - assumes this is the realized P&L for the trade)
        trade_pnl = self._calculate_trade_pnl(trade, stats)
        
        # Update symbol-specific P&L
        if trade.symbol not in self.symbol_pnl:
            self.symbol_pnl[trade.symbol] = 0.0
            self.symbol_realized_pnl[trade.symbol] = 0.0
            self.symbol_unrealized_pnl[trade.symbol] = 0.0
        
        # For sell trades, this represents realized P&L
        if trade.action in ['SELL', 'CLOSE']:
            self.symbol_realized_pnl[trade.symbol] += trade_pnl
            
            # Update realized P&L in main stats
            stats.update_pnl(realized_pnl_change=trade_pnl, timestamp=trade.timestamp)
            
            # Track best/worst trades
            self.best_trade_pnl = max(self.best_trade_pnl, trade_pnl)
            self.worst_trade_pnl = min(self.worst_trade_pnl, trade_pnl)
            
            # Update average trade P&L
            total_sell_trades = len([t for t in stats.trade_records if t.action in ['SELL', 'CLOSE']])
            if total_sell_trades > 0:
                total_realized = sum(self.symbol_realized_pnl.values())
                self.avg_trade_pnl = total_realized / total_sell_trades
        
        # Record trade P&L
        trade_pnl_record = {
            'timestamp': trade.timestamp.isoformat(),
            'symbol': trade.symbol,
            'action': trade.action,
            'trade_pnl': trade_pnl,
            'cumulative_realized_pnl': stats.realized_pnl,
            'total_pnl': stats.total_pnl
        }
        
        self.trade_pnl_history.append(trade_pnl_record)
        
        logger.debug(f"P&L Module: Processed {trade.action} trade for {trade.symbol}, "
                    f"Trade P&L: ${trade_pnl:.2f}, Total P&L: ${stats.total_pnl:.2f}")
    
    def process_position_update(self, stats: StrategyStats, position: PositionSnapshot) -> None:
        """
        Process a position update for unrealized P&L
        
        Args:
            stats: Strategy statistics container
            position: Position snapshot to process
        """
        # Update symbol unrealized P&L
        self.symbol_unrealized_pnl[position.symbol] = position.unrealized_pnl
        self.symbol_pnl[position.symbol] = (
            self.symbol_realized_pnl.get(position.symbol, 0.0) + position.unrealized_pnl
        )
        
        # Record position P&L snapshot
        position_pnl_record = {
            'timestamp': position.timestamp.isoformat(),
            'symbol': position.symbol,
            'unrealized_pnl': position.unrealized_pnl,
            'total_symbol_pnl': self.symbol_pnl[position.symbol],
            'total_unrealized_pnl': stats.unrealized_pnl
        }
        
        self.position_pnl_history.append(position_pnl_record)
        
        # Update main stats P&L (will recalculate total P&L)
        stats.update_pnl(timestamp=position.timestamp)
        
        logger.debug(f"P&L Module: Updated position for {position.symbol}, "
                    f"Unrealized P&L: ${position.unrealized_pnl:.2f}")
    
    def calculate_metrics(self, stats: StrategyStats) -> Dict[str, Any]:
        """
        Calculate comprehensive P&L metrics
        
        Args:
            stats: Strategy statistics container
            
        Returns:
            Dictionary of P&L metrics
        """
        # Basic P&L metrics
        total_return_pct = 0.0
        if stats.initial_capital > 0:
            total_return_pct = (stats.total_pnl / stats.initial_capital) * 100
        
        # Profitability metrics
        profitable_trades = len([pnl for pnl in self.trade_pnl_history 
                                if pnl.get('trade_pnl', 0) > 0])
        total_closed_trades = len([t for t in stats.trade_records 
                                  if t.action in ['SELL', 'CLOSE']])
        
        profitability_ratio = 0.0
        if total_closed_trades > 0:
            profitability_ratio = profitable_trades / total_closed_trades
        
        # Profit factor (gross profit / gross loss)
        gross_profit = sum(pnl['trade_pnl'] for pnl in self.trade_pnl_history 
                          if pnl.get('trade_pnl', 0) > 0)
        gross_loss = abs(sum(pnl['trade_pnl'] for pnl in self.trade_pnl_history 
                            if pnl.get('trade_pnl', 0) < 0))
        
        profit_factor = gross_profit / max(gross_loss, 0.01)  # Avoid division by zero
        
        # Return metrics by symbol
        symbol_returns = {}
        for symbol, pnl in self.symbol_pnl.items():
            # Estimate symbol allocation (simplified)
            symbol_allocation = stats.initial_capital / max(len(self.symbol_pnl), 1)
            symbol_return_pct = (pnl / symbol_allocation) * 100 if symbol_allocation > 0 else 0.0
            symbol_returns[symbol] = {
                'total_pnl': pnl,
                'realized_pnl': self.symbol_realized_pnl.get(symbol, 0.0),
                'unrealized_pnl': self.symbol_unrealized_pnl.get(symbol, 0.0),
                'return_pct': symbol_return_pct
            }
        
        return {
            'total_pnl': stats.total_pnl,
            'realized_pnl': stats.realized_pnl,
            'unrealized_pnl': stats.unrealized_pnl,
            'total_return_pct': total_return_pct,
            'best_trade_pnl': self.best_trade_pnl,
            'worst_trade_pnl': self.worst_trade_pnl,
            'average_trade_pnl': self.avg_trade_pnl,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            'profitable_trades': profitable_trades,
            'total_closed_trades': total_closed_trades,
            'profitability_ratio': profitability_ratio,
            'symbol_pnl': symbol_returns,
            'trade_pnl_count': len(self.trade_pnl_history),
            'position_updates_count': len(self.position_pnl_history)
        }
    
    def _calculate_trade_pnl(self, trade: TradeRecord, stats: StrategyStats) -> float:
        """
        Calculate P&L for a specific trade
        
        This is a simplified calculation. In a real system, you'd need to match
        buy/sell pairs and calculate based on cost basis.
        
        Args:
            trade: Trade record
            stats: Strategy statistics
            
        Returns:
            Estimated P&L for this trade
        """
        # For now, use a simple heuristic:
        # - Buy trades have negative impact (cost)
        # - Sell trades have positive impact (revenue)
        # This is simplified and should be enhanced with proper position tracking
        
        if trade.action == 'BUY':
            return -trade.total_amount  # Cost of purchase
        elif trade.action in ['SELL', 'CLOSE']:
            # For sell trades, estimate P&L based on position
            current_position = stats.current_positions.get(trade.symbol)
            if current_position:
                # Estimate P&L as difference from average cost
                return (trade.price - current_position.avg_cost) * trade.quantity
            else:
                return trade.total_amount  # Fallback: assume all revenue is profit
        else:
            return 0.0
    
    def reset(self) -> None:
        """Reset P&L module state"""
        self.trade_pnl_history.clear()
        self.position_pnl_history.clear()
        self.symbol_pnl.clear()
        self.symbol_realized_pnl.clear()
        self.symbol_unrealized_pnl.clear()
        self.best_trade_pnl = 0.0
        self.worst_trade_pnl = 0.0
        self.avg_trade_pnl = 0.0
        
        logger.debug("Reset P&L module state") 