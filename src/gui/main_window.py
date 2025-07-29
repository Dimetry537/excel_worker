import tkinter as tk
from tkinter import ttk
from src.gui.frames.home_frame import HomeFrame

def run_app():
    root = tk.Tk()
    root.title("Excel Worker")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    home_tab = HomeFrame(notebook)
    notebook.add(home_tab, text="Ввод пациента")

    root.mainloop()