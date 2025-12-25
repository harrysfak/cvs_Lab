import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk, ImageSequence

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
GIF_LOAD = ASSETS_DIR / "gifs" / "load.gif"
GIF_PROCESS = ASSETS_DIR / "gifs" / "data_process.gif"
GIF_SUCCESS = ASSETS_DIR / "gifs" / "success.gif"

class AnimatedGIF(tk.Label):
    def __init__(self, parent, gif_path, size=(32, 32), delay=80, **kw):
        super().__init__(parent, **kw)
        self.gif_path = Path(gif_path)
        self.size = size
        self.delay = delay
        self._frames = []
        self._idx = 0
        self._job = None
        self._load_frames()
        if self._frames:
            self.configure(image=self._frames[0])

    def _load_frames(self):
        self._frames.clear()
        if not self.gif_path.exists():
            return
        im = Image.open(self.gif_path)
        for frame in ImageSequence.Iterator(im):
            fr = frame.convert("RGBA").resize(self.size)
            self._frames.append(ImageTk.PhotoImage(fr))

    def start(self):
        if self._job or not self._frames:
            return
        self._tick()

    def stop(self):
        if self._job:
            self.after_cancel(self._job)
            self._job = None

    def _tick(self):
        self._idx = (self._idx + 1) % len(self._frames)
        self.configure(image=self._frames[self._idx])
        self._job = self.after(self.delay, self._tick)

class StatusSlot(tk.Frame):
    def __init__(self, parent, bg=None, w=90, h=70):
        super().__init__(parent, bg=bg, width=w, height=h)
        self.bg = bg
        self.widget = None
        self.pack_propagate(False)

    def show_gif(self, gif_path, size=(56, 56), delay=80):
        self.clear()

        w = AnimatedGIF(self, gif_path, size=size, delay=delay, bg=self.bg)
        w.pack(expand=True)
        print("FRAMES:", len(w._frames))
        print("GIF PATH:", gif_path)

        w.start()
        print("FRAMES:", len(w._frames))

        self.widget = w

    def show_success_for(self, gif_path, ms=1500, size=(32, 32)):
        self.show_gif(gif_path, size=size, delay=60)
        self.after(ms, self.clear)

    def clear(self):
        if self.widget and hasattr(self.widget, "stop"):
            self.widget.stop()
        for c in self.winfo_children():
            c.destroy()
        self.widget = None
