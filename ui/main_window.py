"""Main window built with customtkinter."""
import threading
from pathlib import Path
from tkinter import filedialog
import customtkinter as ctk
from core.image_converter import IMAGE_FORMATS, convert_image
from core.media_converter import AUDIO_FORMATS, VIDEO_FORMATS, convert_media, detect_type

FORMATS_BY_KIND = {
    "image": IMAGE_FORMATS,
    "audio": AUDIO_FORMATS,
    "video": VIDEO_FORMATS,
}

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Media Converter")
        self.geometry("520x380")
        self.resizable(False, False)

        self.src_path: str | None = None
        self.kind: str | None = None
        self.out_dir: str | None = None

        self._build_widgets()

    def _build_widgets(self):
        pad = {"padx": 20, "pady": 8}

        ctk.CTkLabel(self, text="Media Converter", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 10))

        self.select_btn = ctk.CTkButton(self, text="Select file...", command=self.select_file)
        self.select_btn.pack(**pad)

        self.file_label = ctk.CTkLabel(self, text="No file selected", wraplength=460)
        self.file_label.pack(**pad)

        self.format_menu = ctk.CTkOptionMenu(self, values=["-"], state="disabled")
        self.format_menu.pack(**pad)

        self.out_btn = ctk.CTkButton(self, text="Output folder (default: same as file)",
                                     fg_color="transparent", border_width=1,
                                     command=self.select_output_dir)
        self.out_btn.pack(**pad)

        self.convert_btn = ctk.CTkButton(self, text="Convert", state="disabled", command=self.start_conversion)
        self.convert_btn.pack(**pad)

        self.progress = ctk.CTkProgressBar(self, mode="indeterminate", width=300)
        self.progress.pack(**pad)
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(self, text="", wraplength=460)
        self.status_label.pack(**pad)

    def select_file(self):
        path = filedialog.askopenfilename(
            title="Select a media file",
            filetypes=[
                ("Media files", "*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tiff *.ico "
                                "*.mp3 *.wav *.flac *.aac *.ogg *.m4a *.wma *.opus "
                                "*.mp4 *.mkv *.avi *.mov *.webm *.wmv *.flv"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        kind = detect_type(path)
        if kind is None:
            self.status_label.configure(text="Unsupported file type.", text_color="red")
            return

        self.src_path, self.kind = path, kind
        self.file_label.configure(text=f"{Path(path).name}  ({kind})")

        formats = list(FORMATS_BY_KIND[kind].keys())
        self.format_menu.configure(values=formats, state="normal")
        self.format_menu.set(formats[0])
        self.convert_btn.configure(state="normal")
        self.status_label.configure(text="")

    def select_output_dir(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.out_dir = folder
            self.out_btn.configure(text=f"Output: {folder}")

    def start_conversion(self):
        if self.src_path is None or self.kind is None:
            return

        self.convert_btn.configure(state="disabled")
        self.status_label.configure(text="Converting...", text_color=("black", "white"))
        self.progress.start()

        target = self.format_menu.get()
        threading.Thread(
        target=self._convert_worker,
        args=(self.src_path, self.kind, target),
        daemon=True,
    ).start()

    def _convert_worker(self, src: str, kind: str, target: str):
        try:
            if kind == "image":
                result = convert_image(src, target, self.out_dir)
            else:
                result = convert_media(src, kind, target, self.out_dir)
            self.after(0, self._on_done, f"Done: {result}", False)
        except Exception as exc:
            self.after(0, self._on_done, f"Error: {exc}", True)

    def _on_done(self, message: str, is_error: bool):
        self.progress.stop()
        self.progress.set(0)
        self.convert_btn.configure(state="normal")
        self.status_label.configure(text=message, text_color="red" if is_error else "green")