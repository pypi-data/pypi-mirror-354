"""
Logging configuration for the MCP Code Indexer.

This module provides centralized logging setup with structured JSON output,
proper async handling, and file rotation for production use.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from .error_handler import StructuredFormatter


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    enable_file_logging: bool = False,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Set up comprehensive logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        enable_file_logging: Whether to enable file logging
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        
    Returns:
        Configured root logger
    """
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler (stderr to avoid interfering with MCP stdout)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Use structured formatter for all handlers
    structured_formatter = StructuredFormatter()
    console_handler.setFormatter(structured_formatter)
    
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if enable_file_logging and log_file:
        try:
            # Ensure log directory exists
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Rotating file handler
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)  # File gets all levels
            file_handler.setFormatter(structured_formatter)
            
            root_logger.addHandler(file_handler)
            
        except (OSError, PermissionError) as e:
            # Log to console if file logging fails
            root_logger.warning(f"Failed to set up file logging: {e}")
    
    # Configure specific loggers
    
    # Quiet down noisy libraries
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)
    logging.getLogger("tiktoken").setLevel(logging.WARNING)
    
    # MCP specific loggers
    mcp_logger = logging.getLogger("mcp")
    mcp_logger.setLevel(logging.INFO)
    
    # Database logger
    db_logger = logging.getLogger("src.database")
    db_logger.setLevel(logging.INFO)
    
    # Server logger
    server_logger = logging.getLogger("src.server")
    server_logger.setLevel(logging.INFO)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def log_performance_metrics(
    logger: logging.Logger,
    operation: str,
    duration: float,
    **metrics
) -> None:
    """
    Log performance metrics in structured format.
    
    Args:
        logger: Logger instance
        operation: Name of the operation
        duration: Duration in seconds
        **metrics: Additional metrics to log
    """
    perf_data = {
        "operation": operation,
        "duration_seconds": duration,
        "metrics": metrics
    }
    
    logger.info(
        f"Performance: {operation} completed in {duration:.3f}s",
        extra={"structured_data": {"performance": perf_data}}
    )


def log_tool_usage(
    logger: logging.Logger,
    tool_name: str,
    arguments: dict,
    success: bool,
    duration: Optional[float] = None,
    result_size: Optional[int] = None
) -> None:
    """
    Log MCP tool usage for analytics.
    
    Args:
        logger: Logger instance
        tool_name: Name of the MCP tool
        arguments: Tool arguments (will be sanitized)
        success: Whether the operation succeeded
        duration: Operation duration in seconds
        result_size: Size of result data
    """
    # Sanitize arguments
    safe_args = {}
    for key, value in arguments.items():
        if isinstance(value, str) and len(value) > 50:
            safe_args[key] = f"{value[:50]}..."
        else:
            safe_args[key] = value
    
    usage_data = {
        "tool_name": tool_name,
        "arguments": safe_args,
        "success": success
    }
    
    if duration is not None:
        usage_data["duration_seconds"] = duration
    
    if result_size is not None:
        usage_data["result_size"] = result_size
    
    level = logging.INFO if success else logging.WARNING
    message = f"Tool {tool_name}: {'SUCCESS' if success else 'FAILED'}"
    
    logger.log(
        level,
        message,
        extra={"structured_data": {"tool_usage": usage_data}}
    )
