import subprocess
from pathlib import Path

from config import WHISPER_EXE, OUT_TRANSCRIPTS_DIR, PROJECT_ROOT, MODEL, LANGUAGE
from logger import log


def _assert_inside_root(path: Path) -> None:
    if not str(path.resolve()).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"Path escape detected: {path}")


def transcribe(audio_path: Path, stem: str) -> Path | None:
    _assert_inside_root(OUT_TRANSCRIPTS_DIR)
    log("INFO", f"TRANSCRIBE {audio_path.name}")

    result = subprocess.run(
        [
            WHISPER_EXE,
            str(audio_path),
            "model", MODEL,
            "--output_dir", str(OUT_TRANSCRIPTS_DIR),
            "--task", "transcribe",
            "--language", LANGUAGE,
        ],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    if result.returncode != 0:
        log("ERROR", f"transcription failed — {result.stderr.strip()}")
        return None

    out_file = OUT_TRANSCRIPTS_DIR / f"{stem}.txt"
    log("INFO", f"TRANSCRIBE_OK → out-transcripts/{stem}.txt")
    return out_file
