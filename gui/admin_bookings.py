import tkinter as tk
from tkinter import ttk, messagebox
from db.queries import get_all_bookings, delete_booking

# THEME
BG_COLOR = "#f0f0f0" 
HEADER_TXT = "white"

class AdminBookings:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Manage Bookings")
        
        # 1. CENTERED GEOMETRY
        w, h = 950, 600
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = int(sw/2 - w/2)
        y = int(sh/2 - h/2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")
        self.window.configure(bg=BG_COLOR)

        # ==========================================
        # HEADER
        # ==========================================
        # header_frame = tk.Frame(self.window,pady=20)
        # header_frame.pack(fill="x")
        
        # tk.Label(
        #     header_frame, 
        #     text="Booking History & Refunds", 
        #     font=("Helvetica", 18, "bold"), fg=HEADER_TXT
        # ).pack()

        # ==========================================
        # TABLE AREA
        # ==========================================
        frame_table = tk.Frame(self.window, bg=BG_COLOR, padx=20, pady=20)
        frame_table.pack(fill="both", expand=True)

        cols = ("ID", "Date", "Customer", "Movie", "Tix", "Total")
        self.tree = ttk.Treeview(frame_table, columns=cols, show="headings")

        # Column Configuration
        self.tree.heading("ID", text="ID"); self.tree.column("ID", width=50, anchor="center")
        self.tree.heading("Date", text="Date & Time"); self.tree.column("Date", width=140)
        self.tree.heading("Customer", text="Customer Name"); self.tree.column("Customer", width=180)
        self.tree.heading("Movie", text="Movie"); self.tree.column("Movie", width=250)
        self.tree.heading("Tix", text="Count"); self.tree.column("Tix", width=60, anchor="center")
        self.tree.heading("Total", text="Total Paid"); self.tree.column("Total", width=100, anchor="e")

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ==========================================
        # ACTION BAR
        # ==========================================
        btn_frame = tk.Frame(self.window, bg="#e0e0e0", pady=15, padx=20)
        btn_frame.pack(side="bottom", fill="x")

        # Refund Button (Right)
        tk.Button(
            btn_frame, 
            text="❌ Cancel / Refund", 
            bg="#f44336", fg="white", font=("Arial", 11, "bold"),
            padx=20, pady=5, relief="flat", cursor="hand2",
            command=self.refund_booking
        ).pack(side="right")

        # Refresh Button (Left)
        tk.Button(
            btn_frame, 
            text="🔄 Refresh List", 
            bg="white", fg="black", font=("Arial", 10),
            padx=15, pady=5, relief="flat",
            command=self.load_data
        ).pack(side="left")

        self.load_data()

    def load_data(self):
        # Clear
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch
        bookings = get_all_bookings()
        
        for b in bookings:
            date_str = b['booking_date'].strftime("%Y-%m-%d  %H:%M")
            self.tree.insert("", "end", values=(
                b['id'], 
                date_str, 
                b['customer_name'], 
                b['title'], 
                b['ticket_count'], 
                f"₱{b['total_amount']:,.2f}"
            ))

    def refund_booking(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a booking from the list to refund.", parent=self.window)
            return

        item = self.tree.item(selected)
        booking_id = item['values'][0]
        customer = item['values'][2]
        amount = item['values'][5]

        msg = f"Are you sure you want to cancel the booking for:\n\nCustomer: {customer}\nAmount: {amount}\n\nThis action cannot be undone and will free up the seats."
        
        if messagebox.askyesno("Confirm Refund", msg, icon='warning', parent=self.window):
            if delete_booking(booking_id):
                messagebox.showinfo("Success", "Booking cancelled successfully.\nSeats are now available.", parent=self.window)
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to cancel booking. Please check database connection.", parent=self.window)

    def run(self):
        self.window.mainloop()
