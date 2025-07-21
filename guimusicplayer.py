import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Music Player")
        self.root.geometry("500x400")

        pygame.mixer.init()

        self.playlist = []
        self.current_index = -1
        self.paused = False

        # Playlist Listbox
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, bg="black", fg="white", width=60)
        self.listbox.pack(pady=20)

        # Control Buttons Frame
        controls_frame = tk.Frame(root)
        controls_frame.pack()

        self.play_btn = tk.Button(controls_frame, text="Play", command=self.play_song)
        self.play_btn.grid(row=0, column=0, padx=10)

        self.pause_btn = tk.Button(controls_frame, text="Pause", command=self.pause_song)
        self.pause_btn.grid(row=0, column=1, padx=10)

        self.stop_btn = tk.Button(controls_frame, text="Stop", command=self.stop_song)
        self.stop_btn.grid(row=0, column=2, padx=10)

        self.prev_btn = tk.Button(controls_frame, text="Previous", command=self.prev_song)
        self.prev_btn.grid(row=0, column=3, padx=10)

        self.next_btn = tk.Button(controls_frame, text="Next", command=self.next_song)
        self.next_btn.grid(row=0, column=4, padx=10)

        # Volume Control
        volume_frame = tk.Frame(root)
        volume_frame.pack(pady=10)

        volume_label = tk.Label(volume_frame, text="Volume")
        volume_label.pack(side=tk.LEFT)

        self.volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(70)
        pygame.mixer.music.set_volume(0.7)
        self.volume_slider.pack(side=tk.LEFT)

        # Menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Songs", command=self.add_songs)
        file_menu.add_command(label="Exit", command=root.quit)

    def add_songs(self):
        files = filedialog.askopenfilenames(title="Select Audio Files", filetypes=(("MP3 Files", "*.mp3"), ("WAV Files", "*.wav"), ("All Files", "*.*")))
        for file in files:
            if file not in self.playlist:
                self.playlist.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))

    def play_song(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            return

        try:
            selected_index = self.listbox.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "Please select a song to play.")
            return

        self.current_index = selected_index
        song = self.playlist[self.current_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.paused = False

    def pause_song(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True

    def stop_song(self):
        pygame.mixer.music.stop()
        self.paused = False

    def next_song(self):
        if self.current_index + 1 < len(self.playlist):
            self.current_index += 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.play_song()

    def prev_song(self):
        if self.current_index - 1 >= 0:
            self.current_index -= 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.play_song()

    def set_volume(self, val):
        volume = int(val) / 100
        pygame.mixer.music.set_volume(volume)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
