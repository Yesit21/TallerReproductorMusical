import sys, os
import math
import threading
import random
import numpy as np
from pydub import AudioSegment
from pydub.utils import make_chunks
import pygame
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# --- Nota: Asegúrate de que FFmpeg esté instalado y en PATH para el ecualizador ---

# --- Ajuste de ruta para encontrar carpetas ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.song import Song
from structures.doubly_linked_list import DoublyLinkedList
from utils.player import Player
from utils.equalizer import RealEqualizer  # Importamos la clase desde el módulo

# ------------------- App principal -------------------
class MusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dub Style DJ Player")
        self.root.geometry("800x600")
        self.root.configure(bg="#121212")

        self.playlist = DoublyLinkedList()
        self.player = Player()

        # --- Cargar imagen por defecto automáticamente ---
        imagenes_dir = os.path.join(os.path.dirname(__file__), "..", "imagenes")
        self.default_img_path = None
        for ext in ("png", "jpg", "jpeg", "bmp", "gif"):
            files = [f for f in os.listdir(imagenes_dir) if f.lower().endswith(ext)]
            if files:
                self.default_img_path = os.path.join(imagenes_dir, files[0])
                break

        if self.default_img_path:
            self.img_original = Image.open(self.default_img_path).resize((200, 200), Image.Resampling.LANCZOS)
            self.img = ImageTk.PhotoImage(self.img_original)
        else:
            self.img_original = None
            self.img = None

        # Título de la canción actual
        self.current_song_label = tk.Label(root, text="No hay canción seleccionada",
                                           bg="#121212", fg="#00ffea", font=("Arial", 16, "bold"))
        self.current_song_label.pack(pady=20)

        # Lista de canciones con scroll
        self.list_frame = tk.Frame(root, bg="#121212")
        self.list_frame.place(x=500, y=350)
        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.listbox = tk.Listbox(self.list_frame, width=30, height=10,
                                  bg="#1e1e1e", fg="#ffffff", font=("Arial", 12),
                                  selectbackground="#00ffea", yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Disco giratorio (imagen)
        self.canvas = tk.Canvas(root, width=400, height=400, bg="#121212", highlightthickness=0)
        self.canvas.place(x=50, y=100)
        self.disco = self.canvas.create_image(200, 200, image=self.img)
        self.angle = 0
        self.animate_disc()

        # Botones alrededor
        self.create_buttons()

        # Barra de volumen
        self.volume_label = tk.Label(root, text="Volumen", bg="#121212", fg="#00ffea", font=("Arial", 12))
        self.volume_label.place(x=500, y=300)
        self.volume = tk.DoubleVar()
        self.volume.set(0.5)
        self.volume_slider = tk.Scale(root, from_=0, to=1, resolution=0.05,
                                      orient=tk.HORIZONTAL, variable=self.volume,
                                      bg="#121212", fg="#00ffea", troughcolor="#1e1e1e",
                                      highlightthickness=0, length=250, command=lambda v: self.adjust_volume())
        self.volume_slider.place(x=500, y=320)

    # ------------------- Funciones -------------------
    def create_buttons(self):
        btn_texts = ["+", "<<", "Play", "Pause", "Stop", ">>", "Shuffle", "Repeat", "EQ"]
        radius = 180
        center_x, center_y = 200, 200
        for i, text in enumerate(btn_texts):
            angle = math.radians(i * 360 / len(btn_texts))
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            btn = tk.Button(self.canvas, text=text, bg="#1e1e1e", fg="#00ffea",
                            width=6, height=2, font=("Arial", 12, "bold"))
            self.canvas.create_window(x, y, window=btn)
            if text == "Play": btn.config(command=self.play_song)
            elif text == "Pause": btn.config(command=self.pause_song)
            elif text == "Stop": btn.config(command=self.stop_song)
            elif text == "<<": btn.config(command=self.prev_song)
            elif text == ">>": btn.config(command=self.next_song)
            elif text == "+": btn.config(command=self.add_song)
            elif text == "Shuffle": btn.config(command=self.shuffle_playlist)
            elif text == "Repeat": btn.config(command=self.toggle_repeat)
            elif text == "EQ": btn.config(command=self.open_equalizer)

    def animate_disc(self):
        if not self.img_original:
            return
        self.angle = (self.angle + 5) % 360
        rotated = self.img_original.rotate(self.angle)
        self.img = ImageTk.PhotoImage(rotated)
        self.canvas.itemconfig(self.disco, image=self.img)
        self.root.after(50, self.animate_disc)

    def update_cover(self, song):
        if song and hasattr(song, "cover_path") and song.cover_path and os.path.exists(song.cover_path):
            img_path = song.cover_path
        else:
            img_path = self.default_img_path

        if img_path:
            self.img_original = Image.open(img_path).resize((200, 200), Image.Resampling.LANCZOS)
            self.img = ImageTk.PhotoImage(self.img_original)
            self.canvas.itemconfig(self.disco, image=self.img)

    def adjust_volume(self):
        self.player.set_volume(self.volume.get())

    def add_song(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de música", "*.mp3")])
        if file_path:
            if not os.path.exists(file_path) or not file_path.lower().endswith('.mp3'):
                tk.messagebox.showerror("Error", "Archivo de música inválido")
                return
            title = os.path.basename(file_path)
            song = Song(title, "Desconocido", file_path)
            cover_path = filedialog.askopenfilename(title="Selecciona portada (opcional)",
                                                    filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
            if cover_path:
                if not os.path.exists(cover_path) or not any(cover_path.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']):
                    tk.messagebox.showerror("Error", "Archivo de imagen inválido")
                    return
                song.cover_path = cover_path
            self.playlist.add_song_end(song)
            self.listbox.insert(tk.END, str(song))

    def play_song(self):
        current = self.playlist.get_current()
        if current:
            if not os.path.exists(current.path):
                tk.messagebox.showerror("Error", "Archivo de música no encontrado")
                return
            self.player.play(current.path)
            self.current_song_label.config(text=f"Play {current.title}")
            self.update_cover(current)

    def pause_song(self):
        if self.player.playing:
            self.player.pause()
        else:
            self.player.unpause()

    def stop_song(self):
        self.player.stop()
        self.current_song_label.config(text="No hay canción seleccionada")
        self.update_cover(None)

    def next_song(self):
        next_s = self.playlist.next_song()
        if next_s:
            self.player.play(next_s.path)
            self.current_song_label.config(text=f"Play {next_s.title}")
            self.update_cover(next_s)

    def prev_song(self):
        prev_s = self.playlist.prev_song()
        if prev_s:
            self.player.play(prev_s.path)
            self.current_song_label.config(text=f"Play {prev_s.title}")
            self.update_cover(prev_s)

    def open_equalizer(self):
        current = self.playlist.get_current()
        if current:
            RealEqualizer(self.root, current.path, x=500, y=100)

    def shuffle_playlist(self):
        self.playlist.shuffle()
        self.update_listbox()

    def toggle_repeat(self):
        self.playlist.toggle_repeat()
        status = "Activado" if self.playlist.repeat else "Desactivado"
        tk.messagebox.showinfo("Repeat", f"Modo repeat {status}")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        node = self.playlist.head
        while node:
            self.listbox.insert(tk.END, str(node.song))
            node = node.next

# ------------------- Bloque principal -------------------
if __name__ == "__main__":
    pygame.mixer.init()
    root = tk.Tk()
    app = MusicApp(root)
    root.mainloop()
