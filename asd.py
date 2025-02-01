import re
import time
import lyricsgenius
import tkinter as tk
from threading import Thread
import pythoncom
import keyboard
from pycaw.pycaw import AudioUtilities
from pygetwindow import getWindowsWithTitle

genius = lyricsgenius.Genius("3r2SgLSRJQo4FDtUuMoPiMs2znLgfx9ME6vlIpHbte9GPWzH4vbIxbYHuIbmH6fZ")

is_paused = False
is_visible = True
speed_multiplier = 1.0  # Varsayılan hız çarpanı (pop şarkılar)

def extract_song_name(title):
    cleaned_title = re.sub(r"(\s*-\s*(YouTube|Google Chrome).*)", "", title)
    match = re.match(r"^(.*?)(?:\s*\s*(.*))?$", cleaned_title)
    return match.group(2) if match and match.group(2) else match.group(1) if match else title

def get_lyrics(song_name):
    try:
        song = genius.search_song(song_name)
        return song.lyrics.split("\n") if song else ["Şarkı sözleri bulunamadı."]
    except Exception as e:
        return [f"Hata: {e}"]

def get_media_info():
    pythoncom.CoInitialize()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            process_name = session.Process.name().lower()
            if process_name in ["chrome.exe", "vlc.exe", "spotify.exe", "mspmsnsv.exe"]:
                windows = getWindowsWithTitle(process_name.replace('.exe', ''))
                return windows[0].title if windows else None
    return None

def update_song():
    global lyrics, current_lyric_index
    lyrics.clear()
    current_lyric_index = 0
    lyrics_text.set("")

    media_info = get_media_info()
    if media_info:
        song_name = extract_song_name(media_info)
        lyrics = get_lyrics(song_name)
        if lyrics:
            Thread(target=show_lyrics, args=(lyrics,)).start()
        else:
            lyrics_text.set("Şarkı sözleri bulunamadı.")
    else:
        lyrics_text.set("Çalan medya yok.")

def show_lyrics(lyrics):
    global current_lyric_index, is_paused
    while current_lyric_index < len(lyrics):
        while is_paused:
            time.sleep(0.5)
        lyrics_text.set(lyrics[current_lyric_index])

        sleep_time = (0.9 * len(lyrics[current_lyric_index].split())) / speed_multiplier
        time.sleep(sleep_time)
        current_lyric_index += 1

def set_speed(speed):
    global speed_multiplier
    speed_multiplier = speed

def next_line():
    global current_lyric_index
    if current_lyric_index < len(lyrics) - 1:
        current_lyric_index += 1
        lyrics_text.set(lyrics[current_lyric_index])

def previous_line():
    global current_lyric_index
    if current_lyric_index > 0:
        current_lyric_index -= 1
        lyrics_text.set(lyrics[current_lyric_index])

def pause_lyrics(event):
    global is_paused
    is_paused = True

def resume_lyrics(event):
    global is_paused
    is_paused = False

def hide_window():
    global is_visible
    if is_visible:
        root.geometry("1x1+0+0")
        root.attributes("-alpha", 0.0)
        is_visible = False

def show_window():
    global is_visible
    if not is_visible:
        root.geometry("350x250+0+0")
        root.attributes("-alpha", 0.85)
        is_visible = True

def listen_keyboard():
    while True:
        if keyboard.is_pressed("insert"):
            hide_window()
            time.sleep(0.3)
        elif keyboard.is_pressed("f1"):
            show_window()
            time.sleep(0.3)

def create_gui():
    global lyrics_text, current_lyric_index, lyrics, root
    current_lyric_index = 0
    lyrics = []

    root = tk.Tk()
    root.title("Live Lyrics")
    root.geometry("350x300+0+0")
    root.configure(bg="#1E1E1E")
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.85)
    root.overrideredirect(True)

    tk.Label(root, text="Canlı Şarkı Sözleri", font=("Segoe UI", 12, "bold"), fg="#E0E0E0", bg="#1E1E1E").pack(pady=5)

    lyrics_text = tk.StringVar()
    lyrics_display = tk.Label(root, textvariable=lyrics_text, wraplength=320, height=4, width=40,
                              font=("Segoe UI", 10), fg="#BB86FC", bg="#2C2C2C", relief="groove", padx=5, pady=5)
    lyrics_display.pack(pady=5)

    button_frame = tk.Frame(root, bg="#1E1E1E")
    button_frame.pack(pady=5)

    button_style = {"font": ("Segoe UI", 10), "width": 12, "bd": 0, "relief": "raised"}

    tk.Button(button_frame, text="⏪ Önceki", command=previous_line, fg="white", bg="#B00020",
              activebackground="#790000", **button_style).grid(row=0, column=0, padx=2)

    tk.Button(button_frame, text="🎵 Getir", command=lambda: Thread(target=update_song).start(),
              fg="white", bg="#03DAC6", activebackground="#018786", **button_style).grid(row=0, column=1, padx=2)

    tk.Button(button_frame, text="⏩ Sonraki", command=next_line, fg="white", bg="#6200EE",
              activebackground="#3700B3", **button_style).grid(row=0, column=2, padx=2)

    speed_frame = tk.Frame(root, bg="#1E1E1E")
    speed_frame.pack(pady=5)

    tk.Button(speed_frame, text="🚀 Hızlı", command=lambda: set_speed(1.5), fg="white", bg="#FF0266",
              activebackground="#C51162", **button_style).grid(row=0, column=0, padx=2)

    tk.Button(speed_frame, text="🎤 Pop", command=lambda: set_speed(1.0), fg="white", bg="#03A9F4",
              activebackground="#0277BD", **button_style).grid(row=0, column=1, padx=2)

    tk.Button(speed_frame, text="🐢 Yavaş", command=lambda: set_speed(0.7), fg="white", bg="#FFC107",
              activebackground="#FF9800", **button_style).grid(row=0, column=2, padx=2)

    pause_button = tk.Button(root, text="⏸️ Durdur (Basılı Tut)", font=("Segoe UI", 10), fg="black",
                             bg="#FFCA28", activebackground="#FFB300", width=30, bd=0, relief="raised")
    pause_button.pack(pady=5)

    pause_button.bind("<ButtonPress>", pause_lyrics)
    pause_button.bind("<ButtonRelease>", resume_lyrics)

    Thread(target=listen_keyboard, daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
