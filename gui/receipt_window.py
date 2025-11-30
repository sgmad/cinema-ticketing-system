import tkinter as tk
from tkinter import messagebox

class ReceiptWindow:
    def __init__(self, booking_id, movie_title, showtime_str, seats, total, hall_name):
        self.window = tk.Toplevel()
        self.window.title("Booking Confirmation")
        self.window.geometry("400x550") # Increased height slightly
        self.window.configure(bg="white")

        # Save data for the print function
        self.booking_id = booking_id
        self.movie_title = movie_title
        self.showtime_str = showtime_str
        self.seats = seats
        self.total = total
        self.hall_name = hall_name

        # Success Icon/Text
        tk.Label(
            self.window, 
            text="✔ Booking Confirmed!", 
            fg="green", bg="white", 
            font=("Arial", 18, "bold")
        ).pack(pady=(30, 10))

        tk.Label(
            self.window, 
            text=f"Booking ID: #{booking_id}", 
            fg="#555", bg="white", 
            font=("Arial", 12)
        ).pack(pady=(0, 20))

        # Divider
        tk.Frame(self.window, height=2, bg="#eee").pack(fill="x", padx=20)

        # Details
        detail_frame = tk.Frame(self.window, bg="white", pady=20)
        detail_frame.pack()

        # Helper to make rows
        def add_row(label, value):
            f = tk.Frame(detail_frame, bg="white")
            f.pack(fill="x", pady=5)
            tk.Label(f, text=label, font=("Arial", 10, "bold"), bg="white", width=12, anchor="w").pack(side="left")
            tk.Label(f, text=value, font=("Arial", 10), bg="white", anchor="w").pack(side="left")

        add_row("Movie:", movie_title)
        add_row("Cinema:", hall_name)
        add_row("Time:", showtime_str)
        
        # Format seats list: [('A', 1)] -> "A1"
        self.seat_str = ", ".join([f"{r}{n}" for r, n in seats])
        add_row("Seats:", self.seat_str)
        
        add_row("Total Paid:", f"${total:.2f}")

        # Divider
        tk.Frame(self.window, height=2, bg="#eee").pack(fill="x", padx=20, pady=20)

        # ==========================================
        # NEW: Print Button
        # ==========================================
        tk.Button(
            self.window, 
            text="🖨 Print Receipt", 
            bg="#FF9800", fg="white", 
            font=("Arial", 11),
            width=20,
            command=self.print_receipt
        ).pack(side="bottom", pady=(0, 30))

        # Close Button
        tk.Button(
            self.window, 
            text="Return to Home", 
            bg="#2196F3", fg="white", 
            font=("Arial", 11),
            width=20,
            command=self.close_all
        ).pack(side="bottom", pady=(0, 10))

    def print_receipt(self):
        """ "Printing" by outputting text to the console """
        print("\n" + "="*40)
        print("       SCREENPASS CINEMAS RECEIPT       ")
        print("="*40)
        print(f"Booking ID : #{self.booking_id}")
        print(f"Date       : {self.showtime_str}")
        print("-" * 40)
        print(f"Movie      : {self.movie_title}")
        print(f"Hall       : {self.hall_name}")
        print(f"Seats      : {self.seat_str}")
        print("-" * 40)
        print(f"TOTAL PAID : ${self.total:.2f}")
        print("="*40 + "\n")
        
        messagebox.showinfo("Printer", "Receipt sent to console printer!")

    def close_all(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()