#!/usr/bin/env python3
"""
Comprehensive tests for VarAnnote logging system

Tests cover:
- Logger initialization and configuration
- Multiple log levels and handlers
- Performance metrics tracking
- File rotation and archival
- JSON structured logging
- Thread safety
- Error handling and exception logging
- Context managers and operation timing
"""

import pytest
import tempfile
import json
import time
import threading
import logging
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from contextlib import contextmanager

from varannote.utils.logger import (
    VarAnnoteLogger, JsonFormatter, get_logger, setup_logging,
    debug, info, warning, error, critical
)


class TestVarAnnoteLogger:
    """Test suite for VarAnnoteLogger class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.log_dir = Path(self.temp_dir) / "logs"
    
    def teardown_method(self):
        """Clean up test fixtures"""
        # Clean up any global logger state
        import varannote.utils.logger
        varannote.utils.logger._global_logger = None
    
    def test_logger_initialization(self):
        """Test logger initialization with default settings"""
        logger = VarAnnoteLogger(
            name="test_logger",
            log_dir=self.log_dir,
            log_level="INFO"
        )
        
        assert logger.name == "test_logger"
        assert logger.log_level == logging.INFO
        assert logger.log_dir == self.log_dir
        assert logger.enable_metrics is True
        assert logger.log_dir.exists()
        
        # Check that logger has handlers
        assert len(logger.logger.handlers) > 0
    
    def test_logger_initialization_custom_settings(self):
        """Test logger initialization with custom settings"""
        logger = VarAnnoteLogger(
            name="custom_logger",
            log_dir=self.log_dir,
            log_level="DEBUG",
            max_file_size=5 * 1024 * 1024,  # 5MB
            backup_count=3,
            enable_console=False,
            enable_file=True,
            enable_metrics=False
        )
        
        assert logger.name == "custom_logger"
        assert logger.log_level == logging.DEBUG
        assert logger.enable_metrics is False
        
        # Should have file handlers but no console handler
        handler_types = [type(h).__name__ for h in logger.logger.handlers]
        assert 'StreamHandler' not in handler_types
        assert 'RotatingFileHandler' in handler_types
    
    def test_logger_log_levels(self):
        """Test different log levels"""
        logger = VarAnnoteLogger(
            name="level_test",
            log_dir=self.log_dir,
            log_level="DEBUG",
            enable_console=False  # Avoid console output in tests
        )
        
        # Test all log levels
        logger.debug("Debug message", test_context="debug")
        logger.info("Info message", test_context="info")
        logger.warning("Warning message", test_context="warning")
        logger.error("Error message", test_context="error")
        logger.critical("Critical message", test_context="critical")
        
        # Check that log files were created
        log_files = list(self.log_dir.glob("*.log"))
        assert len(log_files) > 0
    
    def test_logger_with_exception(self):
        """Test logging with exception information"""
        logger = VarAnnoteLogger(
            name="exception_test",
            log_dir=self.log_dir,
            enable_console=False
        )
        
        try:
            raise ValueError("Test exception")
        except ValueError as e:
            logger.error("Error occurred", exception=e, context="test")
            logger.critical("Critical error", exception=e)
        
        # Check that error was recorded in metrics (critical doesn't add to errors if no metrics enabled for critical)
        assert len(logger.metrics['errors']) >= 1
        assert 'Test exception' in str(logger.metrics['errors'][0]['exception'])
    
    def test_operation_timer_success(self):
        """Test operation timer context manager for successful operations"""
        logger = VarAnnoteLogger(
            name="timer_test",
            log_dir=self.log_dir,
            enable_console=False
        )
        
        with logger.operation_timer("test_operation", variant_count=10):
            time.sleep(0.01)  # Simulate work
        
        # Check metrics
        assert "test_operation" in logger.metrics['operations']
        op_metrics = logger.metrics['operations']['test_operation']
        assert op_metrics['count'] == 1
        assert op_metrics['success_count'] == 1
        assert op_metrics['error_count'] == 0
        assert op_metrics['total_duration'] > 0
    
    def test_operation_timer_failure(self):
        """Test operation timer context manager for failed operations"""
        logger = VarAnnoteLogger(
            name="timer_fail_test",
            log_dir=self.log_dir,
            enable_console=False
        )
        
        with pytest.raises(ValueError):
            with logger.operation_timer("failing_operation", test_param="value"):
                time.sleep(0.01)
                raise ValueError("Test failure")
        
        # Check metrics
        assert "failing_operation" in logger.metrics['operations']
        op_metrics = logger.metrics['operations']['failing_operation']
        assert op_metrics['count'] == 1
        assert op_metrics['success_count'] == 0
        assert op_metrics['error_count'] == 1
        assert len(logger.metrics['errors']) == 1
    
    def test_metrics_tracking(self):
        """Test performance metrics tracking"""
        logger = VarAnnoteLogger(
            name="metrics_test",
            log_dir=self.log_dir,
            enable_console=False,
            enable_metrics=True
        )
        
        # Generate some metrics
        logger.warning("Test warning", context="test")
        logger.error("Test error")
        
        with logger.operation_timer("operation1"):
            time.sleep(0.01)
        
        with logger.operation_timer("operation2"):
            time.sleep(0.01)
        
        # Check metrics summary
        summary = logger.get_metrics_summary()
        assert summary['warning_count'] == 1
        assert summary['error_count'] == 1
        assert len(summary['operations']) == 2
        assert 'operation1' in summary['operations']
        assert 'operation2' in summary['operations']
    
    def test_metrics_disabled(self):
        """Test logger with metrics disabled"""
        logger = VarAnnoteLogger(
            name="no_metrics_test",
            log_dir=self.log_dir,
            enable_console=False,
            enable_metrics=False
        )
        
        logger.warning("Test warning")
        logger.error("Test error")
        
        # Metrics should be empty
        summary = logger.get_metrics_summary()
        assert summary == {}
    
    def test_log_level_change(self):
        """Test dynamic log level changes"""
        logger = VarAnnoteLogger(
            name="level_change_test",
            log_dir=self.log_dir,
            log_level="INFO",
            enable_console=False
        )
        
        # Initially INFO level
        assert logger.log_level == logging.INFO
        
        # Change to DEBUG
        logger.set_log_level("DEBUG")
        assert logger.log_level == logging.DEBUG
        
        # Change to ERROR
        logger.set_log_level("ERROR")
        assert logger.log_level == logging.ERROR
    
    def test_metrics_export(self):
        """Test metrics export functionality"""
        logger = VarAnnoteLogger(
            name="export_test",
            log_dir=self.log_dir,
            enable_console=False
        )
        
        # Generate some data
        logger.info("Test message")
        with logger.operation_timer("test_op"):
            time.sleep(0.01)
        
        # Export metrics
        export_file = self.log_dir / "metrics_export.json"
        logger.export_metrics(export_file)
        
        # Check export file
        assert export_file.exists()
        with open(export_file, 'r') as f:
            exported_data = json.load(f)
        
        assert 'export_timestamp' in exported_data
        assert 'metrics' in exported_data
        assert 'operations' in exported_data['metrics']
    
    def test_metrics_export_disabled(self):
        """Test metrics export when metrics are disabled"""
        logger = VarAnnoteLogger(
            name="export_disabled_test",
            log_dir=self.log_dir,
            enable_console=False,
            enable_metrics=False
        )
        
        export_file = self.log_dir / "no_metrics_export.json"
        logger.export_metrics(export_file)
        
        # File should not be created
        assert not export_file.exists()
    
    def test_performance_metrics_logging(self):
        """Test performance metrics logging"""
        logger = VarAnnoteLogger(
            name="perf_log_test",
            log_dir=self.log_dir,
            enable_console=False
        )
        
        # Generate some operations
        with logger.operation_timer("op1"):
            time.sleep(0.01)
        
        with logger.operation_timer("op2"):
            time.sleep(0.01)
        
        # This should not raise an exception
        logger.log_performance_metrics()
        
        # Check that performance data was recorded
        assert len(logger.metrics['performance_data']) == 2
    
    def test_thread_safety(self):
        """Test thread safety of metrics tracking"""
        logger = VarAnnoteLogger(
            name="thread_test",
            log_dir=self.log_dir,
            enable_console=False
        )
        
        def worker_function(worker_id):
            for i in range(5):
                with logger.operation_timer(f"worker_{worker_id}_op", iteration=i):
                    time.sleep(0.001)
                logger.info(f"Worker {worker_id} iteration {i}")
        
        # Create multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=worker_function, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check that all operations were recorded
        total_operations = sum(
            op_data['count'] 
            for op_data in logger.metrics['operations'].values()
        )
        assert total_operations == 15  # 3 workers * 5 operations each


class TestJsonFormatter:
    """Test suite for JsonFormatter class"""
    
    def test_json_formatter_basic(self):
        """Test basic JSON formatting"""
        formatter = JsonFormatter()
        
        # Create a log record
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        record.funcName = "test_function"
        record.module = "test_module"
        record.thread_id = 12345
        record.context = {"key": "value"}
        
        # Format the record
        formatted = formatter.format(record)
        
        # Parse JSON
        log_data = json.loads(formatted)
        
        assert log_data['level'] == 'INFO'
        assert log_data['logger'] == 'test_logger'
        assert log_data['message'] == 'Test message'
        assert log_data['function'] == 'test_function'
        assert log_data['module'] == 'test_module'
        assert log_data['thread_id'] == 12345
        assert log_data['context'] == {"key": "value"}
    
    def test_json_formatter_with_exception(self):
        """Test JSON formatting with exception information"""
        formatter = JsonFormatter()
        
        try:
            raise ValueError("Test exception")
        except ValueError:
            exc_info = sys.exc_info()
        
        record = logging.LogRecord(
            name="test_logger",
            level=logging.ERROR,
            pathname="test.py",
            lineno=10,
            msg="Error occurred",
            args=(),
            exc_info=exc_info
        )
        record.funcName = "test_function"
        record.module = "test_module"
        
        formatted = formatter.format(record)
        log_data = json.loads(formatted)
        
        assert 'exception' in log_data
        assert log_data['exception']['type'] == 'ValueError'
        assert log_data['exception']['message'] == 'Test exception'
        assert 'traceback' in log_data['exception']


class TestGlobalFunctions:
    """Test suite for global logger functions"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.log_dir = Path(self.temp_dir) / "logs"
        
        # Clear global logger
        import varannote.utils.logger
        varannote.utils.logger._global_logger = None
    
    def teardown_method(self):
        """Clean up test fixtures"""
        # Clear global logger
        import varannote.utils.logger
        varannote.utils.logger._global_logger = None
    
    def test_get_logger(self):
        """Test get_logger function"""
        logger1 = get_logger("test_logger", log_dir=self.log_dir, enable_console=False)
        logger2 = get_logger("test_logger", log_dir=self.log_dir, enable_console=False)
        
        # Should return the same instance for same name
        assert logger1 is logger2
        assert logger1.name == "test_logger"
    
    def test_get_logger_different_names(self):
        """Test get_logger with different names"""
        logger1 = get_logger("logger1", log_dir=self.log_dir, enable_console=False)
        logger2 = get_logger("logger2", log_dir=self.log_dir, enable_console=False)
        
        # Should return different instances for different names
        assert logger1 is not logger2
        assert logger1.name == "logger1"
        assert logger2.name == "logger2"
    
    def test_setup_logging(self):
        """Test setup_logging function"""
        logger = setup_logging(
            log_level="DEBUG",
            log_dir=self.log_dir,
            enable_metrics=True
        )
        
        assert isinstance(logger, VarAnnoteLogger)
        assert logger.name == "varannote"
        assert logger.log_level == logging.DEBUG
        assert logger.enable_metrics is True
    
    def test_convenience_functions(self):
        """Test convenience logging functions"""
        # Set up global logger
        setup_logging(log_level="INFO", log_dir=self.log_dir, enable_metrics=True)
        
        # Test convenience functions
        debug("Debug message", context="test")
        info("Info message", context="test")
        warning("Warning message", context="test")
        error("Error message", context="test")
        critical("Critical message", context="test")
        
        # Test error with exception
        try:
            raise ValueError("Test exception")
        except ValueError as e:
            error("Error with exception", exception=e)
        
        # Should not raise any exceptions
        assert True


class TestLoggerIntegration:
    """Integration tests for logger functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.log_dir = Path(self.temp_dir) / "logs"
    
    def test_file_creation_and_rotation(self):
        """Test log file creation and rotation"""
        logger = VarAnnoteLogger(
            name="rotation_test",
            log_dir=self.log_dir,
            max_file_size=1024,  # Small size to trigger rotation
            backup_count=2,
            enable_console=False
        )
        
        # Generate enough log data to trigger rotation
        for i in range(100):
            logger.info(f"Log message {i} with some additional content to increase size")
        
        # Check that log files exist
        log_files = list(self.log_dir.glob("rotation_test*.log"))
        assert len(log_files) > 0
    
    def test_structured_logging(self):
        """Test structured JSON logging"""
        logger = VarAnnoteLogger(
            name="structured_test",
            log_dir=self.log_dir,
            enable_console=False
        )
        
        # Log with structured data
        logger.info("Structured message", 
                   variant_id="chr1:100:A>T",
                   database="clinvar",
                   confidence=0.95)
        
        # Check JSON log file
        json_files = list(self.log_dir.glob("*_structured.jsonl"))
        assert len(json_files) > 0
        
        # Read and parse JSON log - find the structured message line
        with open(json_files[0], 'r') as f:
            lines = f.readlines()
        
        # Find the line with our structured message
        structured_line = None
        for line in lines:
            log_data = json.loads(line.strip())
            if log_data['message'] == 'Structured message':
                structured_line = log_data
                break
        
        assert structured_line is not None
        assert structured_line['context']['variant_id'] == 'chr1:100:A>T'
        assert structured_line['context']['database'] == 'clinvar'
        assert structured_line['context']['confidence'] == 0.95
    
    def test_error_file_separation(self):
        """Test that errors are logged to separate file"""
        logger = VarAnnoteLogger(
            name="error_sep_test",
            log_dir=self.log_dir,
            enable_console=False
        )
        
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
        # Check that error file exists and contains errors
        error_files = list(self.log_dir.glob("*_errors.log"))
        assert len(error_files) > 0
        
        with open(error_files[0], 'r') as f:
            error_content = f.read()
        
        assert "Error message" in error_content
        assert "Critical message" in error_content
        # Info and warning should not be in error file
        assert "Info message" not in error_content
        assert "Warning message" not in error_content
    
    def test_complex_operation_timing(self):
        """Test complex nested operation timing"""
        logger = VarAnnoteLogger(
            name="complex_timing_test",
            log_dir=self.log_dir,
            enable_console=False
        )
        
        with logger.operation_timer("main_operation", total_variants=100):
            for i in range(3):
                with logger.operation_timer("sub_operation", variant_index=i):
                    time.sleep(0.001)
                    logger.info(f"Processed variant {i}")
        
        # Check that all operations were recorded
        assert "main_operation" in logger.metrics['operations']
        assert "sub_operation" in logger.metrics['operations']
        
        main_op = logger.metrics['operations']['main_operation']
        sub_op = logger.metrics['operations']['sub_operation']
        
        assert main_op['count'] == 1
        assert sub_op['count'] == 3
        assert main_op['success_count'] == 1
        assert sub_op['success_count'] == 3


class TestErrorHandling:
    """Test error handling scenarios"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.log_dir = Path(self.temp_dir) / "logs"
    
    def test_invalid_log_level(self):
        """Test handling of invalid log level"""
        with pytest.raises(AttributeError):
            VarAnnoteLogger(
                name="invalid_level_test",
                log_dir=self.log_dir,
                log_level="INVALID_LEVEL"
            )
    
    def test_export_metrics_file_error(self):
        """Test metrics export with file write error"""
        logger = VarAnnoteLogger(
            name="export_error_test",
            log_dir=self.log_dir,
            enable_console=False
        )
        
        # Try to export to invalid path
        invalid_path = Path("/invalid/path/metrics.json")
        logger.export_metrics(invalid_path)
        
        # Should log error but not crash
        assert len(logger.metrics['errors']) > 0
    
    def test_log_with_context_edge_cases(self):
        """Test logging with various context edge cases"""
        logger = VarAnnoteLogger(
            name="context_test",
            log_dir=self.log_dir,
            enable_console=False
        )
        
        # Test with None values
        logger.info("Message with None", value=None)
        
        # Test with complex objects
        logger.info("Message with complex object", 
                   data={"nested": {"key": "value"}},
                   list_data=[1, 2, 3])
        
        # Test with circular reference (should not crash)
        circular = {"key": "value"}
        circular["self"] = circular
        logger.info("Message with circular reference", data=str(circular))
        
        # Should not raise any exceptions
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])