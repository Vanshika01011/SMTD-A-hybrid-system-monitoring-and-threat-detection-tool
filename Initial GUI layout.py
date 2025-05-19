
##                                          Initial GUI layout




import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Pillow required: pip install pillow
import threading
import time
import os

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Loading SMTD...")
        self.geometry("500x300")
        self.overrideredirect(True)  # No title bar

        self.configure(bg="#1e1e1e")

        # Load splash image
        try:
            splash_img = Image.open("splash.png").resize((500, 300))
            self.photo = ImageTk.PhotoImage(splash_img)
            label = tk.Label(self, image=self.photo, bg="#1e1e1e")
            label.pack()
        except FileNotFoundError:
            tk.Label(self, text="SMTD Loading...", font=("Arial", 20), bg="#1e1e1e", fg="white").pack(expand=True)

        # Center on screen
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = w//2 - size[0]//2
        y = h//2 - size[1]//2
        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

class SMTDApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SMTD - System Monitoring and Threat Detection Tool")
        self.geometry("1000x700")
        self.configure(bg="#1e1e1e")

        # Set window icon (Windows only supports .ico)
        if os.path.exists("icon.ico"):
            self.iconbitmap("icon.ico")

        self.style = ttk.Style()
        self.theme = "dark"
        self.set_theme(self.theme)

        self.create_menu()
        self.create_layout()

    def set_theme(self, theme):
        if theme == "dark":
            self.style.theme_use('clam')
            self.style.configure("TFrame", background="#1e1e1e")
            self.style.configure("TLabel", background="#1e1e1e", foreground="white")
            self.style.configure("TButton", background="#333", foreground="white")
        else:
            self.style.theme_use('default')
            self.style.configure("TFrame", background="white")
            self.style.configure("TLabel", background="white", foreground="black")
            self.style.configure("TButton", background="#ddd", foreground="black")

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.set_theme(self.theme)

    def create_menu(self):
        menubar = tk.Menu(self)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Dark/Light Mode", command=self.toggle_theme)
        menubar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "SMTD v1.0\nCreated with ❤️ in Python."))
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def create_layout(self):
        self.graph_frame = ttk.Frame(self)
        self.graph_frame.pack(side="top", fill="both", expand=True, padx=10, pady=5)

        cpu_label = ttk.Label(self.graph_frame, text="CPU/RAM/Disk/Network Graphs Placeholder", font=("Arial", 14))
        cpu_label.pack(pady=20)

        self.process_frame = ttk.Frame(self)
        self.process_frame.pack(side="top", fill="both", expand=True, padx=10, pady=5)

        process_label = ttk.Label(self.process_frame, text="Process Viewer Placeholder", font=("Arial", 14))
        process_label.pack(pady=20)

        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(side="bottom", fill="x")

        self.status_label = ttk.Label(self.status_frame, text="Status: Monitoring system...", font=("Arial", 10))
        self.status_label.pack(anchor="w", padx=10)

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    splash = SplashScreen(root)
    threading.Thread(target=lambda: load_app(splash)).start()
    root.mainloop()

def load_app(splash):
    time.sleep(2.5)  # Simulate loading time

    splash.destroy()
    app = SMTDApp()
    app.mainloop()

if __name__ == "__main__":
    main()
