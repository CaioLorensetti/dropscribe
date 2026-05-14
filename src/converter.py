import subprocess
from pathlib import Path

from config import FFMPEG_EXE, LOSSLESS_AUDIO_EXTENSIONS, IN_FILES_DIR, PROJECT_ROOT
from logger import log


def _assert_inside_root(path: Path) -> None:
    if not str(path.resolve()).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"Path escape detected: {path}")


def extract_audio(input_path: Path) -> Path | None:
    ext = input_path.suffix.lower()

    if ext in LOSSLESS_AUDIO_EXTENSIONS:
        return input_path

    tmp_flac = IN_FILES_DIR / f"_tmp_{input_path.stem}.flac"
    _assert_inside_root(tmp_flac)
    log("INFO", f"CONVERT   {input_path.name} → {tmp_flac.name}")

    result = subprocess.run(
        [
            FFMPEG_EXE,
            "-i", str(input_path),
            "-vn",
            "-c:a", "flac",
            "-compression_level", "8",
            str(tmp_flac),
            "-y",
        ],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    if result.returncode != 0:
        log("ERROR", f"conversion failed — {result.stderr.strip()}")
        return None

    log("INFO", "CONVERT_OK")
    return tmp_flac
