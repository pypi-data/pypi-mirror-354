# Copyright 2024 Agnostiq Inc.
"""Logger for core blueprints functionality."""

import logging
import time
from pathlib import Path

# Define the log file path
BLUEPRINTS_LOGFILE = Path.home() / ".cache/covalent/blueprints/logfile.txt"

# Maximum log file size in MB
MAX_LOG_SIZE_MB = 10


def clear_logs() -> None:
    """Delete the blueprints log file."""
    if not BLUEPRINTS_LOGFILE.exists():
        BLUEPRINTS_LOGFILE.parent.mkdir(parents=True, exist_ok=True)
        BLUEPRINTS_LOGFILE.touch()

    with open(BLUEPRINTS_LOGFILE, "w", encoding="utf-8") as log_file:
        log_file.write("")

    print(f"Erased contents of logs file: {BLUEPRINTS_LOGFILE!s}")


def get_logs_content() -> str:
    """Return the contents of the blueprints log file."""
    with open(BLUEPRINTS_LOGFILE, "r", encoding="utf-8") as log_file:
        return "\n".join([log_file.read(), f"[FILE: {BLUEPRINTS_LOGFILE!s}]"])


# Ensure the log file and its directory exist
if not BLUEPRINTS_LOGFILE.exists():
    BLUEPRINTS_LOGFILE.parent.mkdir(parents=True, exist_ok=True)
    BLUEPRINTS_LOGFILE.touch()
# Clear the log file if it exceeds the maximum size
elif BLUEPRINTS_LOGFILE.is_file():
    size_mb = BLUEPRINTS_LOGFILE.stat().st_size / 1024**2
    if size_mb > MAX_LOG_SIZE_MB:
        print(f"Log file size exceeds {MAX_LOG_SIZE_MB:.1f} MB. Clearing logs.")
        clear_logs()

# Define the log format
LOG_FORMAT = (
    "> %(asctime)s [%(levelname)s] - %(pathname)s:%(lineno)d\n\n%(message)s\n\n"
)

# Create a logger
bp_log = logging.getLogger("covalent_blueprints")
bp_log.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler(BLUEPRINTS_LOGFILE)
file_handler.setLevel(logging.DEBUG)


class LocalTimeFormatter(logging.Formatter):
    """Override the converter to use local time."""

    def converter(self, timestamp):
        """Overridden converter method."""
        return time.localtime(timestamp)


# Create a formatter with local time
formatter = LocalTimeFormatter(
    fmt=LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_handler.setFormatter(formatter)

# Add the handler to the logger
bp_log.addHandler(file_handler)
