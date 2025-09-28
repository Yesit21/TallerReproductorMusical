import pygame

class Player:
    def __init__(self):
        pygame.mixer.init()
        self.playing = False
        self.volume = 0.5  # volumen inicial
        pygame.mixer.music.set_volume(self.volume)

    def play(self, song_path):
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def pause(self):
        pygame.mixer.music.pause()
        self.playing = False

    def unpause(self):
        pygame.mixer.music.unpause()
        self.playing = True

    def set_volume(self, value):
        """Recibe un valor de 0.0 a 1.0"""
        self.volume = value
        pygame.mixer.music.set_volume(self.volume)
