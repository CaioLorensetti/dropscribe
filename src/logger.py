from datetime import datetime
from pathlib import Path
import sys

_log_file: Path | None = None


def _get_log_file() -> Path:
    global _log_file
    if _log_file is None:
        from config import LOG_FILE
        _log_file = LOG_FILE
    return _log_file


def log(level: str, message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}]  {message}"
    try:
        with open(_get_log_file(), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass
    print(line, file=sys.stderr)
