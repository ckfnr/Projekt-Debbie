from typing import Any
import logging
import re
import os
from datetime import datetime
from env.config import config

# Decr
from env.decr.decorators import cached

# Ensure log folder exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create a timestamped log file on first import
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(LOG_DIR, f"{now}.log")

# Only configure logging once
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@cached
def redact_sensitive_data(msg: str) -> str:
    # Patterns to redact
    msg = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[REDACTED_IP]", msg)                                  # IPs
    msg = re.sub(r"\b[\w.-]+@[\w.-]+\.\w+\b", "[REDACTED_EMAIL]", msg)                                  # Emails
    msg = re.sub(r"(?i)(password|passwd|token|secret|api[_-]?key)[\"':= ]+\S+", r"\1=[REDACTED]", msg)  # Keys/secrets
    msg = re.sub(r"/home/\w+[^ ]*", "[REDACTED_PATH]", msg)                                             # Personal file paths
    return msg

def dprint(msg: Any) -> None:
    if not config.debug:
        return

    raw_str = str(msg)
    clean_msg = redact_sensitive_data(raw_str)

    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - DEBUG - {clean_msg}")
    logging.debug(clean_msg)
