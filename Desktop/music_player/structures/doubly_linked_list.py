import random

class Node:
    def __init__(self, song):
        self.song = song
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.repeat = False  # Modo repeat all

    def add_song_end(self, song):
        new_node = Node(song)
        if not self.head:
            self.head = self.tail = new_node
            self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def remove_current(self):
        if not self.current:
            return None
        song_removed = self.current.song

        if self.current == self.head:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
        elif self.current == self.tail:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            self.current.prev.next = self.current.next
            self.current.next.prev = self.current.prev

        self.current = self.head
        return song_removed

    def next_song(self):
        if self.current and self.current.next:
            self.current = self.current.next
        elif self.repeat and self.head:
            self.current = self.head
        return self.current.song if self.current else None

    def prev_song(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        elif self.repeat and self.tail:
            self.current = self.tail
        return self.current.song if self.current else None

    def get_current(self):
        return self.current.song if self.current else None

    def shuffle(self):
        if not self.head:
            return
        songs = []
        node = self.head
        while node:
            songs.append(node.song)
            node = node.next
        random.shuffle(songs)
        # Reconstruir lista
        self.head = self.tail = self.current = None
        for song in songs:
            self.add_song_end(song)

    def toggle_repeat(self):
        self.repeat = not self.repeat
