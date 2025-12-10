import tkinter as tk
import ctypes

class BaseWindow(tk.Toplevel):
    def __init__(self, title, width, height, bg_color="#f0f0f0"):
        super().__init__()
        
        # ENCAPSULATION: Window setup details are hidden here
        self.title(title)
        self.configure(bg=bg_color)
        self.center_window(width, height)
        self.apply_dark_mode()

    def center_window(self, width, height):
        # ABSTRACTION: The math is hidden from the main logic
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(screen_width/2 - width/2)
        y = int(screen_height/2 - height/2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def apply_dark_mode(self):
        # Dark Mode Hack
        try:
            self.update()
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ctypes.windll.user32.GetParent
            hwnd = get_parent(self.winfo_id())
            value = ctypes.c_int(2)
            set_window_attribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
        except:
            pass

    # Method meant to be overridden (Polymorphism)
    def run(self):
        self.mainloop()