import shutil
import subprocess
import sys
from pathlib import Path
from core.image_converter import IMAGE_FORMATS

AUDIO_FORMATS = {
    "MP3": ".mp3",
    "WAV": ".wav",
    "FLAC": ".flac",
    "AAC": ".aac",
    "OGG": ".ogg",
    "M4A": ".m4a",
}

VIDEO_FORMATS = {
    "MP4": ".mp4",
    "MKV": ".mkv",
    "AVI": ".avi",
    "MOV": ".mov",
    "WEBM": ".webm",
    "GIF": ".gif",
}

_IMAGE_EXTS = set(IMAGE_FORMATS.values()) | {".jpeg", ".tif", ".jfif"}
_AUDIO_EXTS = set(AUDIO_FORMATS.values()) | {".wma", ".opus"}
_VIDEO_EXTS = set(VIDEO_FORMATS.values()) | {".wmv", ".flv", ".m4v", ".mpg", ".mpeg"}


def detect_type(path: str) -> str | None:
    ext = Path(path).suffix.lower()
    if ext in _IMAGE_EXTS:
        return "image"
    if ext in _AUDIO_EXTS:
        return "audio"
    if ext in _VIDEO_EXTS:
        return "video"
    return None


def get_ffmpeg() -> str:
    system = shutil.which("ffmpeg")
    if system:
        return system
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:
        raise RuntimeError(
            "ffmpeg not found. Install it (e.g. 'winget install ffmpeg') "
            "or run 'pip install imageio-ffmpeg'."
        ) from exc


def convert_media(src: str, kind: str, target_format: str, out_dir: str | None = None) -> Path:
    formats = AUDIO_FORMATS if kind == "audio" else VIDEO_FORMATS
    src_path = Path(src)
    out_folder = Path(out_dir) if out_dir else src_path.parent
    dst_path = out_folder / (src_path.stem + formats[target_format])


    if dst_path.resolve() == src_path.resolve():
        dst_path = dst_path.with_name(dst_path.stem + "_converted" + dst_path.suffix)

    cmd = [get_ffmpeg(), "-y", "-i", str(src_path)]
    if kind == "audio":
        cmd.append("-vn")
    cmd.append(str(dst_path))

    flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    result = subprocess.run(cmd, capture_output=True, text=True, creationflags=flags)

    if result.returncode != 0:
        last_lines = "\n".join(result.stderr.strip().splitlines()[-5:])
        raise RuntimeError(f"ffmpeg failed:\n{last_lines}")

    return dst_path