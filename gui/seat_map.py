import tkinter as tk
from tkinter import messagebox, simpledialog
import ctypes
from gui.receipt_window import ReceiptWindow
from db.queries import get_taken_seats, save_booking

# THEME
BG_COLOR = "#121212"
SURFACE_COLOR = "#1E1E1E"
TEXT_MAIN = "#FFFFFF"
ACCENT = "#BB86FC"
ACCENT_DARK = "#3700B3"
SEAT_AVAILABLE = "#333333"
SEAT_SELECTED = ACCENT
SEAT_TAKEN = "#CF6679"

class SeatMap:
    def __init__(self, showtime_data):
        self.showtime = showtime_data
        self.window = tk.Toplevel()
        self.window.configure(bg=BG_COLOR)
        
        # 1. DYNAMIC SIZING
        cols = self.showtime['total_cols']
        rows = self.showtime['total_rows']
        
        # Calculate ideal size
        width = max(900, cols * 55 + 200)
        height = max(700, rows * 55 + 250)
        
        # Center Window
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = int(screen_width/2 - width/2)
        center_y = int(screen_height/2 - height/2)
        
        self.window.geometry(f"{width}x{height}+{center_x}+{center_y}")
        self.window.title(f"Select Seats - {self.showtime['hall_name']}")

        # Dark Title Bar
        try:
            self.window.update()
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ctypes.windll.user32.GetParent
            hwnd = get_parent(self.window.winfo_id())
            value = ctypes.c_int(2)
            set_window_attribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
        except: pass

        # Data
        self.selected_seats = [] 
        self.taken_seats = get_taken_seats(self.showtime['id'])

        # ==========================================
        # HEADER
        # ==========================================
        header_frame = tk.Frame(self.window, bg=BG_COLOR, pady=20)
        header_frame.pack(fill="x")
        
        # Movie Title (If passed)
        movie_title = self.showtime.get('movie_title', 'Movie Selection')
        tk.Label(header_frame, text=movie_title, font=("Helvetica", 20, "bold"), fg=TEXT_MAIN, bg=BG_COLOR).pack()
        
        # Details
        time_str = self.showtime['start_time'].strftime("%I:%M %p")
        sub_text = f"{self.showtime['hall_name']}  •  {time_str}  •  ₱{self.showtime['price_standard']}"
        tk.Label(header_frame, text=sub_text, font=("Helvetica", 12), fg="#888", bg=BG_COLOR).pack(pady=(5,0))

        # ==========================================
        # SCREEN VISUAL
        # ==========================================
        screen_frame = tk.Frame(self.window, bg=BG_COLOR)
        screen_frame.pack(fill="x", pady=(10, 30))
        
        # The "Screen" Bar - using a canvas to draw a trapezoid/curve effect
        canvas_screen = tk.Canvas(screen_frame, height=40, bg=BG_COLOR, highlightthickness=0)
        canvas_screen.pack(expand=True, fill="x", padx=100)
        
        # Draw trapezoid to simulate screen perspective
        w = width - 200
        canvas_screen.create_polygon(
            0, 0, w, 0,  # Top corners
            w-40, 30, 40, 30, # Bottom corners (tapered in)
            fill="#333", outline=""
        )
        canvas_screen.create_text(w/2, 15, text="SCREEN", fill="#000", font=("Helvetica", 10, "bold"))

        # ==========================================
        # SEAT GRID
        # ==========================================
        self.grid_frame = tk.Frame(self.window, bg=BG_COLOR)
        self.grid_frame.pack()

        for r in range(rows):
            row_label = chr(65 + r)
            
            # Row Label (Left)
            tk.Label(self.grid_frame, text=row_label, fg="#555", bg=BG_COLOR, font=("Arial", 10, "bold")).grid(row=r, column=0, padx=10)
            
            for c in range(cols):
                seat_num = c + 1
                is_taken = (row_label, seat_num) in self.taken_seats
                
                # Determine Style
                if is_taken:
                    bg = BG_COLOR
                    fg = SEAT_TAKEN
                    relief = "flat"
                    text = "✖" # X mark for taken
                    state = "disabled"
                    cursor = "arrow"
                else:
                    bg = SEAT_AVAILABLE
                    fg = TEXT_MAIN
                    relief = "flat"
                    text = str(seat_num)
                    state = "normal"
                    cursor = "hand2"

                btn = tk.Button(
                    self.grid_frame,
                    text=text,
                    width=4, height=2,
                    bg=bg, fg=fg,
                    activebackground=ACCENT, activeforeground="#000",
                    relief=relief, bd=0,
                    state=state, cursor=cursor,
                    font=("Arial", 9)
                )
                
                # Store coordinates in the button for the click handler
                btn.configure(command=lambda r=row_label, n=seat_num, b=btn: self.toggle_seat(r, n, b))
                
                # Grid placement (Column + 1 to account for Row Label)
                btn.grid(row=r, column=c+1, padx=3, pady=3)
            
            # Row Label (Right)
            tk.Label(self.grid_frame, text=row_label, fg="#555", bg=BG_COLOR, font=("Arial", 10, "bold")).grid(row=r, column=cols+2, padx=10)

        # ==========================================
        # FOOTER (Total & Action)
        # ==========================================
        footer_frame = tk.Frame(self.window, bg=SURFACE_COLOR, height=80)
        footer_frame.pack(side="bottom", fill="x")
        footer_frame.pack_propagate(False) # Force height

        # Legend
        legend_frame = tk.Frame(footer_frame, bg=SURFACE_COLOR)
        legend_frame.pack(side="left", padx=40)
        
        self.create_legend_dot(legend_frame, SEAT_AVAILABLE, "Available")
        self.create_legend_dot(legend_frame, SEAT_SELECTED, "Selected")
        self.create_legend_dot(legend_frame, SEAT_TAKEN, "Sold", is_text=True)

        # Total Price
        self.lbl_total = tk.Label(footer_frame, text="₱0.00", font=("Helvetica", 24, "bold"), fg=ACCENT, bg=SURFACE_COLOR)
        self.lbl_total.pack(side="right", padx=(0, 30))

        # Confirm Button
        self.btn_confirm = tk.Button(
            footer_frame, 
            text="Confirm Selection", 
            bg="#444", fg="#888",
            font=("Helvetica", 11, "bold"),
            relief="flat", padx=20, pady=10,
            state="disabled",
            command=self.open_receipt
        )
        self.btn_confirm.pack(side="right", padx=20)

    def create_legend_dot(self, parent, color, text, is_text=False):
        f = tk.Frame(parent, bg=SURFACE_COLOR)
        f.pack(side="left", padx=10)
        
        if is_text:
            tk.Label(f, text="✖", fg=color, bg=SURFACE_COLOR, font=("Arial", 10, "bold")).pack(side="left")
        else:
            # Draw a little colored square
            canvas = tk.Canvas(f, width=16, height=16, bg=color, highlightthickness=0)
            canvas.pack(side="left")
            
        tk.Label(f, text=text, fg="#CCC", bg=SURFACE_COLOR, font=("Helvetica", 9)).pack(side="left", padx=5)

    def toggle_seat(self, row_lbl, seat_num, btn_obj):
        seat_id = (row_lbl, seat_num)
        
        if seat_id in self.selected_seats:
            # Deselect
            self.selected_seats.remove(seat_id)
            btn_obj.configure(bg=SEAT_AVAILABLE, fg=TEXT_MAIN) 
        else:
            # Select
            self.selected_seats.append(seat_id)
            btn_obj.configure(bg=SEAT_SELECTED, fg="#000") # Purple background, black text
            
        self.update_total()

    def update_total(self):
        count = len(self.selected_seats)
        total = count * float(self.showtime['price_standard'])
        
        self.lbl_total.config(text=f"₱{total:,.2f}")
        
        if count > 0:
            self.btn_confirm.config(state="normal", bg=ACCENT, fg="#000", text=f"Confirm {count} Tickets")
        else:
            self.btn_confirm.config(state="disabled", bg="#444", fg="#888", text="Confirm Selection")

    def open_receipt(self):
        customer_name = simpledialog.askstring("Booking", "Enter Customer Name:", parent=self.window)
        if not customer_name: return 

        total_price = len(self.selected_seats) * float(self.showtime['price_standard'])

        booking_id = save_booking(
            self.showtime['id'],
            customer_name,
            self.selected_seats,
            total_price
        )

        if booking_id:
            self.window.destroy()
            time_str = self.showtime['start_time'].strftime("%d %b, %I:%M %p")
            movie_title = self.showtime.get('movie_title', 'Unknown Movie')
            
            receipt = ReceiptWindow(
                booking_id,
                movie_title, 
                time_str,
                self.selected_seats,
                total_price,
                self.showtime['hall_name']
            )
            receipt.run()
        else:
            messagebox.showerror("Error", "Booking failed! Please try again.")

    def run(self):
        self.window.mainloop()
