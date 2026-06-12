import logging
import logging.handlers
import sys
import os
from .settings import Config

def setup_logging():
    """Configures application-wide logging with rotation to prevent unbounded growth."""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Store log file absolutely in the user's home directory to prevent PermissionError when launched from system directories (e.g., startup registry)
    log_path = os.path.join(os.path.expanduser("~"), "kodearrow.log")
    
    # Use RotatingFileHandler: max 2MB per file, keep 3 backup files (total ~8MB max)
    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=2 * 1024 * 1024,  # 2 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(Config.LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    handlers = [file_handler]
    
    # Only add StreamHandler if stdout is a real stream (not NullStream or None)
    # In windowless mode, stdout may be our NullStream — still safe to write to,
    # but we skip it to avoid useless overhead
    if sys.stdout is not None and hasattr(sys.stdout, 'fileno'):
        try:
            sys.stdout.fileno()  # Will raise if it's our NullStream (-1) or invalid
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(Config.LOG_LEVEL)
            stream_handler.setFormatter(logging.Formatter(log_format))
            handlers.append(stream_handler)
        except (OSError, ValueError):
            pass  # No valid stdout — skip console logging
    
    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format=log_format,
        handlers=handlers
    )
    
    # Suppress verbose logs from third-party libraries
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    logger = logging.getLogger("KodeArrow")
    logger.info(f"Logging initialized at level {Config.LOG_LEVEL}")
    return logger
