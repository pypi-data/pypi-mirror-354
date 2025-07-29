"""
Trade Statistics Module

Tracks trade-related metrics including:
- Win/loss ratios
- Trade frequency
- Average trade duration
- Best/worst trades
- Trade distribution analysis
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from ..stats_tracker import StatModule
from ..strategy_stats import StrategyStats, TradeRecord, PositionSnapshot

logger = logging.getLogger(__name__)

class TradeModule(StatModule):
    """
    Trade statistics module
    
    Provides comprehensive trade analysis including win/loss ratios,
    trade frequency, duration analysis, and performance distribution.
    """
    
    def __init__(self):
        super().__init__("trade")
        
        # Trade categorization
        self.winning_trades: List[TradeRecord] = []
        self.losing_trades: List[TradeRecord] = []
        self.break_even_trades: List[TradeRecord] = []
        
        # Trade timing
        self.trade_durations: List[timedelta] = []
        self.open_positions: Dict[str, datetime] = {}  # symbol -> entry timestamp
        
        # Performance metrics
        self.largest_win = 0.0
        self.largest_loss = 0.0
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.max_consecutive_wins = 0
        self.max_consecutive_losses = 0
        self.current_streak_type = None  # 'win', 'loss', or None
        
        # Frequency analysis
        self.trades_by_symbol: Dict[str, int] = defaultdict(int)
        self.trades_by_hour: Dict[int, int] = defaultdict(int)
        self.trades_by_day: Dict[str, int] = defaultdict(int)
        
        # Trade size analysis
        self.trade_sizes: List[float] = []
        self.avg_trade_size = 0.0
        
        logger.debug("Initialized Trade statistics module")
    
    def process_trade(self, stats: StrategyStats, trade: TradeRecord) -> None:
        """
        Process a trade for trade statistics
        
        Args:
            stats: Strategy statistics container
            trade: Trade record to process
        """
        # Track trade frequency by symbol, time
        self.trades_by_symbol[trade.symbol] += 1
        self.trades_by_hour[trade.timestamp.hour] += 1
        self.trades_by_day[trade.timestamp.strftime('%A')] += 1
        
        # Track trade size
        self.trade_sizes.append(trade.total_amount)
        self.avg_trade_size = sum(self.trade_sizes) / len(self.trade_sizes)
        
        # Handle buy trades (position opening)
        if trade.action == 'BUY':
            self.open_positions[trade.symbol] = trade.timestamp
            logger.debug(f"Trade Module: Opened position for {trade.symbol}")
        
        # Handle sell/close trades (position closing)
        elif trade.action in ['SELL', 'CLOSE']:
            # Calculate trade duration if we have the entry
            if trade.symbol in self.open_positions:
                entry_time = self.open_positions[trade.symbol]
                duration = trade.timestamp - entry_time
                self.trade_durations.append(duration)
                del self.open_positions[trade.symbol]
                
                logger.debug(f"Trade Module: Closed position for {trade.symbol}, "
                           f"Duration: {duration.total_seconds():.0f} seconds")
            
            # Estimate trade P&L for categorization
            trade_pnl = self._estimate_trade_pnl(trade, stats)
            
            # Categorize trade by P&L
            if trade_pnl > 0.01:  # Small threshold for numerical precision
                self.winning_trades.append(trade)
                self._update_winning_streak()
                self.largest_win = max(self.largest_win, trade_pnl)
                stats.winning_trades += 1
            elif trade_pnl < -0.01:
                self.losing_trades.append(trade)
                self._update_losing_streak()
                self.largest_loss = min(self.largest_loss, trade_pnl)
                stats.losing_trades += 1
            else:
                self.break_even_trades.append(trade)
                self._reset_streak()
                stats.break_even_trades += 1
    
    def process_position_update(self, stats: StrategyStats, position: PositionSnapshot) -> None:
        """
        Process a position update for trade statistics
        
        Args:
            stats: Strategy statistics container
            position: Position snapshot to process
        """
        # Trade module primarily focuses on completed trades
        # Position updates don't require special handling here
        pass
    
    def _estimate_trade_pnl(self, trade: TradeRecord, stats: StrategyStats) -> float:
        """
        Estimate P&L for a trade (simplified calculation)
        
        Args:
            trade: Trade record
            stats: Strategy statistics
            
        Returns:
            Estimated P&L for the trade
        """
        # Simple estimation - in practice this would need more sophisticated tracking
        current_position = stats.current_positions.get(trade.symbol)
        if current_position and trade.action in ['SELL', 'CLOSE']:
            return (trade.price - current_position.avg_cost) * trade.quantity
        return 0.0
    
    def _update_winning_streak(self) -> None:
        """Update winning streak counters"""
        if self.current_streak_type == 'win':
            self.consecutive_wins += 1
        else:
            self.consecutive_wins = 1
            self.consecutive_losses = 0
            self.current_streak_type = 'win'
        
        self.max_consecutive_wins = max(self.max_consecutive_wins, self.consecutive_wins)
    
    def _update_losing_streak(self) -> None:
        """Update losing streak counters"""
        if self.current_streak_type == 'loss':
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 1
            self.consecutive_wins = 0
            self.current_streak_type = 'loss'
        
        self.max_consecutive_losses = max(self.max_consecutive_losses, self.consecutive_losses)
    
    def _reset_streak(self) -> None:
        """Reset streak counters for break-even trades"""
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.current_streak_type = None
    
    def calculate_metrics(self, stats: StrategyStats) -> Dict[str, Any]:
        """
        Calculate comprehensive trade metrics
        
        Args:
            stats: Strategy statistics container
            
        Returns:
            Dictionary of trade metrics
        """
        total_closed_trades = len(self.winning_trades) + len(self.losing_trades) + len(self.break_even_trades)
        
        # Win/Loss ratios
        win_rate = 0.0
        loss_rate = 0.0
        if total_closed_trades > 0:
            win_rate = len(self.winning_trades) / total_closed_trades * 100
            loss_rate = len(self.losing_trades) / total_closed_trades * 100
        
        # Trade duration analysis
        avg_duration_seconds = 0.0
        min_duration_seconds = 0.0
        max_duration_seconds = 0.0
        if self.trade_durations:
            avg_duration_seconds = sum(d.total_seconds() for d in self.trade_durations) / len(self.trade_durations)
            min_duration_seconds = min(d.total_seconds() for d in self.trade_durations)
            max_duration_seconds = max(d.total_seconds() for d in self.trade_durations)
        
        # Trading frequency
        total_runtime = datetime.now() - stats.start_time
        trades_per_hour = 0.0
        if total_runtime.total_seconds() > 0:
            trades_per_hour = len(stats.trade_records) / (total_runtime.total_seconds() / 3600)
        
        # Most active periods
        most_active_hour = max(self.trades_by_hour.items(), key=lambda x: x[1])[0] if self.trades_by_hour else None
        most_active_day = max(self.trades_by_day.items(), key=lambda x: x[1])[0] if self.trades_by_day else None
        most_traded_symbol = max(self.trades_by_symbol.items(), key=lambda x: x[1])[0] if self.trades_by_symbol else None
        
        # Risk metrics
        risk_reward_ratio = 0.0
        if self.largest_loss < 0:
            risk_reward_ratio = self.largest_win / abs(self.largest_loss)
        
        # Expectancy (average win * win rate - average loss * loss rate)
        avg_win = sum(self._estimate_trade_pnl(t, stats) for t in self.winning_trades) / max(len(self.winning_trades), 1)
        avg_loss = sum(self._estimate_trade_pnl(t, stats) for t in self.losing_trades) / max(len(self.losing_trades), 1)
        expectancy = (avg_win * win_rate / 100) + (avg_loss * loss_rate / 100)
        
        return {
            'total_trades': len(stats.trade_records),
            'total_closed_trades': total_closed_trades,
            'winning_trades': len(self.winning_trades),
            'losing_trades': len(self.losing_trades),
            'break_even_trades': len(self.break_even_trades),
            'win_rate_pct': win_rate,
            'loss_rate_pct': loss_rate,
            'largest_win': self.largest_win,
            'largest_loss': self.largest_loss,
            'average_win': avg_win,
            'average_loss': avg_loss,
            'risk_reward_ratio': risk_reward_ratio,
            'expectancy': expectancy,
            'consecutive_wins': self.consecutive_wins,
            'consecutive_losses': self.consecutive_losses,
            'max_consecutive_wins': self.max_consecutive_wins,
            'max_consecutive_losses': self.max_consecutive_losses,
            'current_streak_type': self.current_streak_type,
            'average_trade_duration_seconds': avg_duration_seconds,
            'average_trade_duration_minutes': avg_duration_seconds / 60,
            'min_trade_duration_seconds': min_duration_seconds,
            'max_trade_duration_seconds': max_duration_seconds,
            'trades_per_hour': trades_per_hour,
            'average_trade_size': self.avg_trade_size,
            'most_active_hour': most_active_hour,
            'most_active_day': most_active_day,
            'most_traded_symbol': most_traded_symbol,
            'open_positions_count': len(self.open_positions),
            'completed_durations_count': len(self.trade_durations),
            'trades_by_symbol': dict(self.trades_by_symbol),
            'trades_by_hour': dict(self.trades_by_hour),
            'trades_by_day': dict(self.trades_by_day)
        }
    
    def get_trade_distribution(self) -> Dict[str, Any]:
        """
        Get detailed trade distribution analysis
        
        Returns:
            Dictionary with trade distribution data
        """
        return {
            'winning_trades_details': [
                {
                    'symbol': t.symbol,
                    'timestamp': t.timestamp.isoformat(),
                    'price': t.price,
                    'amount': t.total_amount,
                    'confidence': t.signal_confidence
                }
                for t in self.winning_trades
            ],
            'losing_trades_details': [
                {
                    'symbol': t.symbol,
                    'timestamp': t.timestamp.isoformat(),
                    'price': t.price,
                    'amount': t.total_amount,
                    'confidence': t.signal_confidence
                }
                for t in self.losing_trades
            ],
            'trade_durations': [d.total_seconds() for d in self.trade_durations],
            'trade_sizes': self.trade_sizes,
            'frequency_analysis': {
                'by_symbol': dict(self.trades_by_symbol),
                'by_hour': dict(self.trades_by_hour),
                'by_day': dict(self.trades_by_day)
            }
        }
    
    def reset(self) -> None:
        """Reset trade module state"""
        self.winning_trades.clear()
        self.losing_trades.clear()
        self.break_even_trades.clear()
        self.trade_durations.clear()
        self.open_positions.clear()
        self.largest_win = 0.0
        self.largest_loss = 0.0
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.max_consecutive_wins = 0
        self.max_consecutive_losses = 0
        self.current_streak_type = None
        self.trades_by_symbol.clear()
        self.trades_by_hour.clear()
        self.trades_by_day.clear()
        self.trade_sizes.clear()
        self.avg_trade_size = 0.0
        
        logger.debug("Reset Trade module state") 