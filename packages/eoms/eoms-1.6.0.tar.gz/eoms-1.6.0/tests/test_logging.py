"""Tests for structured JSON logging system."""

import json
import logging
import tempfile
from pathlib import Path

from eoms.core.logging import (
    EOSJSONFormatter,
    LogConfig,
    get_logger,
    log_latency_event,
    log_order_event,
    log_pnl_event,
    setup_logging,
)


class TestLogConfig:
    """Test logging configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = LogConfig()

        assert config.level == "INFO"
        assert config.log_dir == "logs"
        assert config.max_bytes == 50 * 1024 * 1024
        assert config.backup_count == 10
        assert config.console_output is True
        assert config.json_format is True
        assert config.service_name == "eoms"
        assert config.environment == "development"

    def test_custom_config(self):
        """Test custom configuration."""
        config = LogConfig(
            level="DEBUG",
            log_dir="/tmp/test_logs",
            max_bytes=1024,
            backup_count=5,
            console_output=False,
            json_format=False,
            service_name="test_service",
            environment="test",
        )

        assert config.level == "DEBUG"
        assert config.log_dir == "/tmp/test_logs"
        assert config.max_bytes == 1024
        assert config.backup_count == 5
        assert config.console_output is False
        assert config.json_format is False
        assert config.service_name == "test_service"
        assert config.environment == "test"


class TestEOSJSONFormatter:
    """Test JSON formatter."""

    def test_basic_formatting(self):
        """Test basic log record formatting."""
        formatter = EOSJSONFormatter("test_service", "test_env")

        # Create log record
        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="/test/file.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.module = "file"
        record.funcName = "test_function"
        record.filename = "file.py"
        record.thread = 12345
        record.threadName = "MainThread"
        record.process = 6789

        # Format and parse JSON
        formatted = formatter.format(record)
        log_data = json.loads(formatted)

        # Verify required fields
        assert log_data["level"] == "INFO"
        assert log_data["logger"] == "test.logger"
        assert log_data["message"] == "Test message"
        assert log_data["service"] == "test_service"
        assert log_data["environment"] == "test_env"
        assert log_data["module"] == "file"
        assert log_data["function"] == "test_function"
        assert log_data["line"] == 42
        assert log_data["filename"] == "file.py"
        assert "@timestamp" in log_data

    def test_exception_formatting(self):
        """Test exception information formatting."""
        formatter = EOSJSONFormatter()

        try:
            raise ValueError("Test exception")
        except ValueError:
            record = logging.LogRecord(
                name="test.logger",
                level=logging.ERROR,
                pathname="/test/file.py",
                lineno=42,
                msg="Error occurred",
                args=(),
                exc_info=True,
            )
            record.module = "file"
            record.funcName = "test_function"
            record.filename = "file.py"
            record.thread = 12345
            record.threadName = "MainThread"
            record.process = 6789

            formatted = formatter.format(record)
            log_data = json.loads(formatted)

            assert "exception" in log_data
            assert log_data["exception"]["type"] == "ValueError"
            assert log_data["exception"]["message"] == "Test exception"
            assert "Traceback" in log_data["exception"]["traceback"]

    def test_custom_fields(self):
        """Test custom fields in log records."""
        formatter = EOSJSONFormatter()

        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="/test/file.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.module = "file"
        record.funcName = "test_function"
        record.filename = "file.py"
        record.thread = 12345
        record.threadName = "MainThread"
        record.process = 6789
        record.custom_fields = {"custom_key": "custom_value"}

        formatted = formatter.format(record)
        log_data = json.loads(formatted)

        assert log_data["custom_key"] == "custom_value"

    def test_trading_fields(self):
        """Test trading-specific fields."""
        formatter = EOSJSONFormatter()

        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="/test/file.py",
            lineno=42,
            msg="Trade executed",
            args=(),
            exc_info=None,
        )
        record.module = "file"
        record.funcName = "test_function"
        record.filename = "file.py"
        record.thread = 12345
        record.threadName = "MainThread"
        record.process = 6789
        record.symbol = "AAPL"
        record.order_id = "ORDER123"
        record.quantity = 100
        record.price = 150.25

        formatted = formatter.format(record)
        log_data = json.loads(formatted)

        assert "trading" in log_data
        assert log_data["trading"]["symbol"] == "AAPL"
        assert log_data["trading"]["order_id"] == "ORDER123"
        assert log_data["trading"]["quantity"] == 100
        assert log_data["trading"]["price"] == 150.25


class TestLoggingSetup:
    """Test logging setup and configuration."""

    def test_setup_with_defaults(self):
        """Test setup with default configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfig(log_dir=temp_dir, console_output=False)
            setup_logging(config)

            # Check log file creation
            log_file = Path(temp_dir) / "eoms.log"

            # Test logging
            logger = logging.getLogger("test.setup")
            logger.info("Test message")

            # Verify log file exists and has content
            assert log_file.exists()

            # Read and verify JSON format
            with open(log_file, "r") as f:
                log_lines = f.read().strip().split("\n")
                # Find our test message
                test_log_data = None
                for line in log_lines:
                    if line:
                        data = json.loads(line)
                        if data["message"] == "Test message":
                            test_log_data = data
                            break

                assert test_log_data is not None
                assert test_log_data["service"] == "eoms"

    def test_setup_non_json_format(self):
        """Test setup with non-JSON formatting."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfig(log_dir=temp_dir, console_output=False, json_format=False)
            setup_logging(config)

            log_file = Path(temp_dir) / "eoms.log"

            logger = logging.getLogger("test.non_json")
            logger.info("Test message")

            assert log_file.exists()

            with open(log_file, "r") as f:
                log_line = f.read().strip()
                # Should not be JSON format
                assert "Test message" in log_line
                assert not log_line.startswith('{"')


class TestLoggerHelpers:
    """Test logger helper functions."""

    def test_get_logger(self):
        """Test get_logger function."""
        logger = get_logger("test.helpers")

        assert isinstance(logger, logging.Logger)
        assert logger.name == "test.helpers"
        assert hasattr(logger, "log_trade")
        assert hasattr(logger, "log_performance")

    def test_log_order_event(self):
        """Test order event logging."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfig(log_dir=temp_dir, console_output=False)
            setup_logging(config)

            logger = get_logger("test.order")
            log_order_event(logger, "order_placed", "ORDER123", "AAPL", "BUY", 100, 150.25)

            log_file = Path(temp_dir) / "eoms.log"
            assert log_file.exists()

            with open(log_file, "r") as f:
                log_lines = f.read().strip().split("\n")
                # Get the last log line (our test message)
                log_data = json.loads(log_lines[-1])

                assert log_data["message"] == "Order event: order_placed"
                assert log_data["event_type"] == "order_placed"
                assert log_data["order_id"] == "ORDER123"
                assert log_data["symbol"] == "AAPL"
                assert log_data["side"] == "BUY"
                assert log_data["quantity"] == 100
                assert log_data["price"] == 150.25

    def test_log_pnl_event(self):
        """Test P&L event logging."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfig(log_dir=temp_dir, console_output=False)
            setup_logging(config)

            logger = get_logger("test.pnl")
            log_pnl_event(logger, "AAPL", 100.0, 50.0, 200)

            log_file = Path(temp_dir) / "eoms.log"
            assert log_file.exists()

            with open(log_file, "r") as f:
                log_lines = f.read().strip().split("\n")
                # Get the last log line (our test message)
                log_data = json.loads(log_lines[-1])

                assert log_data["message"] == "PnL update for AAPL"
                assert log_data["event_type"] == "pnl_update"
                assert log_data["symbol"] == "AAPL"
                assert log_data["realized_pnl"] == 100.0
                assert log_data["unrealized_pnl"] == 50.0
                assert log_data["total_pnl"] == 150.0
                assert log_data["position"] == 200

    def test_log_latency_event(self):
        """Test latency event logging."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfig(log_dir=temp_dir, console_output=False)
            setup_logging(config)

            logger = get_logger("test.latency")
            log_latency_event(logger, "order_placement", 25.5)

            log_file = Path(temp_dir) / "eoms.log"
            assert log_file.exists()

            with open(log_file, "r") as f:
                log_lines = f.read().strip().split("\n")
                # Get the last log line (our test message)
                log_data = json.loads(log_lines[-1])

                assert "Operation order_placement took 25.50ms" in log_data["message"]
                assert log_data["event_type"] == "latency_measurement"
                assert log_data["operation"] == "order_placement"
                assert log_data["latency_ms"] == 25.5

    def test_log_latency_warning_threshold(self):
        """Test latency warning for high latency."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfig(log_dir=temp_dir, console_output=False)
            setup_logging(config)

            logger = get_logger("test.latency")
            log_latency_event(logger, "slow_operation", 150.0)

            log_file = Path(temp_dir) / "eoms.log"
            assert log_file.exists()

            with open(log_file, "r") as f:
                log_lines = f.read().strip().split("\n")
                # Get the last log line (our test message)
                log_data = json.loads(log_lines[-1])

                # Should be WARNING level for high latency
                assert log_data["level"] == "WARNING"
                assert log_data["latency_ms"] == 150.0


class TestLogRotation:
    """Test log rotation functionality."""

    def test_rotation_config(self):
        """Test that rotation configuration is applied."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfig(
                log_dir=temp_dir,
                max_bytes=1024,  # Small size for testing
                backup_count=3,
                console_output=False,
            )
            setup_logging(config)

            # Get handler and verify rotation settings
            logger = logging.getLogger()
            file_handler = None
            for handler in logger.handlers:
                if hasattr(handler, "maxBytes"):
                    file_handler = handler
                    break

            assert file_handler is not None
            assert file_handler.maxBytes == 1024
            assert file_handler.backupCount == 3
