import tkinter as tk
from tkinter import messagebox
from db.queries import check_admin_login
# We import AdminDashboard inside the login function to avoid circular import issues
# if AdminDashboard ever tries to import AdminLogin.

class AdminLogin:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Admin Login")
        self.window.geometry("300x250")
        
        # Make the window modal (keeps it on top)
        self.window.transient() 
        self.window.grab_set()

        # Title
        tk.Label(self.window, text="Administrator Access", font=("Arial", 12, "bold")).pack(pady=15)

        # Username Input
        tk.Label(self.window, text="Username").pack(pady=(5, 0))
        self.entry_user = tk.Entry(self.window)
        self.entry_user.pack()

        # Password Input
        tk.Label(self.window, text="Password").pack(pady=(10, 0))
        self.entry_pass = tk.Entry(self.window, show="*") # show="*" hides the text
        self.entry_pass.pack()

        # Login Button
        tk.Button(
            self.window, 
            text="Login", 
            width=15, 
            bg="#2196F3", 
            fg="white", 
            command=self.attempt_login
        ).pack(pady=20)
        
        # Bind "Enter" key to trigger login too
        self.window.bind('<Return>', lambda event: self.attempt_login())

    def attempt_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        # 1. Check database for this user
        user = check_admin_login(username, password)

        if user:
            # 2. SUCCESS: Close login, open dashboard
            print(f"Login successful for {username}")
            self.window.destroy()
            
            # Late import to prevent circular dependency
            from gui.admin_dashboard import AdminDashboard
            dashboard = AdminDashboard()
            dashboard.run()
        else:
            # 3. FAIL: Show error
            messagebox.showerror("Login Failed", "Invalid username or password")

    def run(self):
        self.window.mainloop()
