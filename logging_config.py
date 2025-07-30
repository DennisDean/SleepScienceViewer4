# logging_config.py
import logging
from logging.handlers import RotatingFileHandler

LOG_FILENAME = "SleepScienceViewer.log"

# Set up a rotating log file (5 files max, 1MB each)
file_handler = RotatingFileHandler(
    LOG_FILENAME, maxBytes=1_000_000, backupCount=5
)
file_handler.setLevel(logging.INFO)

# Stream to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Format for all handlers
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s - %(name)s - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)

# Optional named logger for shared use
logger = logging.getLogger("SleepScienceViewer")
