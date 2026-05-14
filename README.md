# DropScribe - drop a file to transcribe

Background service that watches a folder for media files, transcribes them with Whisper, and saves the result as plain text. Runs silently with no console window.

## How it works

1. Drop any supported media file into `in-files/`
2. The service converts it to FLAC via FFmpeg (if needed) and transcribes it with Whisper
3. The transcript appears in `out-transcripts/<filename>.txt`
4. The original file is deleted; `in-files/` goes back to empty

## Requirements

### FFmpeg

Download from [ffmpeg.org](https://ffmpeg.org/download.html) and note the path to `ffmpeg.exe`.

### OpenAI Whisper

```
pip install openai-whisper
```

After install, note the path to `whisper.exe` (usually inside your Python `Scripts/` folder).

## Setup

Edit `src/config.py` and set the two paths to match your machine:

```python
FFMPEG_EXE  = r"C:\...\ffmpeg.exe"
WHISPER_EXE = r"C:\...\whisper.exe"
```

## Running

**With a console (development / debugging):**
```
python src/main.py
```

**Silently in the background (production):**
```
wscript launch.vbs
```

To start automatically on login, place a shortcut to `wscript launch.vbs` in `shell:startup`.

## Stopping

**Option A — PowerShell (by PID file):**
```powershell
Stop-Process -Id (Get-Content in-files\.pid) -Force
```

**Option B — Task Manager:**
Find `pythonw.exe` in the Details tab → right-click → End Task.

> All three options force-kill the process. The next start automatically detects and removes the stale lock file.

## Supported formats

| Category | Extensions |
|---|---|
| Video | `.mp4` `.mkv` `.mov` `.avi` `.webm` `.flv` `.wmv` `.mpeg` `.m4v` `.3gp` `.mxf` |
| Audio | `.mp3` `.aac` `.wav` `.flac` `.ogg` `.m4a` `.opus` `.wma` `.aiff` `.ac3` `.dts` |

Files with any other extension are logged as skipped and left untouched.

## Logs

Every event is appended to `log.txt` at the project root:

```
[2026-05-14 10:00:01] [INFO]  Idle — no files in queue
[2026-05-14 10:00:06] [INFO]  DETECTED  interview.mp4
[2026-05-14 10:00:06] [INFO]  CONVERT   interview.mp4 → _tmp_interview.flac
[2026-05-14 10:00:18] [INFO]  CONVERT_OK
[2026-05-14 10:00:18] [INFO]  TRANSCRIBE _tmp_interview.flac
[2026-05-14 10:02:45] [INFO]  TRANSCRIBE_OK → out-transcripts/interview.txt
[2026-05-14 10:02:45] [INFO]  DONE      interview.mp4 deleted
```
