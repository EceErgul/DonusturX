# DönüştürX 🚀

**DönüştürX** is a modern, sleek, and user-friendly desktop media conversion application built with Python and CustomTkinter. It allows you to seamlessly convert your image, audio, and video files into various popular formats under one unified interface.

---

## Features ✨

- **Image Conversion:** Fast and lossless conversion between PNG, JPG, WEBP, BMP, and other major image formats using the Pillow library.
- **Audio & Video Conversion:** Robust multimedia format switching supporting MP4, AVI, MKV, MP3, WAV, and more via MoviePy and FFmpeg.
- **Modern UI:** Designed with CustomTkinter, featuring clean dark/light mode support and a responsive layout.
- **Modular Architecture:** Cleanly separated business logic (`core`) and user interface (`ui`) layers for high maintainability.

---

- ## Project Architecture 🗂️

DonusturX/
│
├── core/                   # Business logic and conversion engine
│   ├── __init__.py
│   ├── image_converter.py  # Image format conversion logic
│   └── media_converter.py  # Audio and video format conversion logic
│
├── ui/                     # User interface components
│   ├── __init__.py
│   └── main_window.py      # CustomTkinter main window and UI design
│
├── main.py                 # Main entry point of the application
├── requirements.txt        # Project dependencies list
└── .gitignore              # Git ignored files configuration

---

## Installation and Setup ⚙️

Follow these steps to set up and run the project locally on your machine:

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/KULLANICI_ADIN/DonusturX.git](https://github.com/KULLANICI_ADIN/DonusturX.git)
   cd DonusturX
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv .venv
   ```

  # On Windows:
  ```bash
  .venv\Scripts\activate
  ```

  # On macOS / Linux:
  ```bash
  source .venv/bin/activate
  ```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the Application:**
   ```bash
   python main.py
   ```

   ## Technologies Used 🛠️

- **Python** (Programming Language)
- **CustomTkinter** (Modern UI Library)
- **Pillow (PIL)** (Image Processing Library)
- **MoviePy** (Media and Video Processing Library)

---

## License 📄
This project is open-source and available under the MIT License. Feel free to use, modify, and distribute it as you like.
