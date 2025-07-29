from tkinter import ttk

class HomeFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="20")
        ttk.Label(self, text="Welcome to the Home Frame!").grid(column=0, row=0)
        ttk.Button(self, text="Click Me", command=self.quit_app).grid(column=1, row=0)

    def quit_app(self):
        self.winfo_toplevel().destroy()

