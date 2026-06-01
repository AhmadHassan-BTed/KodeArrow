import logging
import sys
import os
from .settings import Config

def setup_logging():
    """Configures application-wide logging."""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Store log file absolutely in the user's home directory to prevent PermissionError when launched from system directories (e.g., startup registry)
    log_path = os.path.join(os.path.expanduser("~"), "kodearrow.log")
    
    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_path, encoding='utf-8')
        ]
    )
    
    # Suppress verbose logs from third-party libraries
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    logger = logging.getLogger("KodeArrow")
    logger.info(f"Logging initialized at level {Config.LOG_LEVEL}")
    return logger
