import tkinter as tk
from tkinter import messagebox, simpledialog

# OOP IMPORTS
from gui.base_window import BaseWindow
from db.db_manager import DatabaseManager
from gui.receipt_window import ReceiptWindow

# THEME CONSTANTS
BG_COLOR = "#121212"
SURFACE_COLOR = "#1E1E1E"
TEXT_MAIN = "#FFFFFF"
ACCENT = "#BB86FC"
SEAT_AVAILABLE = "#333333"
SEAT_SELECTED = ACCENT
SEAT_TAKEN = "#CF6679"

class SeatMap(BaseWindow):
    def __init__(self, showtime_obj, movie_title="Movie"):
        # 1. Store Data
        self.showtime = showtime_obj
        self.movie_title = movie_title
        self.db = DatabaseManager()
        
        # 2. Calculate Window Size based on Hall dimensions
        # Logic moved from BaseWindow, but params passed here
        cols = self.showtime.total_cols
        rows = self.showtime.total_rows
        w = max(900, cols * 55 + 200)
        h = max(700, rows * 55 + 250)

        # 3. Initialize BaseWindow
        super().__init__(f"Select Seats - {self.showtime.hall_name}", w, h, BG_COLOR)

        # 4. State
        self.selected_seats = [] 
        self.taken_seats = self.db.get_taken_seats(self.showtime.id)

        # 5. Build UI
        self.setup_header()
        self.setup_screen_visual(w)
        self.setup_grid()
        self.setup_footer()

    def setup_header(self):
        header_frame = tk.Frame(self, bg=BG_COLOR, pady=20)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text=self.movie_title, font=("Helvetica", 20, "bold"), fg=TEXT_MAIN, bg=BG_COLOR).pack()
        
        time_str = self.showtime.get_formatted_time()
        sub_text = f"{self.showtime.hall_name}  •  {time_str}  •  ₱{self.showtime.price}"
        tk.Label(header_frame, text=sub_text, font=("Helvetica", 12), fg="#888", bg=BG_COLOR).pack(pady=(5,0))

    def setup_screen_visual(self, window_width):
        screen_frame = tk.Frame(self, bg=BG_COLOR)
        screen_frame.pack(fill="x", pady=(10, 30))
        
        canvas_screen = tk.Canvas(screen_frame, height=40, bg=BG_COLOR, highlightthickness=0)
        canvas_screen.pack(expand=True, fill="x", padx=100)
        
        # Draw trapezoid
        w = window_width - 200
        canvas_screen.create_polygon(
            0, 0, w, 0, 
            w-40, 30, 40, 30, 
            fill="#333", outline=""
        )
        canvas_screen.create_text(w/2, 15, text="SCREEN", fill="#000", font=("Helvetica", 10, "bold"))

    def setup_grid(self):
        self.grid_frame = tk.Frame(self, bg=BG_COLOR)
        self.grid_frame.pack()

        rows = self.showtime.total_rows
        cols = self.showtime.total_cols

        for r in range(rows):
            row_label = chr(65 + r)
            
            # Row Label Left
            tk.Label(self.grid_frame, text=row_label, fg="#555", bg=BG_COLOR, font=("Arial", 10, "bold")).grid(row=r, column=0, padx=10)
            
            for c in range(cols):
                seat_num = c + 1
                is_taken = (row_label, seat_num) in self.taken_seats
                
                bg = SEAT_TAKEN if is_taken else SEAT_AVAILABLE
                state = "disabled" if is_taken else "normal"
                cursor = "arrow" if is_taken else "hand2"
                text = "✖" if is_taken else str(seat_num)

                btn = tk.Button(
                    self.grid_frame, text=text, width=4, height=2,
                    bg=bg, fg=TEXT_MAIN, relief="flat", bd=0,
                    activebackground=ACCENT, activeforeground="#000",
                    state=state, cursor=cursor, font=("Arial", 9)
                )
                
                # Lambda Trap Fix
                btn.configure(command=lambda r=row_label, n=seat_num, b=btn: self.toggle_seat(r, n, b))
                btn.grid(row=r, column=c+1, padx=3, pady=3)
            
            # Row Label Right
            tk.Label(self.grid_frame, text=row_label, fg="#555", bg=BG_COLOR, font=("Arial", 10, "bold")).grid(row=r, column=cols+2, padx=10)

    def setup_footer(self):
        footer_frame = tk.Frame(self, bg=SURFACE_COLOR, height=80)
        footer_frame.pack(side="bottom", fill="x")
        footer_frame.pack_propagate(False)

        # Legend
        legend_frame = tk.Frame(footer_frame, bg=SURFACE_COLOR)
        legend_frame.pack(side="left", padx=40)
        self.create_legend_dot(legend_frame, SEAT_AVAILABLE, "Available")
        self.create_legend_dot(legend_frame, SEAT_SELECTED, "Selected")
        self.create_legend_dot(legend_frame, SEAT_TAKEN, "Sold", is_text=True)

        # Total
        self.lbl_total = tk.Label(footer_frame, text="₱0.00", font=("Helvetica", 24, "bold"), fg=ACCENT, bg=SURFACE_COLOR)
        self.lbl_total.pack(side="right", padx=(0, 30))

        # Confirm Button
        self.btn_confirm = tk.Button(
            footer_frame, text="Confirm Selection", 
            bg="#444", fg="#888", font=("Helvetica", 11, "bold"),
            relief="flat", padx=20, pady=10, state="disabled",
            command=self.process_booking
        )
        self.btn_confirm.pack(side="right", padx=20)

    def create_legend_dot(self, parent, color, text, is_text=False):
        f = tk.Frame(parent, bg=SURFACE_COLOR)
        f.pack(side="left", padx=10)
        if is_text:
            tk.Label(f, text="✖", fg=color, bg=SURFACE_COLOR, font=("Arial", 10, "bold")).pack(side="left")
        else:
            canvas = tk.Canvas(f, width=16, height=16, bg=color, highlightthickness=0)
            canvas.pack(side="left")
        tk.Label(f, text=text, fg="#CCC", bg=SURFACE_COLOR, font=("Helvetica", 9)).pack(side="left", padx=5)

    def toggle_seat(self, row_lbl, seat_num, btn_obj):
        seat_id = (row_lbl, seat_num)
        
        if seat_id in self.selected_seats:
            self.selected_seats.remove(seat_id)
            btn_obj.configure(bg=SEAT_AVAILABLE, fg=TEXT_MAIN) 
        else:
            self.selected_seats.append(seat_id)
            btn_obj.configure(bg=SEAT_SELECTED, fg="#000") 
            
        self.update_total()

    def update_total(self):
        count = len(self.selected_seats)
        total = count * float(self.showtime.price)
        self.lbl_total.config(text=f"₱{total:,.2f}")
        
        if count > 0:
            self.btn_confirm.config(state="normal", bg=ACCENT, fg="#000", text=f"Confirm {count} Tickets")
        else:
            self.btn_confirm.config(state="disabled", bg="#444", fg="#888", text="Confirm Selection")

    def process_booking(self):
        customer_name = simpledialog.askstring("Booking", "Enter Customer Name:", parent=self)
        if not customer_name: return 

        total_price = len(self.selected_seats) * float(self.showtime.price)

        # CALL DB MANAGER
        booking_id = self.db.create_booking(
            self.showtime.id,
            customer_name,
            self.selected_seats,
            total_price
        )

        if booking_id:
            self.destroy()
            # Receipt Window still expects raw data args, we can leave it or refactor it later.
            # For now, passing arguments normally is fine.
            receipt = ReceiptWindow(
                booking_id,
                self.movie_title, 
                self.showtime.get_formatted_time(),
                self.selected_seats,
                total_price,
                self.showtime.hall_name
            )
            receipt.run()
        else:
            messagebox.showerror("Error", "Booking failed!", parent=self)