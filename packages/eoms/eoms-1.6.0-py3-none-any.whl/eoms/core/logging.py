"""Structured JSON logging system for EOMS.

This module provides ELK/Grafana-compatible JSON logging with automatic log rotation
and production-ready configuration for systematic trading operations.
"""

import json
import logging
import logging.handlers
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

__all__ = ["setup_logging", "get_logger", "LogConfig", "EOSJSONFormatter"]


@dataclass
class LogConfig:
    """Configuration for EOMS logging system."""

    level: str = "INFO"
    log_dir: str = "logs"
    max_bytes: int = 50 * 1024 * 1024  # 50MB
    backup_count: int = 10
    console_output: bool = True
    json_format: bool = True
    service_name: str = "eoms"
    environment: str = "development"


class EOSJSONFormatter(logging.Formatter):
    """Custom JSON formatter for EOMS logs compatible with ELK/Grafana."""

    def __init__(self, service_name: str = "eoms", environment: str = "development"):
        super().__init__()
        self.service_name = service_name
        self.environment = environment

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON with standard fields."""
        # Base log structure
        log_entry = {
            "@timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": self.service_name,
            "environment": self.environment,
            "thread": record.thread,
            "thread_name": record.threadName,
            "process": record.process,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "filename": record.filename,
            "pathname": record.pathname,
        }

        # Add exception info if present
        if record.exc_info and record.exc_info != (None, None, None):
            # Handle both tuple and boolean exc_info values
            if isinstance(record.exc_info, tuple):
                exc_type, exc_value, exc_traceback = record.exc_info
                log_entry["exception"] = {
                    "type": exc_type.__name__ if exc_type else None,
                    "message": str(exc_value) if exc_value else None,
                    "traceback": (
                        self.formatException(record.exc_info) if record.exc_info else None
                    ),
                }
            elif record.exc_info is True:
                # Get current exception info
                import sys

                exc_info = sys.exc_info()
                if exc_info and exc_info[0]:
                    log_entry["exception"] = {
                        "type": exc_info[0].__name__,
                        "message": str(exc_info[1]) if exc_info[1] else None,
                        "traceback": self.formatException(exc_info),
                    }

        # Add custom fields from record
        if hasattr(record, "custom_fields"):
            log_entry.update(record.custom_fields)

        # Trading-specific fields if present
        trading_fields = {}
        for field in [
            "symbol",
            "order_id",
            "strategy_id",
            "account",
            "side",
            "quantity",
            "price",
            "pnl",
        ]:
            if hasattr(record, field):
                trading_fields[field] = getattr(record, field)

        if trading_fields:
            log_entry["trading"] = trading_fields

        # Performance fields if present
        perf_fields = {}
        for field in ["latency_ms", "throughput", "memory_mb", "cpu_percent"]:
            if hasattr(record, field):
                perf_fields[field] = getattr(record, field)

        if perf_fields:
            log_entry["performance"] = perf_fields

        return json.dumps(log_entry, ensure_ascii=False)


def setup_logging(config: Optional[LogConfig] = None) -> None:
    """Set up structured logging for EOMS with rotation and JSON formatting.

    Args:
        config: Logging configuration. Uses defaults if None.
    """
    if config is None:
        config = LogConfig()

    # Create log directory
    log_dir = Path(config.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.level.upper()))

    # Clear existing handlers
    root_logger.handlers.clear()

    # File handler with rotation
    log_file = log_dir / f"{config.service_name}.log"
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=config.max_bytes,
            backupCount=config.backup_count,
            encoding="utf-8",
        )

        if config.json_format:
            file_handler.setFormatter(EOSJSONFormatter(config.service_name, config.environment))
        else:
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )

        root_logger.addHandler(file_handler)
    except (OSError, PermissionError) as e:
        # If file logging fails, continue with console only
        print(f"Warning: Could not set up file logging: {e}")
        print("Logging will be console-only")
        pass

    # Console handler
    if config.console_output:
        console_handler = logging.StreamHandler(sys.stdout)

        if config.json_format:
            console_handler.setFormatter(EOSJSONFormatter(config.service_name, config.environment))
        else:
            console_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )

        root_logger.addHandler(console_handler)

    # Configure specific loggers to avoid duplicates
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    # Only log configuration success if explicitly requested
    # This prevents initial log entries during setup


def get_logger(name: str) -> logging.Logger:
    """Get a logger with trading-specific helper methods.

    Args:
        name: Logger name, typically __name__

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Add convenience methods for trading events
    def log_trade(level: int, message: str, **kwargs):
        """Log trading-related events with structured fields."""
        extra = {}
        if kwargs:
            extra["custom_fields"] = kwargs
        logger.log(level, message, extra=extra)

    def log_performance(level: int, message: str, **kwargs):
        """Log performance metrics with structured fields."""
        extra = {}
        if kwargs:
            extra["custom_fields"] = kwargs
        logger.log(level, message, extra=extra)

    # Attach methods to logger instance
    logger.log_trade = log_trade
    logger.log_performance = log_performance

    return logger


# Convenience functions for common trading events
def log_order_event(
    logger: logging.Logger,
    event_type: str,
    order_id: str,
    symbol: str,
    side: str,
    quantity: float,
    price: float = None,
    **kwargs,
):
    """Log order-related events with consistent structure."""
    extra_fields = {
        "event_type": event_type,
        "order_id": order_id,
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
    }

    if price is not None:
        extra_fields["price"] = price

    extra_fields.update(kwargs)

    logger.info(f"Order event: {event_type}", extra={"custom_fields": extra_fields})


def log_pnl_event(
    logger: logging.Logger,
    symbol: str,
    realized_pnl: float,
    unrealized_pnl: float,
    position: float = None,
    **kwargs,
):
    """Log P&L events with consistent structure."""
    extra_fields = {
        "event_type": "pnl_update",
        "symbol": symbol,
        "realized_pnl": realized_pnl,
        "unrealized_pnl": unrealized_pnl,
        "total_pnl": realized_pnl + unrealized_pnl,
    }

    if position is not None:
        extra_fields["position"] = position

    extra_fields.update(kwargs)

    logger.info(f"PnL update for {symbol}", extra={"custom_fields": extra_fields})


def log_latency_event(logger: logging.Logger, operation: str, latency_ms: float, **kwargs):
    """Log latency measurements with consistent structure."""
    extra_fields = {
        "event_type": "latency_measurement",
        "operation": operation,
        "latency_ms": latency_ms,
    }

    extra_fields.update(kwargs)

    level = logging.WARNING if latency_ms > 100 else logging.INFO
    logger.log(
        level,
        f"Operation {operation} took {latency_ms:.2f}ms",
        extra={"custom_fields": extra_fields},
    )
