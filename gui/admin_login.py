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

        # --- Username Field ---
        tk.Label(main_frame, text="USERNAME", font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#888888", anchor="w").pack(fill="x", pady=(10, 5))
        
        self.entry_user = tk.Entry(
            main_frame, font=("Helvetica", 11), bg=SURFACE_COLOR, fg=TEXT_MAIN,
            insertbackground=ACCENT, relief="flat",
            highlightthickness=1, highlightbackground="#333", highlightcolor=ACCENT,
            bd=5
        )
        self.entry_user.pack(fill="x")

        # --- Password Field with Toggle ---
        tk.Label(main_frame, text="PASSWORD", font=("Helvetica", 9, "bold"), bg=BG_COLOR, fg="#888888", anchor="w").pack(fill="x", pady=(15, 5))

        # Container for Entry + Toggle Button
        pass_frame = tk.Frame(main_frame, bg=SURFACE_COLOR, highlightthickness=1, highlightbackground="#333", highlightcolor=ACCENT)
        pass_frame.pack(fill="x")

        self.entry_pass = tk.Entry(
            pass_frame, font=("Helvetica", 11), bg=SURFACE_COLOR, fg=TEXT_MAIN,
            insertbackground=ACCENT, relief="flat", bd=5, show="•"
        )
        self.entry_pass.pack(side="left", fill="x", expand=True)

        self.btn_show_pass = tk.Button(
            pass_frame, text="👁", font=("Segoe UI Emoji", 10),
            bg=SURFACE_COLOR, fg="#888", activebackground=SURFACE_COLOR, activeforeground=ACCENT,
            relief="flat", bd=0, cursor="hand2",
            command=self.toggle_password
        )
        self.btn_show_pass.pack(side="right", padx=5)

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

    def toggle_password(self):
        if self.entry_pass.cget('show') == '':
            self.entry_pass.config(show='•')
            self.btn_show_pass.config(fg="#888") # Dim icon when hidden
        else:
            self.entry_pass.config(show='')
            self.btn_show_pass.config(fg=ACCENT) # Light up icon when visible

    def attempt_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        user = self.db.check_admin_login(username, password)

        if user:
            self.destroy()
            from gui.admin_dashboard import AdminDashboard
            dashboard = AdminDashboard()
            dashboard.run()
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials", parent=self)

    def run(self):
        self.mainloop()
