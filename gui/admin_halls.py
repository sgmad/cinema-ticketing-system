import tkinter as tk
from tkinter import ttk, messagebox

# OOP IMPORTS
from gui.base_window import BaseWindow
from db.db_manager import DatabaseManager

class AdminHalls(BaseWindow):
    def __init__(self):
        # 1. BaseWindow Setup
        super().__init__("Manage Cinemas / Halls", 800, 550)
        
        self.db = DatabaseManager()
        self.current_edit_id = None 

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Main Layout Container
        main_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # ==========================================
        # LEFT COLUMN: INPUT FORM
        # ==========================================
        frame_left = tk.Frame(main_frame, bg="#f0f0f0", width=300)
        frame_left.pack(side="left", fill="y", padx=(0, 20))

        # Form Title
        self.lbl_form_title = tk.Label(frame_left, text="Add New Hall", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.lbl_form_title.pack(anchor="w", pady=(0, 15))

        # Helper for Form Inputs
        def add_input(label):
            tk.Label(frame_left, text=label, bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 0))
            entry = tk.Entry(frame_left, font=("Arial", 11), width=25)
            entry.pack(pady=(0, 5))
            return entry

        self.entry_name = add_input("Hall Name:")
        self.entry_rows = add_input("Rows:")
        self.entry_cols = add_input("Columns:")

        # Action Buttons
        self.btn_save = tk.Button(
            frame_left, 
            text="Create Hall", 
            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
            pady=8, relief="flat", cursor="hand2",
            command=self.save_hall
        )
        self.btn_save.pack(fill="x", pady=(20, 5))
        
        self.btn_clear = tk.Button(
            frame_left, 
            text="Clear / Cancel", 
            bg="#999", fg="white", font=("Arial", 10, "bold"),
            pady=5, relief="flat", cursor="hand2",
            command=self.clear_form
        )
        self.btn_clear.pack(fill="x")

        tk.Button(
            frame_left, 
            text="Delete Selected", 
            bg="#f44336", fg="white", font=("Arial", 10, "bold"),
            pady=8, relief="flat", cursor="hand2",
            command=self.remove_hall
        ).pack(fill="x", pady=(10,0))

        # Reference Guide for Layouts
        guide_frame = tk.LabelFrame(frame_left, text="Recommended Layouts", padx=10, pady=10, bg="#f0f0f0", fg="#666")
        guide_frame.pack(fill="x", pady=(20, 0))

        def add_guide_row(label, size):
            f = tk.Frame(guide_frame, bg="#f0f0f0")
            f.pack(fill="x", pady=2)
            tk.Label(f, text=label, font=("Arial", 9, "bold"), fg="#444", bg="#f0f0f0").pack(side="left")
            tk.Label(f, text=size, font=("Arial", 9), fg="#666", bg="#f0f0f0").pack(side="right")

        add_guide_row("Standard:", "8 rows x 12 cols")
        add_guide_row("IMAX:", "12 rows x 18 cols")
        add_guide_row("VIP / Luxe:", "5 rows x 8 cols")

        # ==========================================
        # RIGHT COLUMN: HALL LIST
        # ==========================================
        # Background is gray to blend with window, preventing white bar artifacts
        frame_right = tk.Frame(main_frame, bg="#f0f0f0") 
        frame_right.pack(side="right", fill="both", expand=True)
        
        # Instructions Label
        tk.Label(
            frame_right, 
            text="Click row to Edit", 
            font=("Arial", 10, "italic"), 
            fg="#666", 
            bg="#f0f0f0"
        ).pack(anchor="w", pady=(0, 5))

        # Data Table
        cols = ("ID", "Name", "Size", "Type", "Price")
        self.tree = ttk.Treeview(frame_right, columns=cols, show="headings")
        
        self.tree.heading("ID", text="ID"); self.tree.column("ID", width=40, anchor="center")
        self.tree.heading("Name", text="Hall Name"); self.tree.column("Name", width=150)
        self.tree.heading("Size", text="Grid Size"); self.tree.column("Size", width=100, anchor="center")
        self.tree.heading("Type", text="Class"); self.tree.column("Type", width=100, anchor="center")
        self.tree.heading("Price", text="Base Price"); self.tree.column("Price", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(frame_right, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Scrollbar on right, tree fills remaining space
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel: return

        item = self.tree.item(sel)
        vals = item['values'] 
        
        self.current_edit_id = vals[0]
        
        # Parse dimensions string (e.g. "10 x 14") to populate inputs
        dims = vals[2].split(" x ")
        rows = dims[0]
        cols = dims[1]

        self.entry_name.delete(0, 'end'); self.entry_name.insert(0, vals[1])
        self.entry_rows.delete(0, 'end'); self.entry_rows.insert(0, rows)
        self.entry_cols.delete(0, 'end'); self.entry_cols.insert(0, cols)

        # Update Form State to "Edit Mode"
        self.lbl_form_title.config(text=f"Edit Hall #{self.current_edit_id}", fg="#2196F3")
        self.btn_save.config(text="Update Hall", bg="#2196F3")

    def save_hall(self):
        name = self.entry_name.get()
        rows = self.entry_rows.get()
        cols = self.entry_cols.get()

        if not name or not rows or not cols:
            messagebox.showerror("Error", "All fields required", parent=self)
            return

        try:
            r = int(rows)
            c = int(cols)
        except ValueError:
            messagebox.showerror("Error", "Rows and Columns must be numbers.", parent=self)
            return

        if r > 20 or c > 30:
             if not messagebox.askyesno("Warning", "That is a very large grid. It might not fit on the screen.\nContinue?", parent=self):
                 return

        if self.current_edit_id:
            # Update Existing Hall
            if self.db.update_hall(self.current_edit_id, name, r, c):
                messagebox.showinfo("Success", "Hall Updated", parent=self)
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Update Failed", parent=self)
        else:
            # Create New Hall
            if self.db.add_hall(name, r, c):
                messagebox.showinfo("Success", "Hall Created", parent=self)
                self.clear_form()
                self.load_data()

    def clear_form(self):
        self.current_edit_id = None
        self.entry_name.delete(0, 'end')
        self.entry_rows.delete(0, 'end')
        self.entry_cols.delete(0, 'end')
        
        self.lbl_form_title.config(text="Add New Hall", fg="black")
        self.btn_save.config(text="Create Hall", bg="#4CAF50")
        
        if self.tree.selection(): self.tree.selection_remove(self.tree.selection())

    def remove_hall(self):
        sel = self.tree.selection()
        if sel:
            if not messagebox.askyesno("Confirm", "Are you sure you want to delete this hall?", parent=self):
                return

            hall_id = self.tree.item(sel)['values'][0]
            
            if self.db.delete_hall(hall_id):
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Could not delete. It might be in use by a showtime.", parent=self)
        else:
            messagebox.showwarning("Warning", "Please select a hall to delete.", parent=self)

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        
        # Use DB Manager to fetch Hall Objects
        halls = self.db.fetch_all_halls()
        
        for h in halls:
            # Polymorphism: Use object method to get price, Class name for type
            hall_type = h.__class__.__name__.replace("Hall", "") 
            
            self.tree.insert("", "end", values=(
                h.id, 
                h.name, 
                f"{h.rows} x {h.cols}",
                hall_type,
                f"₱{h.get_base_price()}"
            ))

if __name__ == "__main__":
    AdminHalls().run()