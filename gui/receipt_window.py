import tkinter as tk
from tkinter import ttk
import ctypes
import random

# THEME CONSTANTS
BG_COLOR = "#121212"
SURFACE_COLOR = "#1E1E1E"
TEXT_MAIN = "#FFFFFF"
TEXT_SUB = "#B3B3B3"
ACCENT = "#BB86FC"
ACCENT_DARK = "#3700B3"
SUCCESS_COLOR = "#03DAC6"

class ReceiptWindow:
    def __init__(self, booking_id, movie_title, showtime_str, seats, total, hall_name):
        self.window = tk.Toplevel()
        self.window.title("Booking Confirmed")
        self.window.configure(bg=BG_COLOR)
        
        # Sizing
        w, h = 450, 750 # Slightly taller for the larger QR
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = int(sw/2 - w/2)
        y = int(sh/2 - h/2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")

        # Dark Title Bar
        try:
            self.window.update()
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ctypes.windll.user32.GetParent
            hwnd = get_parent(self.window.winfo_id())
            value = ctypes.c_int(2)
            set_window_attribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
        except: pass

        self.booking_id = booking_id
        self.movie_title = movie_title
        self.showtime_str = showtime_str
        self.hall_name = hall_name
        self.total = total
        self.seat_str = ", ".join([f"{r}{n}" for r, n in seats])

        # Prepare Text for Printing
        self.receipt_text = (
            f"----------------------------------------\n"
            f"       SCREENPASS DIGITAL TICKET        \n"
            f"----------------------------------------\n"
            f"ID     : #{self.booking_id}\n"
            f"MOVIE  : {self.movie_title}\n"
            f"HALL   : {self.hall_name}\n"
            f"TIME   : {self.showtime_str}\n"
            f"SEATS  : {self.seat_str}\n"
            f"----------------------------------------\n"
            f"TOTAL  : ₱{self.total:,.2f}\n"
            f"----------------------------------------\n"
        )

        # ==========================================
        # UI: SUCCESS HEADER
        # ==========================================
        tk.Label(
            self.window, text="✔ Booking Confirmed", 
            font=("Helvetica", 18, "bold"), fg=SUCCESS_COLOR, bg=BG_COLOR
        ).pack(pady=(25, 5))
        
        tk.Label(
            self.window, text="Your tickets are ready.", 
            font=("Helvetica", 10), fg=TEXT_SUB, bg=BG_COLOR
        ).pack(pady=(0, 20))

        # ==========================================
        # UI: THE "DIGITAL TICKET" CARD
        # ==========================================
        ticket_frame = tk.Frame(self.window, bg=SURFACE_COLOR, padx=20, pady=20)
        ticket_frame.pack(fill="x", padx=30)

        # Movie Title
        tk.Label(ticket_frame, text=self.movie_title, font=("Helvetica", 16, "bold"), fg=TEXT_MAIN, bg=SURFACE_COLOR, wraplength=350).pack(anchor="w")
        tk.Label(ticket_frame, text=f"{self.hall_name} • {self.showtime_str}", font=("Helvetica", 10), fg=ACCENT, bg=SURFACE_COLOR).pack(anchor="w", pady=(5, 15))

        # Divider
        tk.Label(ticket_frame, text="- - - - - - - - - - - - - - - - - - - - - - - - - - - -", fg="#444", bg=SURFACE_COLOR).pack(fill="x")

        # Details Grid
        details_grid = tk.Frame(ticket_frame, bg=SURFACE_COLOR)
        details_grid.pack(fill="x", pady=15)

        def add_detail(parent, label, value, row, col):
            tk.Label(parent, text=label.upper(), font=("Helvetica", 8, "bold"), fg="#666", bg=SURFACE_COLOR).grid(row=row, column=col, sticky="w", pady=(0,2))
            tk.Label(parent, text=value, font=("Helvetica", 12, "bold"), fg=TEXT_MAIN, bg=SURFACE_COLOR).grid(row=row+1, column=col, sticky="w", pady=(0, 10), padx=(0, 20))

        add_detail(details_grid, "Booking ID", f"#{self.booking_id}", 0, 0)
        add_detail(details_grid, "Total Paid", f"₱{self.total:,.2f}", 0, 1)
        add_detail(details_grid, "Seats", self.seat_str, 2, 0)

        # -----------------------------------------------
        # REALISTIC FAKE QR CODE
        # -----------------------------------------------
        # Increased size and pixel density
        qr_size = 140
        pixel_size = 4 
        grid_dim = qr_size // pixel_size # 35x35 grid

        qr_frame = tk.Frame(ticket_frame, bg="white", width=qr_size, height=qr_size)
        qr_frame.pack(pady=15)
        qr_frame.pack_propagate(False)
        
        qr_canvas = tk.Canvas(qr_frame, width=qr_size, height=qr_size, bg="white", highlightthickness=0)
        qr_canvas.pack()

        # Generate dense noise
        for r in range(grid_dim):
            for c in range(grid_dim):
                # 50% chance of black pixel
                if random.random() > 0.5:
                    x1 = c * pixel_size
                    y1 = r * pixel_size
                    qr_canvas.create_rectangle(x1, y1, x1+pixel_size, y1+pixel_size, fill="black", outline="")
        
        # Add "Finder Patterns" (The big squares in corners for realism)
        def draw_finder(cx, cy):
            # Outer box 7x7 pixels
            size = 7 * pixel_size
            qr_canvas.create_rectangle(cx, cy, cx+size, cy+size, fill="black")
            # Inner white 5x5
            qr_canvas.create_rectangle(cx+pixel_size, cy+pixel_size, cx+size-pixel_size, cy+size-pixel_size, fill="white")
            # Inner black 3x3
            qr_canvas.create_rectangle(cx+(2*pixel_size), cy+(2*pixel_size), cx+size-(2*pixel_size), cy+size-(2*pixel_size), fill="black")

        draw_finder(0, 0) # Top Left
        draw_finder(qr_size - (7*pixel_size), 0) # Top Right
        draw_finder(0, qr_size - (7*pixel_size)) # Bottom Left

        # ==========================================
        # ACTION BUTTONS
        # ==========================================
        btn_frame = tk.Frame(self.window, bg=BG_COLOR)
        btn_frame.pack(side="bottom", pady=30, fill="x", padx=30)

        # Print Button (Secondary)
        tk.Button(
            btn_frame, 
            text="🖨 Print Ticket", 
            font=("Helvetica", 10, "bold"),
            bg="#333", fg="#FFF", 
            relief="flat", pady=10, width=15,
            cursor="hand2",
            command=self.print_to_console
        ).pack(side="left")

        # Done Button (Primary)
        tk.Button(
            btn_frame, 
            text="Done", 
            font=("Helvetica", 10, "bold"),
            bg=ACCENT, fg="#000", 
            activebackground=ACCENT_DARK, activeforeground="#FFF",
            relief="flat", pady=10, width=15,
            cursor="hand2",
            command=self.close_all
        ).pack(side="right")

    def print_to_console(self):
        """ Simulates printing without interrupting UI """
        print(self.receipt_text)
        # Optional: Update the button text momentarily to say "Printed!" 
        # but standard behavior is usually silent success.

    def close_all(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()
