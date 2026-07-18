import logging
import os

from assistant.config.settings import LOG_FILE, LOG_LEVEL

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


# Configure the logger
logging.basicConfig(
    filename=LOG_FILE,
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    force=True
)

logger = logging.getLogger("Soni")