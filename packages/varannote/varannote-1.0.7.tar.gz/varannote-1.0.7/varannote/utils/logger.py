#!/usr/bin/env python3
"""
Professional Logging System for VarAnnote v1.0.0

Provides comprehensive logging functionality including:
- Performance metrics tracking
- Error tracking and reporting
- Configurable log levels
- File and console output
- Structured logging for analysis
"""

import logging
import logging.handlers
import json
import time
import traceback
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Union
from datetime import datetime
import threading
from contextlib import contextmanager


class VarAnnoteLogger:
    """
    Professional logging system for VarAnnote
    
    Features:
    - Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - File rotation and archival
    - Performance metrics tracking
    - Error tracking with stack traces
    - JSON structured logging
    - Thread-safe operations
    """
    
    def __init__(self, 
                 name: str = "varannote",
                 log_dir: Optional[Union[str, Path]] = None,
                 log_level: str = "INFO",
                 max_file_size: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5,
                 enable_console: bool = True,
                 enable_file: bool = True,
                 enable_metrics: bool = True):
        """
        Initialize VarAnnote logger
        
        Args:
            name: Logger name
            log_dir: Directory for log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            max_file_size: Maximum size of log file before rotation
            backup_count: Number of backup files to keep
            enable_console: Enable console logging
            enable_file: Enable file logging
            enable_metrics: Enable performance metrics tracking
        """
        self.name = name
        self.log_level = getattr(logging, log_level.upper())
        self.enable_metrics = enable_metrics
        
        # Set up log directory
        if log_dir is None:
            log_dir = Path.home() / ".varannote" / "logs"
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Set up formatters
        self._setup_formatters()
        
        # Set up handlers
        if enable_console:
            self._setup_console_handler()
        
        if enable_file:
            self._setup_file_handlers(max_file_size, backup_count)
        
        # Performance metrics
        self.metrics = {
            'start_time': time.time(),
            'operations': {},
            'errors': [],
            'warnings': [],
            'performance_data': []
        }
        
        # Thread lock for metrics
        self._metrics_lock = threading.Lock()
        
        # Log initialization
        self.info(f"VarAnnote Logger initialized - Level: {log_level}")
        self.info(f"Log directory: {self.log_dir}")
    
    def _setup_formatters(self):
        """Set up log formatters"""
        # Console formatter (human readable)
        self.console_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File formatter (detailed)
        self.file_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # JSON formatter for structured logging
        self.json_formatter = JsonFormatter()
    
    def _setup_console_handler(self):
        """Set up console logging handler"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(self.console_formatter)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handlers(self, max_file_size: int, backup_count: int):
        """Set up file logging handlers"""
        # Main log file (rotating)
        main_log_file = self.log_dir / f"{self.name}.log"
        main_handler = logging.handlers.RotatingFileHandler(
            main_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        main_handler.setLevel(self.log_level)
        main_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(main_handler)
        
        # Error log file (errors only)
        error_log_file = self.log_dir / f"{self.name}_errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(error_handler)
        
        # JSON log file (structured data)
        json_log_file = self.log_dir / f"{self.name}_structured.jsonl"
        json_handler = logging.handlers.RotatingFileHandler(
            json_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        json_handler.setLevel(self.log_level)
        json_handler.setFormatter(self.json_formatter)
        self.logger.addHandler(json_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._log_with_context(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self._log_with_context(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._log_with_context(logging.WARNING, message, **kwargs)
        if self.enable_metrics:
            with self._metrics_lock:
                self.metrics['warnings'].append({
                    'timestamp': time.time(),
                    'message': message,
                    'context': kwargs
                })
    
    def error(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log error message with optional exception"""
        if exception:
            kwargs['exception_type'] = type(exception).__name__
            kwargs['exception_message'] = str(exception)
            kwargs['traceback'] = traceback.format_exc()
        
        self._log_with_context(logging.ERROR, message, **kwargs)
        
        if self.enable_metrics:
            with self._metrics_lock:
                self.metrics['errors'].append({
                    'timestamp': time.time(),
                    'message': message,
                    'exception': str(exception) if exception else None,
                    'context': kwargs
                })
    
    def critical(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log critical message"""
        if exception:
            kwargs['exception_type'] = type(exception).__name__
            kwargs['exception_message'] = str(exception)
            kwargs['traceback'] = traceback.format_exc()
        
        self._log_with_context(logging.CRITICAL, message, **kwargs)
    
    def _log_with_context(self, level: int, message: str, **kwargs):
        """Log message with additional context"""
        # Add context information
        extra = {
            'timestamp': time.time(),
            'thread_id': threading.get_ident(),
            'context': kwargs
        }
        
        # Log the message
        self.logger.log(level, message, extra=extra)
    
    @contextmanager
    def operation_timer(self, operation_name: str, **context):
        """
        Context manager for timing operations
        
        Usage:
            with logger.operation_timer("variant_annotation", variant_count=100):
                # perform annotation
                pass
        """
        start_time = time.time()
        self.debug(f"Starting operation: {operation_name}", **context)
        
        try:
            yield
            
            # Success
            duration = time.time() - start_time
            self.info(f"Completed operation: {operation_name} in {duration:.3f}s", 
                     duration=duration, **context)
            
            if self.enable_metrics:
                self._record_operation_metrics(operation_name, duration, True, context)
                
        except Exception as e:
            # Error
            duration = time.time() - start_time
            self.error(f"Failed operation: {operation_name} after {duration:.3f}s", 
                      exception=e, duration=duration, **context)
            
            if self.enable_metrics:
                self._record_operation_metrics(operation_name, duration, False, context)
            
            raise
    
    def _record_operation_metrics(self, operation_name: str, duration: float, 
                                 success: bool, context: Dict[str, Any]):
        """Record operation metrics"""
        with self._metrics_lock:
            if operation_name not in self.metrics['operations']:
                self.metrics['operations'][operation_name] = {
                    'count': 0,
                    'total_duration': 0.0,
                    'success_count': 0,
                    'error_count': 0,
                    'avg_duration': 0.0,
                    'min_duration': float('inf'),
                    'max_duration': 0.0
                }
            
            op_metrics = self.metrics['operations'][operation_name]
            op_metrics['count'] += 1
            op_metrics['total_duration'] += duration
            
            if success:
                op_metrics['success_count'] += 1
            else:
                op_metrics['error_count'] += 1
            
            op_metrics['avg_duration'] = op_metrics['total_duration'] / op_metrics['count']
            op_metrics['min_duration'] = min(op_metrics['min_duration'], duration)
            op_metrics['max_duration'] = max(op_metrics['max_duration'], duration)
            
            # Record individual performance data point
            self.metrics['performance_data'].append({
                'timestamp': time.time(),
                'operation': operation_name,
                'duration': duration,
                'success': success,
                'context': context
            })
    
    def log_performance_metrics(self):
        """Log current performance metrics"""
        if not self.enable_metrics:
            return
        
        with self._metrics_lock:
            total_runtime = time.time() - self.metrics['start_time']
            
            self.info("=== Performance Metrics Summary ===")
            self.info(f"Total runtime: {total_runtime:.3f}s")
            self.info(f"Total errors: {len(self.metrics['errors'])}")
            self.info(f"Total warnings: {len(self.metrics['warnings'])}")
            
            for op_name, op_metrics in self.metrics['operations'].items():
                success_rate = (op_metrics['success_count'] / op_metrics['count']) * 100
                self.info(f"Operation '{op_name}': "
                         f"count={op_metrics['count']}, "
                         f"avg_duration={op_metrics['avg_duration']:.3f}s, "
                         f"success_rate={success_rate:.1f}%")
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary as dictionary"""
        if not self.enable_metrics:
            return {}
        
        with self._metrics_lock:
            total_runtime = time.time() - self.metrics['start_time']
            
            return {
                'total_runtime': total_runtime,
                'error_count': len(self.metrics['errors']),
                'warning_count': len(self.metrics['warnings']),
                'operations': dict(self.metrics['operations']),
                'recent_errors': self.metrics['errors'][-10:],  # Last 10 errors
                'recent_warnings': self.metrics['warnings'][-10:]  # Last 10 warnings
            }
    
    def export_metrics(self, output_file: Union[str, Path]):
        """Export metrics to JSON file"""
        if not self.enable_metrics:
            self.warning("Metrics not enabled, nothing to export")
            return
        
        output_path = Path(output_file)
        
        with self._metrics_lock:
            metrics_data = {
                'export_timestamp': time.time(),
                'export_datetime': datetime.now().isoformat(),
                'logger_name': self.name,
                'total_runtime': time.time() - self.metrics['start_time'],
                'metrics': self.metrics
            }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(metrics_data, f, indent=2, default=str)
            
            self.info(f"Metrics exported to: {output_path}")
            
        except Exception as e:
            self.error(f"Failed to export metrics to {output_path}", exception=e)
    
    def set_log_level(self, level: str):
        """Change log level dynamically"""
        new_level = getattr(logging, level.upper())
        self.logger.setLevel(new_level)
        self.log_level = new_level
        
        # Update all handlers
        for handler in self.logger.handlers:
            if not isinstance(handler, logging.handlers.RotatingFileHandler) or \
               'errors' not in str(handler.baseFilename):
                handler.setLevel(new_level)
        
        self.info(f"Log level changed to: {level.upper()}")


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record):
        """Format log record as JSON"""
        log_data = {
            'timestamp': record.created,
            'datetime': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
            'thread_id': getattr(record, 'thread_id', None),
            'context': getattr(record, 'context', {})
        }
        
        # Add exception information if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
        
        return json.dumps(log_data, default=str)


# Global logger instance
_global_logger: Optional[VarAnnoteLogger] = None


def get_logger(name: str = "varannote", **kwargs) -> VarAnnoteLogger:
    """
    Get or create VarAnnote logger instance
    
    Args:
        name: Logger name
        **kwargs: Additional arguments for logger initialization
        
    Returns:
        VarAnnoteLogger instance
    """
    global _global_logger
    
    if _global_logger is None or _global_logger.name != name:
        _global_logger = VarAnnoteLogger(name=name, **kwargs)
    
    return _global_logger


def setup_logging(log_level: str = "INFO", 
                 log_dir: Optional[Union[str, Path]] = None,
                 enable_metrics: bool = True) -> VarAnnoteLogger:
    """
    Set up VarAnnote logging system
    
    Args:
        log_level: Logging level
        log_dir: Log directory
        enable_metrics: Enable performance metrics
        
    Returns:
        Configured VarAnnoteLogger instance
    """
    return get_logger(
        name="varannote",
        log_level=log_level,
        log_dir=log_dir,
        enable_metrics=enable_metrics
    )


# Convenience functions for quick logging
def debug(message: str, **kwargs):
    """Quick debug logging"""
    get_logger().debug(message, **kwargs)


def info(message: str, **kwargs):
    """Quick info logging"""
    get_logger().info(message, **kwargs)


def warning(message: str, **kwargs):
    """Quick warning logging"""
    get_logger().warning(message, **kwargs)


def error(message: str, exception: Optional[Exception] = None, **kwargs):
    """Quick error logging"""
    get_logger().error(message, exception=exception, **kwargs)


def critical(message: str, exception: Optional[Exception] = None, **kwargs):
    """Quick critical logging"""
    get_logger().critical(message, exception=exception, **kwargs) 