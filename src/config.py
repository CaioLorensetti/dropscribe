from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
IN_FILES_DIR = PROJECT_ROOT / "in-files"
OUT_TRANSCRIPTS_DIR = PROJECT_ROOT / "out-transcripts"
LOG_FILE = PROJECT_ROOT / "log.txt"
LOCK_FILE = IN_FILES_DIR / ".lock"
PID_FILE = IN_FILES_DIR / ".pid"

FFMPEG_EXE = r"C:\Users\caiol\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
WHISPER_EXE = r"C:\Users\caiol\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts\whisper.exe"

POLL_INTERVAL_SEC = 5

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv", ".wmv", ".mpeg", ".m4v", ".3gp", ".mxf"}
AUDIO_EXTENSIONS = {".mp3", ".aac", ".wav", ".flac", ".ogg", ".m4a", ".opus", ".wma", ".aiff", ".ac3", ".dts"}
ACCEPTED_EXTENSIONS = VIDEO_EXTENSIONS | AUDIO_EXTENSIONS
LOSSLESS_AUDIO_EXTENSIONS = {".flac", ".wav", ".aiff"}
