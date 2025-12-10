import tkinter as tk
from tkinter import messagebox

# OOP IMPORTS
from gui.base_window import BaseWindow
from db.db_manager import DatabaseManager

# THEME
BG_COLOR = "#121212"
SURFACE_COLOR = "#1E1E1E"
TEXT_MAIN = "#FFFFFF"
ACCENT = "#BB86FC"
ACCENT_DARK = "#3700B3"

class AdminLogin(BaseWindow):
    def __init__(self):
        # 1. BaseWindow handles geometry (360x420) and centering
        super().__init__("Admin Login", 360, 420, BG_COLOR)
        
        self.db = DatabaseManager()
        
        # Make Modal
        self.transient() 
        self.grab_set()

        self.setup_ui()

    def setup_ui(self):
        # Container
        main_frame = tk.Frame(self, bg=BG_COLOR, padx=30, pady=30)
        main_frame.pack(expand=True, fill="both")

        # Icon / Header
        tk.Label(main_frame, text="🔒", font=("Segoe UI Emoji", 40), bg=BG_COLOR, fg=ACCENT).pack(pady=(0, 10))
        tk.Label(main_frame, text="Admin Access", font=("Helvetica", 18, "bold"), bg=BG_COLOR, fg=TEXT_MAIN).pack(pady=(0, 20))

        # Helper for Inputs
        def create_input(label_text, is_password=False):
            tk.Label(main_frame, text=label_text, font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#888888", anchor="w").pack(fill="x", pady=(10, 5))
            
            entry = tk.Entry(
                main_frame, font=("Helvetica", 11), bg=SURFACE_COLOR, fg=TEXT_MAIN,
                insertbackground=ACCENT, relief="flat",
                highlightthickness=1, highlightbackground="#333", highlightcolor=ACCENT,
                bd=5
            )
            entry.pack(fill="x")
            if is_password: entry.config(show="•")
            return entry

        self.entry_user = create_input("USERNAME")
        self.entry_pass = create_input("PASSWORD", is_password=True)

        # Login Button
        btn_login = tk.Button(
            main_frame, text="LOGIN", font=("Helvetica", 10, "bold"),
            bg=ACCENT, fg="#000000", activebackground=ACCENT_DARK, activeforeground="#FFFFFF",
            relief="flat", cursor="hand2", pady=10,
            command=self.attempt_login
        )
        btn_login.pack(fill="x", pady=(30, 0))
        
        # Bind "Enter" key
        self.bind('<Return>', lambda event: self.attempt_login())
        self.entry_user.focus_set()

    def attempt_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        # USE DB MANAGER
        user = self.db.check_admin_login(username, password)

        if user:
            self.destroy()
            from gui.admin_dashboard import AdminDashboard
            dashboard = AdminDashboard()
            dashboard.run()
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials", parent=self)

    # Note: BaseWindow has the .run() method, so we don't strictly need to redefine it unless we want specific logic.
    # But keeping it for compatibility with your existing calls is fine.
    def run(self):
        self.mainloop()