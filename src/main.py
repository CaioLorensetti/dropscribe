import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import config
from logger import log
from converter import extract_audio
from transcriber import transcribe


def _assert_inside_root(path: Path) -> None:
    if not str(path.resolve()).startswith(str(config.PROJECT_ROOT)):
        raise ValueError(f"Path escape detected: {path}")


def _is_pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except PermissionError:
        return True  # process exists but we lack permission to signal it
    except OSError:
        return False


def acquire_lock() -> None:
    if config.LOCK_FILE.exists():
        pid: int | None = None
        if config.PID_FILE.exists():
            try:
                pid = int(config.PID_FILE.read_text(encoding="utf-8").strip())
            except ValueError:
                pass

        if pid is not None and _is_pid_alive(pid):
            log("ERROR", "another instance is running")
            sys.exit(1)

        log("INFO", "Stale lock removed — previous instance was killed ungracefully")
        config.LOCK_FILE.unlink(missing_ok=True)
        config.PID_FILE.unlink(missing_ok=True)

    config.LOCK_FILE.touch()


def release_lock() -> None:
    config.LOCK_FILE.unlink(missing_ok=True)


def write_pid() -> None:
    config.PID_FILE.write_text(str(os.getpid()), encoding="utf-8")


def delete_pid() -> None:
    config.PID_FILE.unlink(missing_ok=True)


def process_file(source: Path) -> None:
    log("INFO", f"DETECTED  {source.name}")
    audio_path: Path | None = None
    try:
        audio_path = extract_audio(source)
        if audio_path is None:
            return

        out_file = transcribe(audio_path, source.stem)
        if out_file is None:
            return

        _assert_inside_root(source)
        source.unlink()
        log("INFO", f"DONE      {source.name} deleted")
    finally:
        if audio_path is not None and audio_path != source and audio_path.exists():
            audio_path.unlink(missing_ok=True)


def poll_cycle() -> None:
    candidates = [
        f for f in config.IN_FILES_DIR.iterdir()
        if f.is_file() and not f.name.startswith(".")
    ]

    if not candidates:
        log("INFO", "Idle — no files in queue")
        return

    for source in sorted(candidates, key=lambda p: p.stat().st_mtime):
        ext = source.suffix.lower()
        if ext not in config.ACCEPTED_EXTENSIONS:
            log("INFO", f"SKIP      {source.name} — unsupported format")
            continue
        process_file(source)

    log("INFO", "IDLE      queue empty")


def main() -> None:
    acquire_lock()
    write_pid()
    log("INFO", "Service started")
    try:
        while True:
            try:
                poll_cycle()
            except Exception as exc:
                log("FATAL", str(exc))
            time.sleep(config.POLL_INTERVAL_SEC)
    except KeyboardInterrupt:
        log("INFO", "SHUTDOWN")
    finally:
        release_lock()
        delete_pid()


if __name__ == "__main__":
    main()
