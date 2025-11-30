import tkinter as tk
from tkinter import ttk, messagebox
from db.queries import get_all_bookings, delete_booking

class AdminBookings:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Manage Bookings")
        self.window.geometry("800x500")

        tk.Label(self.window, text="Booking History", font=("Arial", 16, "bold")).pack(pady=15)

        # ==========================================
        # TABLE
        # ==========================================
        frame_table = tk.Frame(self.window)
        frame_table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        cols = ("ID", "Date", "Customer", "Movie", "Tix", "Total")
        self.tree = ttk.Treeview(frame_table, columns=cols, show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Customer", text="Customer")
        self.tree.heading("Movie", text="Movie")
        self.tree.heading("Tix", text="Count")
        self.tree.heading("Total", text="Total")

        self.tree.column("ID", width=50)
        self.tree.column("Date", width=120)
        self.tree.column("Customer", width=150)
        self.tree.column("Movie", width=150)
        self.tree.column("Tix", width=50)
        self.tree.column("Total", width=80)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ==========================================
        # ACTIONS
        # ==========================================
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(fill="x", padx=20, pady=20)

        tk.Button(
            btn_frame, 
            text="❌ Cancel / Refund Selected Booking", 
            bg="#f44336", fg="white", font=("Arial", 11),
            command=self.refund_booking
        ).pack(side="right")

        tk.Button(
            btn_frame, 
            text="🔄 Refresh List", 
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
            date_str = b['booking_date'].strftime("%Y-%m-%d %H:%M")
            self.tree.insert("", "end", values=(
                b['id'], 
                date_str, 
                b['customer_name'], 
                b['title'], 
                b['ticket_count'], 
                f"${b['total_amount']:.2f}"
            ))

    def refund_booking(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to refund.")
            return

        item = self.tree.item(selected)
        booking_id = item['values'][0]
        customer = item['values'][2]

        if messagebox.askyesno("Confirm Refund", f"Are you sure you want to cancel the booking for {customer}?\nThis will free up the seats."):
            if delete_booking(booking_id):
                messagebox.showinfo("Success", "Booking cancelled and refunded.")
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to cancel booking.")

    def run(self):
        self.window.mainloop()
