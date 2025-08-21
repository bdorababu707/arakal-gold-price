import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Development flag; set False for production
is_development = True

def setup_logging() -> None:
    log_dir = Path("./logs/gold")  # Separate folder for gold price logs
    log_dir.mkdir(parents=True, exist_ok=True)

    rotation_size = 10 * 1024 * 1024  # 10 MB
    backup_count = 5

    root_logger = logging.getLogger()
    base_level = logging.INFO if is_development else logging.WARNING
    root_logger.setLevel(base_level)

    # Remove old handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(base_level)
    root_logger.addHandler(console_handler)

    # Main log file
    file_handler = RotatingFileHandler(
        filename=log_dir / "app.log",
        maxBytes=rotation_size,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(base_level)
    root_logger.addHandler(file_handler)

    # Error log file
    error_file_handler = RotatingFileHandler(
        filename=log_dir / "error.log",
        maxBytes=rotation_size,
        backupCount=backup_count,
        encoding="utf-8"
    )
    error_file_handler.setFormatter(formatter)
    error_file_handler.setLevel(logging.ERROR)
    root_logger.addHandler(error_file_handler)

    logging.info(f"Gold price fetcher initialized in {'development' if is_development else 'production'} mode")

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
