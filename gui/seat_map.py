import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from gui.receipt_window import ReceiptWindow
from db.queries import get_taken_seats
from db.queries import save_booking

class SeatMap:
    def __init__(self, showtime_data):
        """
        showtime_data is the dictionary passed from the previous screen.
        It must contain: 'id', 'hall_name', 'price_standard', 'start_time',
        'total_rows', 'total_cols'
        """
        self.showtime = showtime_data
        self.window = tk.Toplevel()
        
        # DYNAMIC SIZING LOGIC
        # Base size + (Pixels per button * count)
        cols = self.showtime['total_cols']
        rows = self.showtime['total_rows']
        
        # Rough math: 50px width per seat, 50px height per seat
        width = max(800, cols * 60 + 100)  # Minimum 800px
        height = max(700, rows * 60 + 200) # Minimum 700px
        
        self.window.geometry(f"{width}x{height}")
        self.window.title(f"Select Seats - {self.showtime['hall_name']}")
        
        # Data Containers
        self.selected_seats = [] # List of tuples like ('A', 1)
        self.taken_seats = get_taken_seats(self.showtime['id']) # Fetch sold tickets
        
        # ==========================================
        # HEADER
        # ==========================================
        header_frame = tk.Frame(self.window, pady=10)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame, 
            text=f"Screen: {self.showtime['hall_name']}", 
            font=("Arial", 16, "bold")
        ).pack()
        
        time_str = self.showtime['start_time'].strftime("%d %b, %I:%M %p")
        tk.Label(
            header_frame, 
            text=f"{time_str}  •  ₱{self.showtime['price_standard']}/ticket", 
            font=("Arial", 12)
        ).pack()

        # ==========================================
        # SCREEN VISUAL (The "Screen" bar)
        # ==========================================
        tk.Label(self.window, text="SCREEN", bg="#333", fg="white", width=60).pack(pady=(10, 20))

        # ==========================================
        # SEAT GRID
        # ==========================================
        # We use a Frame to hold the grid of buttons
        self.grid_frame = tk.Frame(self.window)
        self.grid_frame.pack()

        rows = self.showtime['total_rows'] # e.g., 8
        cols = self.showtime['total_cols'] # e.g., 10

        for r in range(rows):
            # Convert 0 -> 'A', 1 -> 'B'
            row_label = chr(65 + r)
            
            for c in range(cols):
                seat_num = c + 1
                
                # Check if this seat is already taken
                is_taken = (row_label, seat_num) in self.taken_seats
                
                # Visual Styles
                bg_color = "#e53935" if is_taken else "#81c784" # Red if taken, Green if free
                state = "disabled" if is_taken else "normal"
                
                btn = tk.Button(
                    self.grid_frame,
                    text=f"{row_label}{seat_num}",
                    width=4,
                    height=2,
                    bg=bg_color,
                    state=state,
                    # We use a helper function to bind the click
                    command=lambda r=row_label, n=seat_num, b_ref=None: self.toggle_seat(r, n, b_ref)
                )
                
                # We need to update the command to pass the button object itself so we can change its color
                # This is a common Tkinter trick
                btn.configure(command=lambda r=row_label, n=seat_num, b=btn: self.toggle_seat(r, n, b))
                
                btn.grid(row=r, column=c, padx=5, pady=5)

        # ==========================================
        # FOOTER (Legend & Confirm)
        # ==========================================
        footer_frame = tk.Frame(self.window, pady=20)
        footer_frame.pack(side="bottom", fill="x")

        # Legend
        legend_frame = tk.Frame(footer_frame)
        legend_frame.pack(pady=10)
        
        self.create_legend_item(legend_frame, "#81c784", "Available").pack(side="left", padx=10)
        self.create_legend_item(legend_frame, "#2196F3", "Selected").pack(side="left", padx=10)
        self.create_legend_item(legend_frame, "#e53935", "Sold").pack(side="left", padx=10)

        # Confirm Button
        self.btn_confirm = tk.Button(
            footer_frame, 
            text="Confirm Booking", 
            bg="#2196F3", 
            fg="white", 
            font=("Arial", 12, "bold"),
            state="disabled",
            command=self.open_receipt
        )
        self.btn_confirm.pack(pady=10)

        self.lbl_total = tk.Label(footer_frame, text="Total: ₱0.00", font=("Arial", 14, "bold"))
        self.lbl_total.pack()

    def create_legend_item(self, parent, color, text):
        f = tk.Frame(parent)
        tk.Label(f, bg=color, width=4, height=1).pack(side="left")
        tk.Label(f, text=text).pack(side="left", padx=5)
        return f

    def toggle_seat(self, row_lbl, seat_num, btn_obj):
        seat_id = (row_lbl, seat_num)
        
        if seat_id in self.selected_seats:
            # Deselect
            self.selected_seats.remove(seat_id)
            btn_obj.configure(bg="#81c784") # Back to Green
        else:
            # Select
            self.selected_seats.append(seat_id)
            btn_obj.configure(bg="#2196F3") # Blue
            
        self.update_total()

    def update_total(self):
        count = len(self.selected_seats)
        total = count * float(self.showtime['price_standard'])
        
        self.lbl_total.config(text=f"Total: ₱{total:.2f}")
        
        if count > 0:
            self.btn_confirm.config(state="normal", text=f"Confirm {count} Tickets")
        else:
            self.btn_confirm.config(state="disabled", text="Confirm Booking")

    def open_receipt(self):
        # 1. Get Customer Name
        customer_name = simpledialog.askstring("Customer Name", "Please enter your name for the booking:")
        
        if not customer_name:
            return # User clicked cancel

        # 2. Calculate final price
        total_price = len(self.selected_seats) * float(self.showtime['price_standard'])

        # 3. Save to Database
        booking_id = save_booking(
            self.showtime['id'],
            customer_name,
            self.selected_seats,
            total_price
        )

        if booking_id:
            # 4. Success! Close this map and show receipt
            self.window.destroy()
            
            # Format time for display
            time_str = self.showtime['start_time'].strftime("%d %b, %I:%M %p")
            
            receipt = ReceiptWindow(
                booking_id,
                # We don't have movie title in showtime_dict usually, 
                # but we can pass it or just show Hall info. 
                # Ideally, pass movie title into SeatMap init too.
                "Movie Ticket", 
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
