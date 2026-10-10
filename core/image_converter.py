from pathlib import Path
from PIL import Image

IMAGE_FORMATS = {
    "PNG": ".png",
    "JPG": ".jpg",
    "WEBP": ".webp",
    "BMP": ".bmp",
    "GIF": ".gif",
    "TIFF": ".tiff",
    "ICO": ".ico",
}

_PILLOW_NAMES = {"JPG": "JPEG"}
_NO_ALPHA = {"JPG", "BMP"}

def convert_image(src: str, target_format: str, out_dir: str | None = None) -> Path:
    src_path = Path(src)
    out_folder = Path(out_dir) if out_dir else src_path.parent
    dst_path = out_folder / (src_path.stem + IMAGE_FORMATS[target_format])

    with Image.open(src_path) as img:
        if target_format in _NO_ALPHA and img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")  # drop transparency, otherwise saving fails
        img.save(dst_path, format=_PILLOW_NAMES.get(target_format, target_format))

    return dst_path