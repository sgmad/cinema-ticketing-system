import tkinter as tk
from tkinter import ttk, messagebox
from db.queries import get_all_halls, add_hall, delete_hall, update_hall

class AdminHalls:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Manage Cinemas / Halls")
        
        # 1. CENTERED GEOMETRY
        w, h = 800, 550
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = int(sw/2 - w/2)
        y = int(sh/2 - h/2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")
        self.window.configure(bg="#f0f0f0")
        
        self.current_edit_id = None # Track edit state

        # ==========================================
        # HEADER
        # ==========================================
        # header_frame = tk.Frame(self.window, bg="#607D8B", pady=20)
        # header_frame.pack(fill="x")
        # self.lbl_header = tk.Label(
        #     header_frame, 
        #     text="Cinema Hall Configuration", 
        #     font=("Arial", 18, "bold"), fg="white", bg="#607D8B"
        # )
        # self.lbl_header.pack()

        # Main Layout Container
        main_frame = tk.Frame(self.window, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # ==========================================
        # LEFT SIDE: FORM
        # ==========================================
        frame_left = tk.Frame(main_frame, bg="#f0f0f0", width=300)
        frame_left.pack(side="left", fill="y", padx=(0, 20))

        self.lbl_form_title = tk.Label(frame_left, text="Add New Hall", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.lbl_form_title.pack(anchor="w", pady=(0, 15))

        # Helper for Inputs
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

        # Layout Guide
        guide_frame = tk.LabelFrame(frame_left, text="Recommended Layouts", padx=10, pady=10, bg="#f0f0f0", fg="#666")
        guide_frame.pack(fill="x", pady=(20, 0))

        def add_guide_row(label, size):
            f = tk.Frame(guide_frame, bg="#f0f0f0")
            f.pack(fill="x", pady=2)
            tk.Label(f, text=label, font=("Arial", 9, "bold"), fg="#444", bg="#f0f0f0").pack(side="left")
            tk.Label(f, text=size, font=("Arial", 9), fg="#666", bg="#f0f0f0").pack(side="right")

        add_guide_row("Standard:", "10 rows x 14 cols")
        add_guide_row("IMAX:", "14 rows x 20 cols")
        add_guide_row("VIP / Luxe:", "5 rows x 8 cols")

        # ==========================================
        # RIGHT SIDE: LIST
        # ==========================================
        frame_right = tk.Frame(main_frame, bg="white")
        frame_right.pack(side="right", fill="both", expand=True)
        
        tk.Label(frame_right, text="Click row to Edit", font=("Arial", 10, "italic"), fg="#666", bg="white").pack(anchor="ne")

        cols = ("ID", "Name", "Size")
        self.tree = ttk.Treeview(frame_right, columns=cols, show="headings")
        
        self.tree.heading("ID", text="ID"); self.tree.column("ID", width=40, anchor="center")
        self.tree.heading("Name", text="Hall Name"); self.tree.column("Name", width=150)
        self.tree.heading("Size", text="Grid Size"); self.tree.column("Size", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(frame_right, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.load_data()

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel: return

        item = self.tree.item(sel)
        vals = item['values'] # [id, Name, "10 x 14"]
        
        self.current_edit_id = vals[0]
        
        # Parse dimensions string "10 x 14"
        dims = vals[2].split(" x ")
        rows = dims[0]
        cols = dims[1]

        # Populate
        self.entry_name.delete(0, 'end'); self.entry_name.insert(0, vals[1])
        self.entry_rows.delete(0, 'end'); self.entry_rows.insert(0, rows)
        self.entry_cols.delete(0, 'end'); self.entry_cols.insert(0, cols)

        # UI Update
        self.lbl_form_title.config(text=f"Edit Hall #{self.current_edit_id}", fg="#2196F3")
        self.btn_save.config(text="Update Hall", bg="#2196F3")

    def save_hall(self):
        name = self.entry_name.get()
        rows = self.entry_rows.get()
        cols = self.entry_cols.get()

        if not name or not rows or not cols:
            messagebox.showerror("Error", "All fields required", parent=self.window)
            return

        try:
            r = int(rows)
            c = int(cols)
        except ValueError:
            messagebox.showerror("Error", "Rows and Columns must be numbers.", parent=self.window)
            return

        if r > 20 or c > 30:
             if not messagebox.askyesno("Warning", "That is a very large grid. It might not fit on the screen.\nContinue?", parent=self.window):
                 return

        if self.current_edit_id:
            # UPDATE
            if update_hall(self.current_edit_id, name, r, c):
                messagebox.showinfo("Success", "Hall Updated", parent=self.window)
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Update Failed", parent=self.window)
        else:
            # CREATE
            if add_hall(name, r, c):
                messagebox.showinfo("Success", "Hall Created", parent=self.window)
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
            if not messagebox.askyesno("Confirm", "Are you sure you want to delete this hall?", parent=self.window):
                return

            hall_id = self.tree.item(sel)['values'][0]
            
            if delete_hall(hall_id):
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Could not delete. It might be in use by a showtime.", parent=self.window)
        else:
            messagebox.showwarning("Warning", "Please select a hall to delete.", parent=self.window)

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for h in get_all_halls():
            self.tree.insert("", "end", values=(h['id'], h['name'], f"{h['total_rows']} x {h['total_cols']}"))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    AdminHalls().run()