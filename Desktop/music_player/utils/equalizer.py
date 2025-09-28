import threading
import random
import numpy as np
from pydub import AudioSegment
from pydub.utils import make_chunks
import tkinter as tk
import pygame

class RealEqualizer:
    def __init__(self, root, audio_path, x=500, y=100, num_bars=30, bar_width=12, max_height=200, divisor=5000):
        self.root = root
        self.audio_path = audio_path
        self.num_bars = num_bars
        self.bar_width = bar_width
        self.max_height = max_height
        self.divisor = divisor
        self.colors = ["#0B3D91", "#4B0082", "#1F305E", "#3A0071", "#2C2C54", "#2A2A72"]

        self.eq_canvas = tk.Canvas(root, width=num_bars*bar_width, height=max_height, bg="#121212", highlightthickness=0)
        self.eq_canvas.place(x=x, y=y)

        self.eq_bars = [self.eq_canvas.create_rectangle(
                            i*bar_width, max_height, i*bar_width+bar_width-2, max_height,
                            fill=random.choice(self.colors))
                        for i in range(num_bars)]

        try:
            self.song = AudioSegment.from_file(audio_path)
            self.chunk_ms = 50
            self.chunks = make_chunks(self.song, self.chunk_ms)
            self.last_values = [0]*num_bars
            # Reproducir canción con pygame
            pygame.mixer.music.load(audio_path)
            threading.Thread(target=self.play_and_update, daemon=True).start()
        except Exception as e:
            print(f"Error al cargar el ecualizador: {e}")
            # Opcional: mostrar mensaje en UI
            tk.Label(self.root, text="Error: No se pudo cargar el ecualizador", bg="#121212", fg="#ff0000").place(x=x, y=y)

    def play_and_update(self):
        pygame.mixer.music.play()
        for chunk in self.chunks:
            if not pygame.mixer.music.get_busy():
                break

            try:
                samples = np.array(chunk.get_array_of_samples())
                fft = np.abs(np.fft.fft(samples))[:len(samples)//2]
                step = max(1, len(fft)//self.num_bars)

                for i in range(self.num_bars):
                    value = np.mean(fft[i*step:(i+1)*step])
                    h = min(int(value/self.divisor), self.max_height)
                    self.last_values[i] = 0.8*self.last_values[i] + 0.2*h

                    self.eq_canvas.coords(self.eq_bars[i],
                                          i*self.bar_width,
                                          self.max_height-self.last_values[i],
                                          i*self.bar_width+self.bar_width-2,
                                          self.max_height)

                    color = "#FF0000" if self.last_values[i] > self.max_height*0.7 else random.choice(self.colors)
                    self.eq_canvas.itemconfig(self.eq_bars[i], fill=color)

                self.root.update()
            except Exception as e:
                print(f"Error en procesamiento de audio: {e}")
                break
