import tkinter as tk
from tkinter import ttk

from frames import Container


class GUI(tk.Tk):
    """
    GUI for file explorer.
    """

    def __init__(self):
        super().__init__()
        self.title("File Explorer")
        self.style = ttk.Style()
        self.style.configure("ExpBar.TButton", width=5)
        self.nbook = ttk.Notebook(self)
        self.nbook.grid(row=0, column=0, sticky="nsew")
        self.tab_1 = Container(self.nbook)
        self.nbook.add(self.tab_1, text="Tab 1")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

g = GUI()
g.mainloop()
