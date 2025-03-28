# argos_utils.py

from datetime import datetime, timezone
import time

DEBUG_LOG = "argos_debug_log.txt"

def get_utc_timestamp():
    """Returns UTC timestamp formatted for logging."""
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


def log_debug(message):
    """Appends a timestamped debug message to the log file."""
    timestamp = get_utc_timestamp()
    line = f"[{timestamp}] {message}\n"
    with open(DEBUG_LOG, "a") as f:
        f.write(line)


def retry_with_backoff(func, *args, max_attempts=5, base_delay=1, **kwargs):
    """
    Generic retry wrapper with exponential backoff.
    Accepts a function and retries it on failure.
    """
    attempt = 0
    delay = base_delay

    while attempt < max_attempts:
        try:
            result = func(*args, **kwargs)
            if result is not None:
                return result
        except Exception as e:
            log_debug(f"🔥 Attempt {attempt+1} failed: {e}")

        log_debug(f"⏳ Backing off for {delay}s before retry...")
        time.sleep(delay)
        delay *= 2
        attempt += 1

    log_debug("❌ Max retries exceeded.")
    return None
