import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(app_name: str, log_dir: str = "logs"):
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{app_name}.log")

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )

    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False  # avoid root logger conflicts

    if not logger.handlers:
        # File handler
        file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=5)
       # file_handler.setLevel(logging.INFO)      # ✅ explicitly set level
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)    # ✅ explicitly set level
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # Redirect Uvicorn loggers to the same handlers
    uvicorn_loggers = ["uvicorn", "uvicorn.error", "uvicorn.access"]
    for name in uvicorn_loggers:
        uv_logger = logging.getLogger(name)
        uv_logger.handlers = logger.handlers
        uv_logger.setLevel(logging.INFO)
        uv_logger.propagate = False

    return logger