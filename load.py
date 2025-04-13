#!/usr/bin/env python3
import sys
import os
import time
import requests
from io import BytesIO
from PIL import Image, ImageSequence

try:
    import cv2
except ImportError:
    cv2 = None

# TS: Konvertiert ein PIL-Bild in farbige ASCII-Art – Pixel für Pixel, original in Farbe.
def image_to_color_ascii(image, new_width=120):
    # Stelle sicher, dass das Bild im RGB-Modus ist – ohne Farbe gibt's hier keinen Style.
    image = image.convert("RGB")
    width, height = image.size
    new_height = int(new_width * (height / width) * 0.55)  # 0.55 passt das Seitenverhältnis fürs Terminal an.
    image = image.resize((new_width, new_height))
    
    ascii_chars = "@%#*+=-:. "  # Unsere exklusive Palette – von tiefschwarz bis lichtdurchflutet.
    pixels = list(image.getdata())
    ascii_image = ""
    
    for i in range(new_height):
        line = ""
        for j in range(new_width):
            index = i * new_width + j
            r, g, b = pixels[index]
            # Helligkeitsberechnung im TS-Stil – präzise und dominant.
            brightness = 0.299 * r + 0.587 * g + 0.114 * b
            char_index = int((brightness / 255) * (len(ascii_chars) - 1))
            ascii_char = ascii_chars[char_index]
            # Setze mit ANSI-Escape Sequence die originale Farbe des Pixels.
            line += f"\033[38;2;{r};{g};{b}m{ascii_char}\033[0m"
        ascii_image += line + "\n"
    return ascii_image

# TS: Lädt ein GIF aus dem Memory-Stream, zerlegt es in Frames und spielt es ab – originaler Frame-Delay inklusive.
def animate_gif(stream, new_width=120):
    try:
        im = Image.open(stream)
    except Exception as e:
        print(f"TS: Fehler beim Öffnen des GIFs – {e}")
        sys.exit(1)
    
    frames = []
    delays = []
    
    # Zerlege das GIF in seine Frames, extrahiere den Delay (in ms) und konvertiere jeden Frame.
    for frame in ImageSequence.Iterator(im):
        delay = frame.info.get('duration', 100)  # Standardmäßig 100 ms, wenn nichts angegeben.
        delays.append(delay)
        ascii_frame = image_to_color_ascii(frame, new_width=new_width)
        frames.append(ascii_frame)
    
    avg_delay = sum(delays) / len(delays) if delays else 100
    
    # TS: Spiele jeden Frame ab – im originalen Timing, wie es sein muss.
    for ascii_frame, delay in zip(frames, delays):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_frame)
        time.sleep(delay / 1000.0)
    
    fps = 1000 / avg_delay if avg_delay > 0 else 0
  # TS: Liest Video-Frames mit OpenCV, konvertiert sie in farbige ASCII-Art und spielt sie ab.
def animate_video(video_path, new_width=120):
    if cv2 is None:
        sys.exit(1)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        sys.exit(1)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25  # Fallback-Wert
    delay = 1.0 / fps
    
    # TS: Lies jeden Frame, verarbeite ihn und spiele ihn synchron ab.
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Verwandle den Frame in ein PIL-Bild.
        frame_pil = Image.fromarray(frame)
        ascii_frame = image_to_color_ascii(frame_pil, new_width=new_width)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_frame)
        time.sleep(delay)
    
    cap.release()
    print(f"TS: Video abgespielt mit ca. {fps:.2f} fps (Frame-Delay: {1000/fps:.2f} ms).")

# TS: Hauptprogramm – lädt direkt das Medium von der URL, spielt es ab und beendet sich dann.
def main():
    url = "https://raw.githubusercontent.com/titanxrio/krypta1/refs/heads/main/IMG_9107.GIF"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.content
    except Exception as e:
        sys.exit(1)
    
    ext = os.path.splitext(url)[1].lower()
    if ext == ".gif":
        stream = BytesIO(data)
        animate_gif(stream, new_width=120)
    else:
        # Für Videoformate: Schreibe den Inhalt in eine temporäre Datei, spiele das Video ab und lösche die Datei anschließend.
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        animate_video(tmp_path, new_width=120)
        os.remove(tmp_path)
    

if __name__ == "__main__":
    main()
